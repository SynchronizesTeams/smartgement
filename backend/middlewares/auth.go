package middlewares

import (
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt/v5"
)

func AuthMiddleware() fiber.Handler {
	return func(c *fiber.Ctx) error {
		authHeader := c.Get("Authorization")
		if authHeader == "" {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"error": "Missing authorization header",
			})
		}

		// Expect: Bearer <token>
		if !strings.HasPrefix(authHeader, "Bearer ") {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"error": "Invalid authorization format",
			})
		}

		tokenString := strings.TrimPrefix(authHeader, "Bearer ")

		jwtSecret := os.Getenv("JWT_SECRET")
		if jwtSecret == "" {
			// SECURITY: Stop if secret is not defined
			return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
				"error": "JWT secret not configured",
			})
		}

		token, err := jwt.Parse(tokenString, func(t *jwt.Token) (interface{}, error) {
			if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf("unexpected signing method: %v", t.Header["alg"])
			}
			return []byte(jwtSecret), nil
		})

		if err != nil || !token.Valid {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"error": "Invalid or expired token",
			})
		}

		claims := token.Claims.(jwt.MapClaims)

		// Validate exp (token expiry)
		if expFloat, ok := claims["exp"].(float64); ok {
			exp := int64(expFloat)
			if time.Now().Unix() > exp {
				return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
					"error": "Token expired",
				})
			}
		} else {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"error": "Missing exp in token",
			})
		}

		// Get user_id from claims (this is the actual user ID in database)
		userIDFloat, ok := claims["user_id"].(float64)
		if !ok {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"error": "Invalid user_id format in token",
			})
		}

		// Store userID for use in controllers
		c.Locals("userID", userIDFloat)

		return c.Next()
	}
}
