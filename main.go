package main

import (
	"fmt"
	"sync"

	"github.com/gofiber/fiber/v2"
)

// GlobalState handles the "Implement concurrent in-memory state" task.
// sync.RWMutex prevents data corruption in a distributed environment.
type GlobalState struct {
	mu   sync.RWMutex
	data map[string]string
}

func main() {
	// 1. Initialize Go + Fiber project
	app := fiber.New()

	// Initialize the storage
	state := &GlobalState{data: make(map[string]string)}

	// 2. Add Health-check endpoint
	// Test: http://localhost:3000/health
	app.Get("/health", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{
			"status":  "online",
			"service": "AI-Service-Base",
		})
	})

	// 3. Implement Telemetry + Threshold Detection + Central Integration
	app.Post("/telemetry", func(c *fiber.Ctx) error {
		type TelemetryData struct {
			SensorID string  `json:"sensor_id"`
			Value    float64 `json:"value"`
		}

		input := new(TelemetryData)
		if err := c.BodyParser(input); err != nil {
			return c.Status(400).SendString("Invalid data format")
		}

		// Save to concurrent state
		state.mu.Lock()
		state.data[input.SensorID] = fmt.Sprintf("%.2f", input.Value)
		state.mu.Unlock()

		// --- THRESHOLD DETECTION LOGIC ---
		if input.Value > 50.0 {
			fmt.Printf("⚠️ ALERT: Sensor %s detected high value: %.2f\n", input.SensorID, input.Value)
			
			// --- REST CALL TO CENTRAL (Mock) ---
			// In a real scenario, you'd use the 'http' package here to POST to Central
			fmt.Printf("📡 Sending Alert for %s to Central Server...\n", input.SensorID)
		} else {
			fmt.Printf("✅ Info: Sensor %s value normal: %.2f\n", input.SensorID, input.Value)
		}

		return c.Status(201).JSON(fiber.Map{
			"status": "processed",
			"sensor": input.SensorID,
		})
	})

	// 4. Start the server
	fmt.Println("Digital-Twin AI Service starting on http://localhost:3000")
	app.Listen(":3000")
}