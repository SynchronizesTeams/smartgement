package models

import (
	"time"
)

type AutomationLog struct {
	ID         uint      `gorm:"primaryKey;autoIncrement" json:"id"`
	MerchantID uint      `gorm:"not null;index" json:"merchant_id"`
	Action     string    `gorm:"type:text;not null" json:"action"`
	Result     string    `gorm:"type:text" json:"result"`
	CreatedAt  time.Time `json:"created_at"`

	// Belongs to User (merchant)
	Merchant User `gorm:"foreignKey:MerchantID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE" json:"-"`
}
