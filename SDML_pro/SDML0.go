package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

// HuggingFaceAPIRequest represents the request structure for HF Inference API
type HuggingFaceAPIRequest struct {
	Inputs     string                 `json:"inputs"`
	Parameters map[string]interface{} `json:"parameters,omitempty"`
}

// HuggingFaceAPIResponse represents the response from HF Inference API
type HuggingFaceAPIResponse []struct {
	GeneratedText string `json:"generated_text"`
}

// Message represents a chat message
type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

func main() {
	// Open output file
	outputFile, err := os.Create("SDML0_output.txt")
	if err != nil {
		fmt.Printf("Error creating output file: %v\n", err)
		return
	}
	defer outputFile.Close()

	// Model configuration
	modelID := "HuggingFaceTB/SmolLM2-1.7B-Instruct"
	apiURL := fmt.Sprintf("https://api-inference.huggingface.co/models/%s", modelID)

	// Symptom prompt
	symptoms := "I have a high fever, dry cough, and severe fatigue."
	messages := []Message{
		{Role: "system", Content: "You are a medical AI assistant. Analyze the symptoms and identify the single most likely condition with the highest probability."},
		{Role: "user", Content: symptoms},
	}

	// Create prompt with chat template
	prompt := formatChatTemplate(messages)

	// Prepare request
	requestBody := HuggingFaceAPIRequest{
		Inputs: prompt,
		Parameters: map[string]interface{}{
			"max_new_tokens": 200,
			"temperature":    0.2,
			"do_sample":      true,
		},
	}

	// Convert to JSON
	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf("Error marshaling JSON: %v\n", err)
		outputFile.WriteString(fmt.Sprintf("Error marshaling JSON: %v\n", err))
		return
	}

	// Create HTTP request with timeout
	client := &http.Client{
		Timeout: 60 * time.Second,
	}

	req, err := http.NewRequest("POST", apiURL, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf("Error creating request: %v\n", err)
		outputFile.WriteString(fmt.Sprintf("Error creating request: %v\n", err))
		return
	}

	req.Header.Set("Content-Type", "application/json")
	// Note: You may need to set HF_TOKEN environment variable for authentication
	// req.Header.Set("Authorization", "Bearer YOUR_HF_TOKEN")

	// Send request
	resp, err := client.Do(req)
	if err != nil {
		errorMsg := fmt.Sprintf("Error sending request: %v\n", err)
		fmt.Print(errorMsg)
		outputFile.WriteString(errorMsg)
		printFallbackResponse(symptoms, outputFile)
		return
	}
	defer resp.Body.Close()

	// Read response
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		errorMsg := fmt.Sprintf("Error reading response: %v\n", err)
		fmt.Print(errorMsg)
		outputFile.WriteString(errorMsg)
		printFallbackResponse(symptoms, outputFile)
		return
	}

	// Check status code
	if resp.StatusCode != http.StatusOK {
		errorMsg := fmt.Sprintf("API returned status %d: %s\n", resp.StatusCode, string(body))
		fmt.Print(errorMsg)
		outputFile.WriteString(errorMsg)
		printFallbackResponse(symptoms, outputFile)
		return
	}

	// Parse response
	var apiResponse HuggingFaceAPIResponse
	err = json.Unmarshal(body, &apiResponse)
	if err != nil {
		errorMsg := fmt.Sprintf("Error parsing response: %v\n", err)
		fmt.Print(errorMsg)
		outputFile.WriteString(errorMsg)
		printFallbackResponse(symptoms, outputFile)
		return
	}

	// Print generated text
	if len(apiResponse) > 0 {
		responseText := apiResponse[0].GeneratedText
		fmt.Println(responseText)
		outputFile.WriteString(responseText + "\n")
	} else {
		errorMsg := "No response generated\n"
		fmt.Print(errorMsg)
		outputFile.WriteString(errorMsg)
		printFallbackResponse(symptoms, outputFile)
	}

	fmt.Println("\nOutput saved to SDML0_output.txt")
}

// formatChatTemplate creates a chat template similar to tokenizer.apply_chat_template
func formatChatTemplate(messages []Message) string {
	var template string
	for _, msg := range messages {
		template += fmt.Sprintf("<|im_start|>%s\n%s<|im_end|>\n", msg.Role, msg.Content)
	}
	template += "<|im_start|>assistant\n"
	return template
}

// printFallbackResponse provides a mock response for demonstration
func printFallbackResponse(symptoms string, outputFile *os.File) {
	fallbackResponse := `

--- Demo Mode: Fallback Response ---
<|im_start|>system
You are a medical AI assistant. Analyze the symptoms and identify the single most likely condition with the highest probability.
<|im_end|>
<|im_start|>user
` + symptoms + `
<|im_end|>
<|im_start|>assistant
Based on the symptoms you've provided, the most likely condition is:

Influenza (Flu): This is a viral infection that causes symptoms like fever, cough, and fatigue. It's highly contagious and can spread quickly, especially during flu season. The combination of high fever, dry cough, and severe fatigue strongly suggests influenza as the primary diagnosis.

Please remember that this is just a potential condition and it's important to consult with a healthcare professional for a proper diagnosis.
`
	fmt.Print(fallbackResponse)
	outputFile.WriteString(fallbackResponse)
}
