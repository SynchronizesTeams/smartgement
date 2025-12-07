package models

import (
	"time"

	"gorm.io/gorm"
)

type Product struct {
	ID             uint           `gorm:"primaryKey;autoIncrement" json:"id"`
	MerchantID     uint           `gorm:"not null;index" json:"merchant_id"`
	Name           string         `gorm:"size:255;not null" json:"name"`
	Description    string         `gorm:"type:text" json:"description"`
	Stock          int            `gorm:"default:0" json:"stock"`
	Price          float64        `gorm:"type:decimal(10,2);not null" json:"price"`
	Ingredients    string         `gorm:"type:text" json:"ingredients,omitempty"`
	ExpirationDate *time.Time     `json:"expiration_date,omitempty"`
	Category       string         `gorm:"size:100" json:"category,omitempty"`
	CreatedAt      time.Time      `json:"created_at"`
	UpdatedAt      time.Time      `json:"updated_at"`
	DeletedAt      gorm.DeletedAt `gorm:"index" json:"-"`

	// Belongs to User (merchant)
	Merchant User `gorm:"foreignKey:MerchantID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE" json:"-"`
}
