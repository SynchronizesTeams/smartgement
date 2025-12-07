package utils

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"time"
)

type RecaptchaResponse struct {
	Success     bool     `json:"success"`
	ChallengeTS string   `json:"challenge_ts"`
	Hostname    string   `json:"hostname"`
	ErrorCodes  []string `json:"error-codes"`
}

// VerifyRecaptcha verifies the reCAPTCHA token with Google's API
func VerifyRecaptcha(token string) (bool, error) {
	secret := os.Getenv("RECAPTCHA_SECRET")
	if secret == "" {
		return false, fmt.Errorf("RECAPTCHA_SECRET not configured")
	}

	if token == "" {
		return false, fmt.Errorf("recaptcha token is empty")
	}

	// Prepare request to Google reCAPTCHA API
	data := url.Values{}
	data.Set("secret", secret)
	data.Set("response", token)

	client := &http.Client{
		Timeout: 10 * time.Second,
	}

	resp, err := client.PostForm("https://www.google.com/recaptcha/api/siteverify", data)
	if err != nil {
		return false, fmt.Errorf("failed to verify recaptcha: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return false, fmt.Errorf("failed to read recaptcha response: %v", err)
	}

	var recaptchaResp RecaptchaResponse
	if err := json.Unmarshal(body, &recaptchaResp); err != nil {
		return false, fmt.Errorf("failed to parse recaptcha response: %v", err)
	}

	if !recaptchaResp.Success {
		return false, fmt.Errorf("recaptcha verification failed: %v", recaptchaResp.ErrorCodes)
	}

	return true, nil
}
