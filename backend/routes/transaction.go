package routes

import (
	"backend/controllers"
	"backend/middlewares"

	"github.com/gofiber/fiber/v2"
)

func SetupTransactionRoutes(app *fiber.App, controller *controllers.TransactionController) {
	api := app.Group("/api")

	// Protected transaction routes
	transactions := api.Group("/transactions")
	transactions.Use(middlewares.AuthMiddleware())

	transactions.Post("/", controller.CreateTransaction)
	transactions.Get("/", controller.GetTransactions)
	transactions.Get("/today", controller.GetTodaySales)
	transactions.Get("/:id", controller.GetTransaction)
}
