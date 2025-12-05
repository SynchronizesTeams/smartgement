package routes

import (
	"backend/controllers"
	"backend/middlewares"

	"github.com/gofiber/fiber/v2"
)

func SetupChatRoutes(app *fiber.App, controller *controllers.ChatController) {
	api := app.Group("/api")
	chat := api.Group("/chat", middlewares.AuthMiddleware())

	chat.Post("/command", controller.ProcessCommand)
	chat.Get("/history", controller.GetChatHistory)
}
