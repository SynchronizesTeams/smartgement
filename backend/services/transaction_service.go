package services

import (
	"backend/models"
	"time"

	"gorm.io/gorm"
)

type TransactionService struct {
	DB *gorm.DB
}

func NewTransactionService(db *gorm.DB) *TransactionService {
	return &TransactionService{DB: db}
}

// CreateTransaction creates a new transaction with items and updates product stock
func (s *TransactionService) CreateTransaction(merchantID uint, transaction *models.Transaction) (*models.Transaction, error) {
	// Start transaction
	tx := s.DB.Begin()
	defer func() {
		if r := recover(); r != nil {
			tx.Rollback()
		}
	}()

	// Set merchant ID
	transaction.MerchantID = merchantID
	transaction.CreatedAt = time.Now()
	transaction.UpdatedAt = time.Now()

	// Calculate total and update stock
	var total float64
	for i := range transaction.Items {
		item := &transaction.Items[i]

		// Get product
		var product models.Product
		if err := tx.First(&product, item.ProductID).Error; err != nil {
			tx.Rollback()
			return nil, err
		}

		// Check stock
		if product.Stock < item.Quantity {
			tx.Rollback()
			return nil, gorm.ErrInvalidData
		}

		// Calculate subtotal
		item.Price = product.Price
		item.ProductName = product.Name
		item.Subtotal = float64(item.Quantity) * item.Price
		total += item.Subtotal

		// Update product stock
		product.Stock -= item.Quantity
		if err := tx.Save(&product).Error; err != nil {
			tx.Rollback()
			return nil, err
		}
	}

	transaction.TotalAmount = total

	// Create transaction
	if err := tx.Create(transaction).Error; err != nil {
		tx.Rollback()
		return nil, err
	}

	// Commit transaction
	if err := tx.Commit().Error; err != nil {
		return nil, err
	}

	// Load items with product details
	s.DB.Preload("Items").First(transaction, transaction.ID)

	return transaction, nil
}

// GetTransactions retrieves transactions for a merchant
func (s *TransactionService) GetTransactions(merchantID uint, limit, offset int) ([]models.Transaction, int64, error) {
	var transactions []models.Transaction
	var total int64

	query := s.DB.Where("merchant_id = ?", merchantID)

	// Count total
	query.Model(&models.Transaction{}).Count(&total)

	// Get paginated results
	err := query.
		Preload("Items").
		Order("created_at DESC").
		Limit(limit).
		Offset(offset).
		Find(&transactions).Error

	return transactions, total, err
}

// GetTransaction retrieves a single transaction by ID
func (s *TransactionService) GetTransaction(id uint, merchantID uint) (*models.Transaction, error) {
	var transaction models.Transaction
	err := s.DB.
		Where("id = ? AND merchant_id = ?", id, merchantID).
		Preload("Items.Product").
		First(&transaction).Error

	return &transaction, err
}

// GetTodaySales gets today's sales summary
func (s *TransactionService) GetTodaySales(merchantID uint) (map[string]interface{}, error) {
	var totalAmount float64
	var count int64

	today := time.Now().Format("2006-01-02")

	err := s.DB.Model(&models.Transaction{}).
		Where("merchant_id = ? AND DATE(created_at) = ? AND status = 'completed'", merchantID, today).
		Select("COALESCE(SUM(total_amount), 0)").
		Scan(&totalAmount).Error

	if err != nil {
		return nil, err
	}

	s.DB.Model(&models.Transaction{}).
		Where("merchant_id = ? AND DATE(created_at) = ? AND status = 'completed'", merchantID, today).
		Count(&count)

	return map[string]interface{}{
		"total_amount": totalAmount,
		"count":        count,
		"date":         today,
	}, nil
}

// UpdateTransaction updates allowed fields (notes, customer_name) of a transaction
func (s *TransactionService) UpdateTransaction(id uint, merchantID uint, updates map[string]interface{}) error {
	// Only allow updating specific fields
	allowedFields := map[string]bool{
		"notes":         true,
		"customer_name": true,
	}

	filteredUpdates := make(map[string]interface{})
	for key, value := range updates {
		if allowedFields[key] {
			filteredUpdates[key] = value
		}
	}

	result := s.DB.Model(&models.Transaction{}).
		Where("id = ? AND merchant_id = ?", id, merchantID).
		Updates(filteredUpdates)

	if result.Error != nil {
		return result.Error
	}

	if result.RowsAffected == 0 {
		return gorm.ErrRecordNotFound
	}

	return nil
}

// CancelTransaction cancels a transaction and restores product stock
func (s *TransactionService) CancelTransaction(id uint, merchantID uint) error {
	// Start transaction
	tx := s.DB.Begin()
	defer func() {
		if r := recover(); r != nil {
			tx.Rollback()
		}
	}()

	// Get transaction with items
	var transaction models.Transaction
	if err := tx.Where("id = ? AND merchant_id = ?", id, merchantID).
		Preload("Items").
		First(&transaction).Error; err != nil {
		tx.Rollback()
		return err
	}

	// Check if already cancelled
	if transaction.Status == "cancelled" {
		tx.Rollback()
		return gorm.ErrInvalidData
	}

	// Restore stock for each item
	for _, item := range transaction.Items {
		if err := tx.Model(&models.Product{}).
			Where("id = ?", item.ProductID).
			Update("stock", gorm.Expr("stock + ?", item.Quantity)).Error; err != nil {
			tx.Rollback()
			return err
		}
	}

	// Update transaction status
	if err := tx.Model(&transaction).
		Update("status", "cancelled").Error; err != nil {
		tx.Rollback()
		return err
	}

	return tx.Commit().Error
}
