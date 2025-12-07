package controllers

import (
	"backend/models"
	"backend/services"
	"backend/utils"

	"github.com/gofiber/fiber/v2"
)

type AuthController struct {
	service *services.AuthService
}

func NewAuthController(service *services.AuthService) *AuthController {
	return &AuthController{service: service}
}

type LoginRequest struct {
	Username       string `json:"username"`
	Password       string `json:"password"`
	RecaptchaToken string `json:"recaptcha_token"`
}

type RegisterRequest struct {
	Username       string `json:"username"`
	Password       string `json:"password"`
	RecaptchaToken string `json:"recaptcha_token"`
}

func (ctrl *AuthController) Register(c *fiber.Ctx) error {
	var req RegisterRequest
	if err := c.BodyParser(&req); err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid request body", err)
	}

	if req.Username == "" || req.Password == "" {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Username and password are required", nil)
	}

	// Verify reCAPTCHA
	valid, err := utils.VerifyRecaptcha(req.RecaptchaToken)
	if err != nil || !valid {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "reCAPTCHA verification failed", err)
	}

	user := models.User{
		Username: req.Username,
		Password: req.Password,
	}

	if err := ctrl.service.Register(&user); err != nil {
		return utils.ErrorResponse(c, fiber.StatusInternalServerError, "Failed to register user", err)
	}

	return utils.SuccessResponse(c, "User registered successfully", nil)
}

func (ctrl *AuthController) Login(c *fiber.Ctx) error {
	var req LoginRequest
	if err := c.BodyParser(&req); err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid request body", err)
	}

	// Verify reCAPTCHA
	valid, err := utils.VerifyRecaptcha(req.RecaptchaToken)
	if err != nil || !valid {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "reCAPTCHA verification failed", err)
	}

	token, user, err := ctrl.service.Login(req.Username, req.Password)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusUnauthorized, err.Error(), nil)
	}

	return utils.SuccessResponse(c, "Login successful", fiber.Map{
		"token": token,
		"user": fiber.Map{
			"id":       user.ID,
			"username": user.Username,
		},
	})
}

// Loading Authorized User
func (ctrl *AuthController) GetCurrentUser(c *fiber.Ctx) error {

	// Read user_id from JWT claims already placed in Locals() by AuthMiddleware
	userID, ok := c.Locals("userID").(float64)
	if !ok {
		return utils.ErrorResponse(c, fiber.StatusUnauthorized, "Unauthorized", nil)
	}

	// Fetch user by ID
	user, err := ctrl.service.GetUserByID(uint(userID))
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusNotFound, "User not found", err)
	}

	return utils.SuccessResponse(c, "User retrieved successfully", fiber.Map{
		"user": fiber.Map{
			"id":       user.ID,
			"username": user.Username,
		},
	})
}
