package services

import (
	"backend/models"
	"errors"
	"fmt"
	"os"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
)

type AuthService struct {
	db *gorm.DB
}

func NewAuthService(db *gorm.DB) *AuthService {
	return &AuthService{db: db}
}

func (s *AuthService) Register(user *models.User) error {
	// Hash password
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	user.Password = string(hashedPassword)

	fmt.Printf("Attempting to create user: %s\n", user.Username)
	err = s.db.Create(user).Error
	if err != nil {
		fmt.Printf("Error creating user: %v\n", err)
		return err
	}
	fmt.Printf("User created successfully with ID: %d\n", user.ID)
	return nil
}

func (s *AuthService) Login(username, password string) (string, *models.User, error) {
	var user models.User
	if err := s.db.Where("username = ?", username).First(&user).Error; err != nil {
		return "", nil, errors.New("invalid credentials")
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password)); err != nil {
		return "", nil, errors.New("invalid credentials")
	}

	// Generate JWT
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"user_id": user.ID,
		"exp":     time.Now().Add(time.Hour * 24).Unix(),
	})

	jwtSecret := os.Getenv("JWT_SECRET")
	if jwtSecret == "" {
		jwtSecret = "secret" // Fallback for dev
	}

	tokenString, err := token.SignedString([]byte(jwtSecret))
	if err != nil {
		return "", nil, err
	}

	return tokenString, &user, nil
}

// GetUserByID retrieves a user by their ID
func (s *AuthService) GetUserByID(id uint) (*models.User, error) {
	var user models.User
	if err := s.db.First(&user, id).Error; err != nil {
		return nil, errors.New("user not found")
	}
	return &user, nil
}
