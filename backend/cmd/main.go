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
	"github.com/gofiber/fiber/v2/middleware/requestid"
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
	if err := db.AutoMigrate(
		&models.User{},
		&models.Product{},
		&models.SyncJob{},
		&models.AutomationLog{},
		&models.Transaction{},
		&models.TransactionItem{},
	); err != nil {
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
	app.Use(requestid.New())
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
	authService := services.NewAuthService(db)
	productService := services.NewProductService(db)
	chatService := services.NewChatService(db)
	transactionService := services.NewTransactionService(db)

	// Initialize controllers
	authController := controllers.NewAuthController(authService)
	productController := controllers.NewProductController(productService)
	chatController := controllers.NewChatController(chatService)
	transactionController := controllers.NewTransactionController(transactionService)

	// Setup routes
	routes.SetupAuthRoutes(app, authController)
	routes.SetupProductRoutes(app, productController)
	routes.SetupChatRoutes(app, chatController)
	routes.SetupTransactionRoutes(app, transactionController)

	// Start server
	port := os.Getenv("PORT")
	if port == "" || port == "3000" {
		port = "8080"
	}

	log.Printf("Server starting on port %s...", port)
	if err := app.Listen(":" + port); err != nil {
		log.Fatal("Failed to start server:", err)
	}
}
