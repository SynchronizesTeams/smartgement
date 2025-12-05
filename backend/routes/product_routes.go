package routes

import (
	"backend/controllers"
	"backend/middlewares"

	"github.com/gofiber/fiber/v2"
)

func SetupProductRoutes(app *fiber.App, controller *controllers.ProductController) {
	api := app.Group("/api")
	products := api.Group("/products", middlewares.AuthMiddleware())

	products.Get("/", controller.GetProducts)
	products.Get("/:id", controller.GetProduct)
	products.Post("/", controller.CreateProduct)
	products.Put("/:id", controller.UpdateProduct)
	products.Delete("/:id", controller.DeleteProduct)
}
