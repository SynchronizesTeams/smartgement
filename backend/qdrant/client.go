package qdrant

import (
	"log"
	"os"
)

type QdrantClient struct {
	URL string
}

var Client *QdrantClient

// InitQdrant initializes the Qdrant client (placeholder implementation)
func InitQdrant() {
	qdrantURL := os.Getenv("QDRANT_URL")
	if qdrantURL == "" {
		qdrantURL = "http://localhost:6333"
	}

	Client = &QdrantClient{
		URL: qdrantURL,
	}

	log.Printf("Qdrant client initialized (placeholder) at: %s\n", qdrantURL)
}

// GetClient returns the Qdrant client instance
func GetClient() *QdrantClient {
	return Client
}

// Ping placeholder method to check connectivity
func (q *QdrantClient) Ping() error {
	// TODO: Implement actual Qdrant API ping
	log.Println("Qdrant ping (placeholder)")
	return nil
}
