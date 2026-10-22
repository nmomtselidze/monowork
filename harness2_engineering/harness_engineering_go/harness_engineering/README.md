# Harness Engineering Go

A Go command-line application that sends a prompt to Google's Gemini API.

## Setup

Copy `.env.example` to `.env` and add your API key, or set
`GEMINI_API_KEY` in the environment:

```bash
cp .env.example .env
# Edit .env and set GEMINI_API_KEY
```

## Build, test, and run

```bash
go build .
go test ./...
go vet ./...
go run .
```

The app calls Gemini 2.5 Flash and uses Go's standard library only. It reads
`.env` without overriding environment variables already set in the process.
========================================================================
source ~/.bashrc
go run .
===R E S P O N S===
Gemini Response: Hello! I'd be happy to.

I am a large language model, trained by Google.

My purpose is to assist users like you by providing information, answering questions, generating creative content, and engaging in helpful and informative conversations across a wide range of topics. I don't have personal experiences, feelings, or a physical form, but I'm here to help you in many ways!

What can I do for you today, or what would you like to chat about?
----------------------------------------------------------------
source ~/.bashrc
go test .
===R E S P O N S===
ok  	harness_engineering_go	0.005s
----------------------------------------------------------------
source ~/.bashrc
cd /media/user/dsk64/monowork/nexus/
go test ./...
===R E S P O N S===
ok  	multi-agent-graph/agent	0.279s
ok  	multi-agent-graph/examples	11.786s
?   	multi-agent-graph/examples/cmd	        [no test files]
?   	multi-agent-graph/examples/cmd/bgs	    [no test files]
?   	multi-agent-graph/examples/cmd/bpa	    [no test files]
?   	multi-agent-graph/examples/cmd/ms	    [no test files]
?   	multi-agent-graph/examples/cmd/stream	[no test files]
ok  	multi-agent-graph/graph	0.004s
ok  	multi-agent-graph/orchestrator	0.475s

