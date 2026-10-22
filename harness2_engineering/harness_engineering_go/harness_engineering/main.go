package main

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"time"
)

const (
	apiEndpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
	prompt      = "Hello! Can you introduce yourself?"
)

type generateContentRequest struct {
	Contents []content `json:"contents"`
}

type content struct {
	Parts []part `json:"parts"`
}

type part struct {
	Text string `json:"text"`
}

type generateContentResponse struct {
	Candidates []struct {
		Content content `json:"content"`
	} `json:"candidates"`
}

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, "Error:", err)
		os.Exit(1)
	}
}

func run() error {
	if err := loadDotEnv(".env"); err != nil {
		return fmt.Errorf("load .env: %w", err)
	}

	apiKey := os.Getenv("GEMINI_API_KEY")
	if apiKey == "" {
		return errors.New("GEMINI_API_KEY is not set; add it to .env or your environment")
	}

	body, err := json.Marshal(generateContentRequest{
		Contents: []content{{Parts: []part{{Text: prompt}}}},
	})
	if err != nil {
		return fmt.Errorf("encode request: %w", err)
	}

	requestURL, err := url.Parse(apiEndpoint)
	if err != nil {
		return fmt.Errorf("parse Gemini API URL: %w", err)
	}
	query := requestURL.Query()
	query.Set("key", apiKey)
	requestURL.RawQuery = query.Encode()

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	req, err := http.NewRequestWithContext(ctx, http.MethodPost, requestURL.String(), bytes.NewReader(body))
	if err != nil {
		return fmt.Errorf("create Gemini request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("send Gemini request: %w", err)
	}
	defer resp.Body.Close()

	responseBody, err := io.ReadAll(io.LimitReader(resp.Body, 1<<20))
	if err != nil {
		return fmt.Errorf("read Gemini response: %w", err)
	}
	if resp.StatusCode < http.StatusOK || resp.StatusCode >= http.StatusMultipleChoices {
		return fmt.Errorf("Gemini API returned %s: %s", resp.Status, strings.TrimSpace(string(responseBody)))
	}

	var result generateContentResponse
	if err := json.Unmarshal(responseBody, &result); err != nil {
		return fmt.Errorf("decode Gemini response: %w", err)
	}
	for _, candidate := range result.Candidates {
		for _, responsePart := range candidate.Content.Parts {
			if responsePart.Text != "" {
				fmt.Println("Gemini Response:", responsePart.Text)
				return nil
			}
		}
	}

	fmt.Println("No text response received")
	return nil
}

func loadDotEnv(path string) error {
	data, err := os.ReadFile(path)
	if errors.Is(err, os.ErrNotExist) {
		return nil
	}
	if err != nil {
		return err
	}

	for lineNumber, line := range strings.Split(string(data), "\n") {
		line = strings.TrimSpace(line)
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		line = strings.TrimPrefix(line, "export ")
		key, value, found := strings.Cut(line, "=")
		if !found {
			return fmt.Errorf("invalid assignment on line %d", lineNumber+1)
		}
		key = strings.TrimSpace(key)
		value = strings.TrimSpace(value)
		if key == "" {
			return fmt.Errorf("empty variable name on line %d", lineNumber+1)
		}
		if len(value) >= 2 && (value[0] == '"' && value[len(value)-1] == '"' || value[0] == '\'' && value[len(value)-1] == '\'') {
			if value[0] == '"' {
				unquoted, err := strconv.Unquote(value)
				if err != nil {
					return fmt.Errorf("invalid quoted value on line %d: %w", lineNumber+1, err)
				}
				value = unquoted
			} else {
				value = value[1 : len(value)-1]
			}
		} else if comment := strings.Index(value, " #"); comment >= 0 {
			value = strings.TrimSpace(value[:comment])
		}
		if _, exists := os.LookupEnv(key); !exists {
			if err := os.Setenv(key, value); err != nil {
				return fmt.Errorf("set %s from .env: %w", key, err)
			}
		}
	}
	return nil
}
