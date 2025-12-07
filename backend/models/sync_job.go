package models

import (
	"time"

	"gorm.io/gorm"
)

type SyncJob struct {
	ID         uint           `gorm:"primaryKey;autoIncrement" json:"id"`
	MerchantID uint           `gorm:"not null;index" json:"merchant_id"`
	JobType    string         `gorm:"size:50;not null" json:"job_type"`
	Status     string         `gorm:"size:50;not null" json:"status"`
	CreatedAt  time.Time      `json:"created_at"`
	UpdatedAt  time.Time      `json:"updated_at"`
	DeletedAt  gorm.DeletedAt `gorm:"index" json:"-"`

	// Belongs to User (merchant)
	Merchant User `gorm:"foreignKey:MerchantID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE" json:"-"`
}
