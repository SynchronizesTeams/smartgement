package controllers

import (
	"backend/models"
	"backend/services"
	"strconv"

	"github.com/gofiber/fiber/v2"
)

type TransactionController struct {
	Service *services.TransactionService
}

func NewTransactionController(service *services.TransactionService) *TransactionController {
	return &TransactionController{Service: service}
}

// CreateTransaction creates a new transaction
func (c *TransactionController) CreateTransaction(ctx *fiber.Ctx) error {
	// Get merchant ID from context (set by auth middleware)
	userIDFloat, ok := ctx.Locals("userID").(float64)
	if !ok {
		return ctx.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
			"error": "Unauthorized",
		})
	}
	merchantID := uint(userIDFloat)

	var transaction models.Transaction
	if err := ctx.BodyParser(&transaction); err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	result, err := c.Service.CreateTransaction(merchantID, &transaction)
	if err != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return ctx.Status(fiber.StatusCreated).JSON(result)
}

// GetTransactions retrieves all transactions for a merchant
func (c *TransactionController) GetTransactions(ctx *fiber.Ctx) error {
	userIDFloat, ok := ctx.Locals("userID").(float64)
	if !ok {
		return ctx.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
			"error": "Unauthorized",
		})
	}
	merchantID := uint(userIDFloat)

	limit, _ := strconv.Atoi(ctx.Query("limit", "20"))
	offset, _ := strconv.Atoi(ctx.Query("offset", "0"))

	transactions, total, err := c.Service.GetTransactions(merchantID, limit, offset)
	if err != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return ctx.JSON(fiber.Map{
		"data":   transactions,
		"total":  total,
		"limit":  limit,
		"offset": offset,
	})
}

// GetTransaction retrieves a single transaction
func (c *TransactionController) GetTransaction(ctx *fiber.Ctx) error {
	userIDFloat, ok := ctx.Locals("userID").(float64)
	if !ok {
		return ctx.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
			"error": "Unauthorized",
		})
	}
	merchantID := uint(userIDFloat)

	id, err := strconv.ParseUint(ctx.Params("id"), 10, 32)
	if err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid transaction ID",
		})
	}

	transaction, err := c.Service.GetTransaction(uint(id), merchantID)
	if err != nil {
		return ctx.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "Transaction not found",
		})
	}

	return ctx.JSON(transaction)
}

// GetTodaySales retrieves today's sales summary
func (c *TransactionController) GetTodaySales(ctx *fiber.Ctx) error {
	userIDFloat, ok := ctx.Locals("userID").(float64)
	if !ok {
		return ctx.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
			"error": "Unauthorized",
		})
	}
	merchantID := uint(userIDFloat)

	summary, err := c.Service.GetTodaySales(merchantID)
	if err != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return ctx.JSON(summary)
}

// UpdateTransaction updates transaction notes and customer name
func (c *TransactionController) UpdateTransaction(ctx *fiber.Ctx) error {
	userIDFloat, ok := ctx.Locals("userID").(float64)
	if !ok {
		return ctx.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
			"error": "Unauthorized",
		})
	}
	merchantID := uint(userIDFloat)

	id, err := strconv.ParseUint(ctx.Params("id"), 10, 32)
	if err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid transaction ID",
		})
	}

	var updates map[string]interface{}
	if err := ctx.BodyParser(&updates); err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	if err := c.Service.UpdateTransaction(uint(id), merchantID, updates); err != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return ctx.JSON(fiber.Map{
		"message": "Transaction updated successfully",
	})
}

// CancelTransaction cancels/voids a transaction
func (c *TransactionController) CancelTransaction(ctx *fiber.Ctx) error {
	userIDFloat, ok := ctx.Locals("userID").(float64)
	if !ok {
		return ctx.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
			"error": "Unauthorized",
		})
	}
	merchantID := uint(userIDFloat)

	id, err := strconv.ParseUint(ctx.Params("id"), 10, 32)
	if err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid transaction ID",
		})
	}

	if err := c.Service.CancelTransaction(uint(id), merchantID); err != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return ctx.JSON(fiber.Map{
		"message": "Transaction cancelled successfully",
	})
}
