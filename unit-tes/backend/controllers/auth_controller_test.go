package controllers

import (
	"backend/controllers"
	"backend/models"
	"backend/services"
	"bytes"
	"encoding/json"
	"net/http/httptest"
	"testing"
	testutils "unit-tes/backend"

	"github.com/gofiber/fiber/v2"
	"github.com/stretchr/testify/assert"
)

func TestRegister_Success(t *testing.T) {
	// Setup
	db := testutils.SetupTestDB()
	defer testutils.CleanupTestDB(db)

	authService := services.NewAuthService(db)
	authController := controllers.NewAuthController(authService)

	app := fiber.New()
	app.Post("/register", authController.Register)

	// Test data
	reqBody := map[string]interface{}{
		"username":        "testuser",
		"password":        "testpass123",
		"recaptcha_token": "fake-token",
	}
	body, _ := json.Marshal(reqBody)

	// Make request
	req := httptest.NewRequest("POST", "/register", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")

	resp, err := app.Test(req)
	assert.NoError(t, err)
	assert.Equal(t, 200, resp.StatusCode)

	// Verify user was created
	var user models.User
	db.Where("username = ?", "testuser").First(&user)
	assert.Equal(t, "testuser", user.Username)
}

func TestRegister_MissingFields(t *testing.T) {
	db := testutils.SetupTestDB()
	defer testutils.CleanupTestDB(db)

	authService := services.NewAuthService(db)
	authController := controllers.NewAuthController(authService)

	app := fiber.New()
	app.Post("/register", authController.Register)

	// Missing password
	reqBody := map[string]interface{}{
		"username":        "testuser",
		"recaptcha_token": "fake-token",
	}
	body, _ := json.Marshal(reqBody)

	req := httptest.NewRequest("POST", "/register", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")

	resp, err := app.Test(req)
	assert.NoError(t, err)
	assert.Equal(t, 400, resp.StatusCode)
}

func TestLogin_Success(t *testing.T) {
	db := testutils.SetupTestDB()
	defer testutils.CleanupTestDB(db)

	// Create test user
	testutils.CreateTestUser(db, "testuser", "testpass123")

	authService := services.NewAuthService(db)
	authController := controllers.NewAuthController(authService)

	app := fiber.New()
	app.Post("/login", authController.Login)

	reqBody := map[string]interface{}{
		"username":        "testuser",
		"password":        "testpass123",
		"recaptcha_token": "fake-token",
	}
	body, _ := json.Marshal(reqBody)

	req := httptest.NewRequest("POST", "/login", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")

	resp, err := app.Test(req)
	assert.NoError(t, err)
	assert.Equal(t, 200, resp.StatusCode)

	// Parse response
	var result map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&result)

	data := result["data"].(map[string]interface{})
	assert.NotNil(t, data["token"])
	assert.NotNil(t, data["user"])
}

func TestLogin_WrongPassword(t *testing.T) {
	db := testutils.SetupTestDB()
	defer testutils.CleanupTestDB(db)

	testutils.CreateTestUser(db, "testuser", "testpass123")

	authService := services.NewAuthService(db)
	authController := controllers.NewAuthController(authService)

	app := fiber.New()
	app.Post("/login", authController.Login)

	reqBody := map[string]interface{}{
		"username":        "testuser",
		"password":        "wrongpassword",
		"recaptcha_token": "fake-token",
	}
	body, _ := json.Marshal(reqBody)

	req := httptest.NewRequest("POST", "/login", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")

	resp, err := app.Test(req)
	assert.NoError(t, err)
	assert.Equal(t, 401, resp.StatusCode)
}

func TestGetCurrentUser_Success(t *testing.T) {
	db := testutils.SetupTestDB()
	defer testutils.CleanupTestDB(db)

	user := testutils.CreateTestUser(db, "testuser", "testpass123")

	authService := services.NewAuthService(db)
	authController := controllers.NewAuthController(authService)

	app := fiber.New()
	app.Get("/me", func(c *fiber.Ctx) error {
		// Simulate authenticated request
		c.Locals("userID", float64(user.ID))
		return authController.GetCurrentUser(c)
	})

	req := httptest.NewRequest("GET", "/me", nil)
	resp, err := app.Test(req)

	assert.NoError(t, err)
	assert.Equal(t, 200, resp.StatusCode)

	var result map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&result)

	data := result["data"].(map[string]interface{})
	userMap := data["user"].(map[string]interface{})
	assert.Equal(t, "testuser", userMap["username"])
}

func TestGetCurrentUser_Unauthorized(t *testing.T) {
	db := testutils.SetupTestDB()
	defer testutils.CleanupTestDB(db)

	authService := services.NewAuthService(db)
	authController := controllers.NewAuthController(authService)

	app := fiber.New()
	app.Get("/me", authController.GetCurrentUser)

	req := httptest.NewRequest("GET", "/me", nil)
	resp, err := app.Test(req)

	assert.NoError(t, err)
	assert.Equal(t, 401, resp.StatusCode)
}
