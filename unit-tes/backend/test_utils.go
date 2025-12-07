package backend

import (
	"backend/models"
	"backend/utils"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

// SetupTestDB creates an in-memory SQLite database for testing
func SetupTestDB() *gorm.DB {
	db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	if err != nil {
		panic("failed to connect test database")
	}

	// Auto-migrate models
	db.AutoMigrate(&models.User{}, &models.Product{}, &models.Transaction{}, &models.TransactionItem{})

	return db
}

// CreateTestUser creates a test user in the database
func CreateTestUser(db *gorm.DB, username, password string) *models.User {
	hashedPassword, _ := utils.HashPassword(password)
	user := &models.User{
		Username: username,
		Password: hashedPassword,
	}
	db.Create(user)
	return user
}

// CreateTestProduct creates a test product for a merchant
func CreateTestProduct(db *gorm.DB, merchantID uint, name string, price float64, stock int) *models.Product {
	product := &models.Product{
		MerchantID:  merchantID,
		Name:        name,
		Price:       price,
		Stock:       stock,
		Description: "Test product description",
		Category:    "Test Category",
	}
	db.Create(product)
	return product
}

// GenerateTestJWT creates a JWT token for testing
func GenerateTestJWT(userID uint) string {
	claims := jwt.MapClaims{
		"user_id": float64(userID),
		"exp":     time.Now().Add(time.Hour * 24).Unix(),
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, _ := token.SignedString([]byte("test-secret"))
	return tokenString
}

// MockRecaptchaVerification mocks the recaptcha verification for testing
func MockRecaptchaVerification() {
	// In real tests, you would use a mocking library or dependency injection
	// For now, this is a placeholder for the concept
}

// CleanupTestDB closes and cleans up the test database
func CleanupTestDB(db *gorm.DB) {
	sqlDB, _ := db.DB()
	sqlDB.Close()
}

// CreateTestTransaction creates a test transaction
func CreateTestTransaction(db *gorm.DB, merchantID uint, total float64) *models.Transaction {
	transaction := &models.Transaction{
		MerchantID:   merchantID,
		Total:        total,
		CustomerName: "Test Customer",
	}
	db.Create(transaction)
	return transaction
}
