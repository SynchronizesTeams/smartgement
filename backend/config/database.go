package config

import (
	"fmt"
	"log"
	"os"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var DB *gorm.DB

func InitDatabase() {
	var err error

	dbUser := os.Getenv("DB_USER")
	if dbUser == "" {
		dbUser = "root" // Default user
	}

	dbPassword := os.Getenv("DB_PASSWORD")
	// No default for password, an empty string means no password

	dbHost := os.Getenv("DB_HOST")
	if dbHost == "" {
		dbHost = "127.0.0.1" // Default host
	}

	dbPort := os.Getenv("DB_PORT")
	if dbPort == "" {
		dbPort = "3306" // Default port
	}

	dbName := os.Getenv("DB_NAME")
	if dbName == "" {
		dbName = "smartgement" // Default database name
	}

	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=utf8mb4&parseTime=True&loc=Local",
		dbUser, dbPassword, dbHost, dbPort, dbName)

	DB, err = gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed to connect to MySQL database:", err)
	}

	log.Println("MySQL database connected successfully!")
}

func GetDB() *gorm.DB {
	return DB
}
