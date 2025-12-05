package main

import (
	"backend/config"
	"backend/controllers"
	"backend/models"
	"backend/qdrant"
	"backend/routes"
	"backend/services"
	"log"
	"os"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/joho/godotenv"
)

func main() {
	// Load environment variables
	if err := godotenv.Load(); err != nil {
		log.Println("Warning: .env file not found, using system environment variables")
	}

	// Initialize database
	config.InitDatabase()
	db := config.GetDB()

	// Run migrations
	log.Println("Running database migrations...")
	if err := db.AutoMigrate(&models.User{}, &models.Product{}, &models.SyncJob{}); err != nil {
		log.Fatal("Failed to run migrations:", err)
	}
	log.Println("Migrations completed successfully!")

	// Initialize Qdrant client
	qdrant.InitQdrant()

	// Initialize Fiber app
	app := fiber.New(fiber.Config{
		AppName: "Merchant Product Management API",
	})

	// Middleware
	app.Use(logger.New())
	app.Use(cors.New(cors.Config{
		AllowOrigins: "*",
		AllowHeaders: "Origin, Content-Type, Accept, Authorization",
	}))

	// Health check route
	app.Get("/health", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{
			"status":  "ok",
			"message": "Server is running",
		})
	})

	// Initialize services
	productService := services.NewProductService(db)
	chatService := services.NewChatService(db)

	// Initialize controllers
	productController := controllers.NewProductController(productService)
	chatController := controllers.NewChatController(chatService)

	// Setup routes
	routes.SetupProductRoutes(app, productController)
	routes.SetupChatRoutes(app, chatController)

	// Start server
	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}

	log.Printf("Server starting on port %s...", port)
	if err := app.Listen(":" + port); err != nil {
		log.Fatal("Failed to start server:", err)
	}
}
