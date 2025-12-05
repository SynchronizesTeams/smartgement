package middlewares

import (
	"os"

	"github.com/gofiber/fiber/v2"
)

// AuthMiddleware is a placeholder JWT authentication middleware
func AuthMiddleware() fiber.Handler {
	return func(c *fiber.Ctx) error {
		// TODO: Implement actual JWT authentication
		// For now, this is a placeholder that allows all requests

		token := c.Get("Authorization")
		if token == "" {
			// In production, this should return 401 Unauthorized
			// For development/placeholder, we'll allow it
			c.Locals("merchantID", "00000000-0000-0000-0000-000000000000")
		}

		// TODO: Verify JWT token using JWT_SECRET from env
		jwtSecret := os.Getenv("JWT_SECRET")
		_ = jwtSecret // Placeholder to avoid unused variable warning

		// TODO: Extract merchantID from JWT claims
		// c.Locals("merchantID", extractedMerchantID)

		return c.Next()
	}
}
