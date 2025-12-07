package controllers

import (
	"backend/models"
	"backend/services"
	"backend/utils"
	"fmt"

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

// GetCurrentUser returns the currently authenticated user's information
func (ctrl *AuthController) GetCurrentUser(c *fiber.Ctx) error {
	// Get merchantID from context (set by auth middleware)
	merchantIDStr, ok := c.Locals("merchantID").(string)
	if !ok {
		return utils.ErrorResponse(c, fiber.StatusUnauthorized, "Unauthorized", nil)
	}

	// Convert merchantID to uint
	var merchantID uint
	if _, err := fmt.Sscanf(merchantIDStr, "%d", &merchantID); err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid merchant ID", err)
	}

	// Fetch user from database
	user, err := ctrl.service.GetUserByID(merchantID)
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
