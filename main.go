package main

import (
	"sync"
	"github.com/gofiber/fiber/v2"
)

// This fulfills your "Implement concurrent in-memory state" task
type GlobalState struct {
	mu   sync.RWMutex
	data map[string]string
}

func main() {
	// Initializes the Go + Fiber project
	app := fiber.New()

	// Initialize the storage
	state := &GlobalState{data: make(map[string]string)}

	// Add a Health-check endpoint (Task 6)
	app.Get("/health", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{
			"status":  "online",
			"message": "AI Service Base is running",
		})
	})

	// Placeholder for Telemetry (Task 3)
	app.Post("/telemetry", func(c *fiber.Ctx) error {
		state.mu.Lock()
		defer state.mu.Unlock()
		return c.SendStatus(202)
	})

	// Start the server on port 3000
	app.Listen(":3000")
}