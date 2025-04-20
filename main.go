package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"
)

type DiscordMessage struct {
	Content string `json:"content"`
}

func updatePackageList() error {
	cmd := exec.Command("apt", "update")
	cmd.Stdout = nil
	cmd.Stderr = nil
	return cmd.Run()
}

func checkForUpdates() ([]string, error) {
	cmd := exec.Command("apt", "list", "--upgradable")
	var out bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = nil

	if err := cmd.Run(); err != nil {
		return nil, fmt.Errorf("failed to check updates: %v", err)
	}

	var updates []string
	for _, line := range strings.Split(out.String(), "\n") {
		if strings.HasPrefix(line, "Listing...") {
			continue
		}
		if line = strings.TrimSpace(line); line != "" {
			updates = append(updates, line)
		}
	}

	return updates, nil
}

func sendDiscordMessage(updates []string, webhookURL string) error {
	hostname, err := os.Hostname()
	if err != nil {
		return fmt.Errorf("failed to get hostname: %v", err)
	}

	timestamp := time.Now().Format("2006-01-02 15:04:05")
	message := fmt.Sprintf("🔄 Available Updates on **%s** at %s\n", hostname, timestamp)
	message += fmt.Sprintf("Found %d package(s) to update:\n", len(updates))
	message += fmt.Sprintf("```\n%s```", strings.Join(updates, "\n"))

	payload := DiscordMessage{Content: message}
	jsonData, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("failed to marshal JSON: %v", err)
	}

	resp, err := http.Post(webhookURL, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return fmt.Errorf("failed to send Discord message: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusNoContent && resp.StatusCode != http.StatusOK {
		return fmt.Errorf("Discord API returned status: %d", resp.StatusCode)
	}

	return nil
}

func getWebhookURL() (string, error) {
	var webhookURL string
	flag.StringVar(&webhookURL, "webhook", "", "Discord webhook URL")
	flag.Parse()

	if webhookURL == "" {
		webhookURL = os.Getenv("WEBHOOK")
	}

	if webhookURL == "" {
		return "", fmt.Errorf("webhook URL not provided. Use --webhook flag or set WEBHOOK environment variable")
	}

	return webhookURL, nil
}

func main() {
	log.SetFlags(log.Lshortfile)

	webhookURL, err := getWebhookURL()
	if err != nil {
		log.Fatal(err)
	}

	if err := updatePackageList(); err != nil {
		log.Fatal("Failed to update package list:", err)
	}

	updates, err := checkForUpdates()
	if err != nil {
		log.Fatal("Failed to check for updates:", err)
	}

	if len(updates) > 0 {
		if err := sendDiscordMessage(updates, webhookURL); err != nil {
			log.Fatal("Failed to send Discord message:", err)
		}
	}
} 