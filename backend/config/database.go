package config

import (
	"log"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var DB *gorm.DB

// MySQL connection - hardcoded for local development
// Database: smartgement, User: root, No password
const DSN = "root:@tcp(127.0.0.1:3306)/smartgement?charset=utf8mb4&parseTime=True&loc=Local"

func InitDatabase() {
	var err error
	DB, err = gorm.Open(mysql.Open(DSN), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed to connect to MySQL database:", err)
	}

	log.Println("MySQL database connected successfully!")
}

func GetDB() *gorm.DB {
	return DB
}
