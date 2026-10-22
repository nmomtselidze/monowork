package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestLoadDotEnv(t *testing.T) {
	const (
		plainKey    = "HARNESS_TEST_DOTENV_PLAIN"
		quotedKey   = "HARNESS_TEST_DOTENV_QUOTED"
		exportKey   = "HARNESS_TEST_DOTENV_EXPORT"
		existingKey = "HARNESS_TEST_DOTENV_EXISTING"
	)
	for _, key := range []string{plainKey, quotedKey, exportKey, existingKey} {
		unsetEnvForTest(t, key)
	}
	t.Setenv(existingKey, "from environment")

	path := filepath.Join(t.TempDir(), ".env")
	content := strings.Join([]string{
		"# comments are ignored",
		"",
		plainKey + "=plain value # inline comment",
		quotedKey + "=\"quoted value\"",
		"export " + exportKey + "='exported value'",
		existingKey + "=from file",
	}, "\n")
	if err := os.WriteFile(path, []byte(content), 0o600); err != nil {
		t.Fatal(err)
	}

	if err := loadDotEnv(path); err != nil {
		t.Fatalf("loadDotEnv() error = %v", err)
	}

	for key, want := range map[string]string{
		plainKey:    "plain value",
		quotedKey:   "quoted value",
		exportKey:   "exported value",
		existingKey: "from environment",
	} {
		if got := os.Getenv(key); got != want {
			t.Errorf("%s = %q, want %q", key, got, want)
		}
	}
}

func TestLoadDotEnvMissingFile(t *testing.T) {
	path := filepath.Join(t.TempDir(), "missing.env")

	if err := loadDotEnv(path); err != nil {
		t.Fatalf("loadDotEnv() error = %v, want nil for a missing file", err)
	}
}

func TestLoadDotEnvInvalidAssignments(t *testing.T) {
	tests := []struct {
		name    string
		content string
		wantErr string
	}{
		{
			name:    "missing equals sign",
			content: "NOT_AN_ASSIGNMENT\n",
			wantErr: "invalid assignment on line 1",
		},
		{
			name:    "empty variable name",
			content: "=value\n",
			wantErr: "empty variable name on line 1",
		},
		{
			name:    "invalid escape in double-quoted value",
			content: "HARNESS_TEST_DOTENV_INVALID=\"\\q\"\n",
			wantErr: "invalid quoted value on line 1",
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			path := filepath.Join(t.TempDir(), ".env")
			if err := os.WriteFile(path, []byte(test.content), 0o600); err != nil {
				t.Fatal(err)
			}

			err := loadDotEnv(path)
			if err == nil || !strings.Contains(err.Error(), test.wantErr) {
				t.Fatalf("loadDotEnv() error = %v, want an error containing %q", err, test.wantErr)
			}
		})
	}
}

func unsetEnvForTest(t *testing.T, key string) {
	t.Helper()

	value, wasSet := os.LookupEnv(key)
	if err := os.Unsetenv(key); err != nil {
		t.Fatalf("unset %s: %v", key, err)
	}
	t.Cleanup(func() {
		var err error
		if wasSet {
			err = os.Setenv(key, value)
		} else {
			err = os.Unsetenv(key)
		}
		if err != nil {
			t.Errorf("restore %s: %v", key, err)
		}
	})
}
