package controllers

import (
	"backend/controllers"
	"backend/models"
	"backend/services"
	"bytes"
	"encoding/json"
	"fmt"
	"net/http/httptest"
	"testing"
	testutils "unit-tes/backend"

	"github.com/gofiber/fiber/v2"
	"github.com/stretchr/testify/assert"
)

func setupProductTest() (*fiber.App, *models.User, func()) {
	db := testutils.SetupTestDB()
	user := testutils.CreateTestUser(db, "merchant", "pass123")

	productService := services.NewProductService(db)
	productController := controllers.NewProductController(productService)

	app := fiber.New()

	// Middleware to simulate authentication
	app.Use(func(c *fiber.Ctx) error {
		c.Locals("userID", float64(user.ID))
		return c.Next()
	})

	app.Get("/products", productController.GetProducts)
	app.Get("/products/:id", productController.GetProduct)
	app.Post("/products", productController.CreateProduct)
	app.Put("/products/:id", productController.UpdateProduct)
	app.Delete("/products/:id", productController.DeleteProduct)

	cleanup := func() {
		testutils.CleanupTestDB(db)
	}

	return app, user, cleanup
}

func TestGetProducts_Success(t *testing.T) {
	app, user, cleanup := setupProductTest()
	defer cleanup()

	req := httptest.NewRequest("GET", "/products", nil)
	resp, err := app.Test(req)

	assert.NoError(t, err)
	assert.Equal(t, 200, resp.StatusCode)

	var result map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&result)
	assert.Equal(t, "Products retrieved successfully", result["message"])
}

func TestCreateProduct_Success(t *testing.T) {
	app, user, cleanup := setupProductTest()
	defer cleanup()

	reqBody := map[string]interface{}{
		"name":        "Test Product",
		"price":       15000.0,
		"stock":       50,
		"description": "Test description",
		"category":    "Test",
	}
	body, _ := json.Marshal(reqBody)

	req := httptest.NewRequest("POST", "/products", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")

	resp, err := app.Test(req)

	assert.NoError(t, err)
	assert.Equal(t, 200, resp.StatusCode)

	var result map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&result)

	data := result["data"].(map[string]interface{})
	assert.Equal(t, "Test Product", data["name"])
	assert.Equal(t, 15000.0, data["price"])
}

func TestGetProduct_Success(t *testing.T) {
	app, user, cleanup := setupProductTest()
	defer cleanup()

	// First create a product
	db := testutils.SetupTestDB()
	product := testutils.CreateTestProduct(db, user.ID, "Test Product", 10000, 20)

	req := httptest.NewRequest("GET", fmt.Sprintf("/products/%d", product.ID), nil)
	resp, err := app.Test(req)

	assert.NoError(t, err)
	assert.Equal(t, 200, resp.StatusCode)

	var result map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&result)

	data := result["data"].(map[string]interface{})
	assert.Equal(t, "Test Product", data["name"])
}

func TestUpdateProduct_Success(t *testing.T) {
	app, user, cleanup := setupProductTest()
	defer cleanup()

	db := testutils.SetupTestDB()
	product := testutils.CreateTestProduct(db, user.ID, "Test Product", 10000, 20)

	reqBody := map[string]interface{}{
		"price": 15000.0,
		"stock": 30,
	}
	body, _ := json.Marshal(reqBody)

	req := httptest.NewRequest("PUT", fmt.Sprintf("/products/%d", product.ID), bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")

	resp, err := app.Test(req)

	assert.NoError(t, err)
	assert.Equal(t, 200, resp.StatusCode)
}

func TestDeleteProduct_Success(t *testing.T) {
	app, user, cleanup := setupProductTest()
	defer cleanup()

	db := testutils.SetupTestDB()
	product := testutils.CreateTestProduct(db, user.ID, "Test Product", 10000, 20)

	req := httptest.NewRequest("DELETE", fmt.Sprintf("/products/%d", product.ID), nil)
	resp, err := app.Test(req)

	assert.NoError(t, err)
	assert.Equal(t, 200, resp.StatusCode)

	// Verify product is deleted
	var deletedProduct models.Product
	result := db.First(&deletedProduct, product.ID)
	assert.Error(t, result.Error)
}

func TestCreateProduct_InvalidData(t *testing.T) {
	app, _, cleanup := setupProductTest()
	defer cleanup()

	reqBody := map[string]interface{}{
		"name": "", // Invalid empty name
	}
	body, _ := json.Marshal(reqBody)

	req := httptest.NewRequest("POST", "/products", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")

	resp, err := app.Test(req)

	assert.NoError(t, err)
	// Should return error status (implementation dependent)
	assert.True(t, resp.StatusCode >= 400)
}
