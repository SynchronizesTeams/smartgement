package controllers

import (
	"backend/services"
	"backend/utils"
	"strconv"

	"github.com/gofiber/fiber/v2"
)

type ChatController struct {
	service *services.ChatService
}

func NewChatController(service *services.ChatService) *ChatController {
	return &ChatController{service: service}
}

// CommandRequest represents the request body for chat commands
type CommandRequest struct {
	Command string `json:"command"`
}

// ProcessCommand handles chat command processing
func (ctrl *ChatController) ProcessCommand(c *fiber.Ctx) error {
	userIDFloat, ok := c.Locals("userID").(float64)
	if !ok {
		return utils.ErrorResponse(c, fiber.StatusUnauthorized, "Unauthorized", nil)
	}
	merchantID := strconv.FormatUint(uint64(userIDFloat), 10)

	var req CommandRequest
	if err := c.BodyParser(&req); err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid request body", err)
	}

	if req.Command == "" {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Command is required", nil)
	}

	response, err := ctrl.service.ProcessCommand(merchantID, req.Command)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusInternalServerError, "Failed to process command", err)
	}

	return utils.SuccessResponse(c, "Command processed successfully", fiber.Map{
		"response": response,
	})
}

// GetChatHistory retrieves chat history for the merchant
func (ctrl *ChatController) GetChatHistory(c *fiber.Ctx) error {
	userIDFloat, ok := c.Locals("userID").(float64)
	if !ok {
		return utils.ErrorResponse(c, fiber.StatusUnauthorized, "Unauthorized", nil)
	}
	merchantID := strconv.FormatUint(uint64(userIDFloat), 10)

	limit := c.QueryInt("limit", 50)
	if limit > 100 {
		limit = 100
	}

	history, err := ctrl.service.GetChatHistory(merchantID, limit)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusInternalServerError, "Failed to fetch chat history", err)
	}

	return utils.SuccessResponse(c, "Chat history retrieved successfully", history)
}
