package controllers

import (
	"backend/services"
	"backend/utils"

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
	merchantID := c.Locals("merchantID").(string)

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
	merchantID := c.Locals("merchantID").(string)

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
