package routes

import (
	"backend/controllers"
	"backend/middlewares"

	"github.com/gofiber/fiber/v2"
)

func SetupAuthRoutes(app *fiber.App, controller *controllers.AuthController) {
	api := app.Group("/api/auth")

	api.Post("/register", controller.Register)
	api.Post("/login", controller.Login)

	// Protected route - requires authentication
	api.Get("/me", middlewares.AuthMiddleware(), controller.GetCurrentUser)
}
