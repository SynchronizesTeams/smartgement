package controllers

import (
	"backend/models"
	"backend/services"
	"backend/utils"

	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
)

type ProductController struct {
	service *services.ProductService
}

func NewProductController(service *services.ProductService) *ProductController {
	return &ProductController{service: service}
}

// GetProducts retrieves all products for a merchant
func (ctrl *ProductController) GetProducts(c *fiber.Ctx) error {
	// TODO: Get merchantID from JWT token in context
	merchantID := c.Locals("merchantID").(string)
	merchantUUID, err := uuid.Parse(merchantID)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid merchant ID", err)
	}

	products, err := ctrl.service.GetAllProducts(merchantUUID)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusInternalServerError, "Failed to fetch products", err)
	}

	return utils.SuccessResponse(c, "Products retrieved successfully", products)
}

// GetProduct retrieves a single product by ID
func (ctrl *ProductController) GetProduct(c *fiber.Ctx) error {
	merchantID := c.Locals("merchantID").(string)
	merchantUUID, err := uuid.Parse(merchantID)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid merchant ID", err)
	}

	productID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid product ID", err)
	}

	product, err := ctrl.service.GetProductByID(productID, merchantUUID)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusNotFound, "Product not found", err)
	}

	return utils.SuccessResponse(c, "Product retrieved successfully", product)
}

// CreateProduct creates a new product
func (ctrl *ProductController) CreateProduct(c *fiber.Ctx) error {
	merchantID := c.Locals("merchantID").(string)
	merchantUUID, err := uuid.Parse(merchantID)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid merchant ID", err)
	}

	var product models.Product
	if err := c.BodyParser(&product); err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid request body", err)
	}

	product.MerchantID = merchantUUID

	if err := ctrl.service.CreateProduct(&product); err != nil {
		return utils.ErrorResponse(c, fiber.StatusInternalServerError, "Failed to create product", err)
	}

	return utils.SuccessResponse(c, "Product created successfully", product)
}

// UpdateProduct updates an existing product
func (ctrl *ProductController) UpdateProduct(c *fiber.Ctx) error {
	merchantID := c.Locals("merchantID").(string)
	merchantUUID, err := uuid.Parse(merchantID)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid merchant ID", err)
	}

	productID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid product ID", err)
	}

	var updates models.Product
	if err := c.BodyParser(&updates); err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid request body", err)
	}

	if err := ctrl.service.UpdateProduct(productID, merchantUUID, &updates); err != nil {
		return utils.ErrorResponse(c, fiber.StatusInternalServerError, "Failed to update product", err)
	}

	return utils.SuccessResponse(c, "Product updated successfully", nil)
}

// DeleteProduct deletes a product
func (ctrl *ProductController) DeleteProduct(c *fiber.Ctx) error {
	merchantID := c.Locals("merchantID").(string)
	merchantUUID, err := uuid.Parse(merchantID)
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid merchant ID", err)
	}

	productID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return utils.ErrorResponse(c, fiber.StatusBadRequest, "Invalid product ID", err)
	}

	if err := ctrl.service.DeleteProduct(productID, merchantUUID); err != nil {
		return utils.ErrorResponse(c, fiber.StatusInternalServerError, "Failed to delete product", err)
	}

	return utils.SuccessResponse(c, "Product deleted successfully", nil)
}
