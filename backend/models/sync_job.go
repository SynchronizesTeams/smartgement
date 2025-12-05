package models

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type SyncJob struct {
	ID         uuid.UUID `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	MerchantID uuid.UUID `gorm:"type:uuid;not null;index" json:"merchant_id"`
	JobType    string    `gorm:"not null" json:"job_type"`
	Status     string    `gorm:"not null" json:"status"`
	CreatedAt  time.Time `json:"created_at"`
	UpdatedAt  time.Time `json:"updated_at"`

	// Foreign key relationship
	Merchant User `gorm:"foreignKey:MerchantID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE;" json:"-"`
}

func (s *SyncJob) BeforeCreate(tx *gorm.DB) (err error) {
	if s.ID == uuid.Nil {
		s.ID = uuid.New()
	}
	return
}
