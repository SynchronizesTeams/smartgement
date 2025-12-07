package controllers

import (
	"backend/models"
	"backend/services"
	"backend/utils"
	"strconv"

	"github.com/gofiber/fiber/v2"
)

type ProductController struct {
	service *services.ProductService
}

func NewProductController(service *services.ProductService) *ProductController {
	return &ProductController{service: service}
}

// GetProducts retrieves all products for a merchant
func (ctrl *ProductController) GetProducts(c *fiber.Ctx) error {
	userIDFloat, ok := c.Locals("userID").(float64)
	if !ok {
		return utils.ErrorResponse(c, fiber.StatusUnauthorized, "Unauthorized", nil)
	}
	merchantID := uint(userIDFloat)

	products, err := ctrl.service.GetAllProducts(merchantID)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusInternalServerError, "Failed to fetch products", err)
	}

	return utils.SuccessResponse(c, "Products retrieved successfully", products)
}

// GetProduct retrieves a single product by ID
func (ctrl *ProductController) GetProduct(c *fiber.Ctx) error {
	userIDFloat, ok := c.Locals("userID").(float64)
	if !ok {
		return utils.ErrorResponse(c, fiber.StatusUnauthorized, "Unauthorized", nil)
	}
	merchantID := uint(userIDFloat)

	productIDStr := c.Params("id")
	productID, err := strconv.ParseUint(productIDStr, 10, 32)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid product ID", err)
	}

	product, err := ctrl.service.GetProductByID(uint(productID), merchantID)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusNotFound, "Product not found", err)
	}

	return utils.SuccessResponse(c, "Product retrieved successfully", product)
}

// CreateProduct creates a new product
func (ctrl *ProductController) CreateProduct(c *fiber.Ctx) error {
	userIDFloat, ok := c.Locals("userID").(float64)
	if !ok {
		return utils.ErrorResponse(c, fiber.StatusUnauthorized, "Unauthorized", nil)
	}
	merchantID := uint(userIDFloat)

	var product models.Product
	if err := c.BodyParser(&product); err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid request body", err)
	}

	product.MerchantID = merchantID

	if err := ctrl.service.CreateProduct(&product); err != nil {
		return utils.ErrorResponse(c, fiber.StatusInternalServerError, "Failed to create product", err)
	}

	return utils.SuccessResponse(c, "Product created successfully", product)
}

// UpdateProduct updates an existing product
func (ctrl *ProductController) UpdateProduct(c *fiber.Ctx) error {
	userIDFloat, ok := c.Locals("userID").(float64)
	if !ok {
		return utils.ErrorResponse(c, fiber.StatusUnauthorized, "Unauthorized", nil)
	}
	merchantID := uint(userIDFloat)

	productIDStr := c.Params("id")
	productID, err := strconv.ParseUint(productIDStr, 10, 32)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid product ID", err)
	}

	var updates models.Product
	if err := c.BodyParser(&updates); err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid request body", err)
	}

	if err := ctrl.service.UpdateProduct(uint(productID), merchantID, &updates); err != nil {
		return utils.ErrorResponse(c, fiber.StatusInternalServerError, "Failed to update product", err)
	}

	return utils.SuccessResponse(c, "Product updated successfully", nil)
}

// DeleteProduct deletes a product
func (ctrl *ProductController) DeleteProduct(c *fiber.Ctx) error {
	userIDFloat, ok := c.Locals("userID").(float64)
	if !ok {
		return utils.ErrorResponse(c, fiber.StatusUnauthorized, "Unauthorized", nil)
	}
	merchantID := uint(userIDFloat)

	productIDStr := c.Params("id")
	productID, err := strconv.ParseUint(productIDStr, 10, 32)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid product ID", err)
	}

	if err := ctrl.service.DeleteProduct(uint(productID), merchantID); err != nil {
		return utils.ErrorResponse(c, fiber.StatusInternalServerError, "Failed to delete product", err)
	}

	return utils.SuccessResponse(c, "Product deleted successfully", nil)
}

//generate description with AI /generate-description in python

