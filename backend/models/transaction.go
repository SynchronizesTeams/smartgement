package models

import (
	"time"
)

type Transaction struct {
	ID            uint      `gorm:"primaryKey" json:"id"`
	MerchantID    uint      `gorm:"not null;index" json:"merchant_id"`
	TotalAmount   float64   `gorm:"not null" json:"total_amount"`
	PaymentMethod string    `gorm:"type:varchar(50)" json:"payment_method"` // cash, card, ewallet
	CustomerName  string    `gorm:"type:varchar(255)" json:"customer_name"`
	Notes         string    `gorm:"type:text" json:"notes"`
	Status        string    `gorm:"type:varchar(20);default:'completed'" json:"status"` // completed, cancelled
	CreatedAt     time.Time `json:"created_at"`
	UpdatedAt     time.Time `json:"updated_at"`

	// Relations
	Items []TransactionItem `gorm:"foreignKey:TransactionID" json:"items,omitempty"`
}

type TransactionItem struct {
	ID            uint    `gorm:"primaryKey" json:"id"`
	TransactionID uint    `gorm:"not null;index" json:"transaction_id"`
	ProductID     uint    `gorm:"not null;index" json:"product_id"`
	ProductName   string  `gorm:"type:varchar(255)" json:"product_name"` // Snapshot of product name
	Quantity      int     `gorm:"not null" json:"quantity"`
	Price         float64 `gorm:"not null" json:"price"` // Snapshot of price at time of sale
	Subtotal      float64 `gorm:"not null" json:"subtotal"`

	// Relations
	Product *Product `gorm:"foreignKey:ProductID" json:"product,omitempty"`
}

func (Transaction) TableName() string {
	return "transactions"
}

func (TransactionItem) TableName() string {
	return "transaction_items"
}
