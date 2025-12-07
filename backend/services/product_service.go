package services

import (
	"backend/models"
	"errors"

	"gorm.io/gorm"
)

type ProductService struct {
	db *gorm.DB
}

func NewProductService(db *gorm.DB) *ProductService {
	return &ProductService{db: db}
}

func (s *ProductService) GetAllProducts(merchantID uint) ([]models.Product, error) {
	var products []models.Product
	err := s.db.Where("merchant_id = ?", merchantID).Find(&products).Error
	return products, err
}

func (s *ProductService) GetProductByID(id uint, merchantID uint) (*models.Product, error) {
	var product models.Product
	err := s.db.Where("id = ? AND merchant_id = ?", id, merchantID).First(&product).Error
	if err != nil {
		return nil, err
	}
	return &product, nil
}

func (s *ProductService) CreateProduct(product *models.Product) error {
	return s.db.Create(product).Error
}

func (s *ProductService) UpdateProduct(id uint, merchantID uint, updates *models.Product) error {
	result := s.db.Model(&models.Product{}).
		Where("id = ? AND merchant_id = ?", id, merchantID).
		Updates(updates)

	if result.Error != nil {
		return result.Error
	}
	if result.RowsAffected == 0 {
		return errors.New("product not found or unauthorized")
	}
	return nil
}

func (s *ProductService) DeleteProduct(id uint, merchantID uint) error {
	result := s.db.Where("id = ? AND merchant_id = ?", id, merchantID).Delete(&models.Product{})
	if result.Error != nil {
		return result.Error
	}
	if result.RowsAffected == 0 {
		return errors.New("product not found or unauthorized")
	}
	return nil
}
