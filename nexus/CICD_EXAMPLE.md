# CI/CD Pipeline Example

This document explains the CI/CD (Continuous Integration/Continuous Deployment) pipeline example included in the multi-agent graph system.

## Overview

The CI/CD pipeline demonstrates a modern software delivery workflow that:
1. **Builds** the application
2. **Tests** on multiple platforms in parallel (Linux, Windows, macOS)
3. **Runs** integration tests
4. **Scans** for security vulnerabilities
5. **Lints** code for quality
6. **Deploys** to staging environment (conditional on test results)

## Workflow Structure

```
                    ┌─────────────┐
                    │    build    │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │ test_   │      │ test_   │      │ test_   │
   │ linux   │      │windows  │      │ macos   │
   └────┬────┘      └────┬────┘      └────┬────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │ test_     │     │security │      │  lint   │
   │integration│     │  scan   │      │         │
   └────┬────┘      └────┬────┘      └────┬────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼──────┐
                    │ deploy_     │
                    │ staging     │
                    └─────────────┘
```

## Agents

### 1. BuildAgent

Compiles and packages the application.

**Properties:**
- Project path
- Build configuration
- Generates artifact ID and binary path

**Output:** `BuildResult` struct containing:
- Success status
- Artifact ID
- Binary path
- Build duration
- Build timestamp

### 2. TestAgent

Runs tests on specific platforms.

**Properties:**
- Platform (Linux, Windows, macOS)
- Test type (unit, integration, e2e)
- Platform-specific test durations

**Output:** `TestResult` struct containing:
- Platform name
- Total tests count
- Passed/Failed/Skipped counts
- Code coverage percentage
- Success status
- Test duration

### 3. SecurityScanAgent

Scans for security vulnerabilities.

**Properties:**
- Scanner type (e.g., Snyk, SonarQube)
- Vulnerability severity levels

**Output:** `SecurityScanResult` struct containing:
- Success status
- Total vulnerabilities
- Critical/High/Medium/Low counts
- Scan duration

### 4. LintAgent

Performs code quality checks.

**Properties:**
- Linter type (e.g., golangci-lint, ESLint)
- Linting rules

**Output:** `LintResult` struct containing:
- Success status
- Issues found
- Warnings/Errors counts
- Lint duration

### 5. DeployAgent

Deploys the application to an environment.

**Properties:**
- Target environment (staging, production)
- Deployment configuration
- **Conditional deployment** - only deploys if all tests pass

**Output:** `DeployResult` struct containing:
- Success status
- Environment name
- Version number
- Deployment URL
- Deploy duration

## Running the CI/CD Pipeline

### Sequential Mode
```bash
./multi-agent-graph cicd
```
Executes each node one at a time. Good for debugging and understanding the flow.

### Parallel Mode (Recommended)
```bash
./multi-agent-graph cicd --parallel
```
Executes independent nodes concurrently:
- Build runs first
- All tests, security scan, and lint run in parallel after build
- Deploy runs after all checks complete

**Performance comparison:**
- Sequential: ~1.14s
- Parallel: ~540ms (2x faster)

## Example Output

```
=== CI/CD Pipeline Results ===

Build:
  Status: SUCCESS
  Artifact ID: artifact-1792061521
  Binary Path: /builds/Build Agent/app-binary
  Build Time: 201.036963ms

Test Results:
  linux: PASSED (100/100 passed, 85.5% coverage)
  windows: PASSED (100/100 passed, 85.5% coverage)
  macos: PASSED (100/100 passed, 85.5% coverage)
  linux: PASSED (100/100 passed, 85.5% coverage)
  Overall: ALL TESTS PASSED

Security Scan:
  Status: SUCCESS
  Vulnerabilities: 2 (Critical: 0, High: 1, Medium: 1, Low: 0)
  Scan Time: 121.02947ms

Lint:
  Status: SUCCESS
  Issues Found: 5 (Warnings: 3, Errors: 0)
  Lint Time: 80.404643ms

Deployment:
  Status: SUCCESS
  Environment: staging
  Version: v1.0.1792061521
  URL: https://staging.example.com
  Deploy Time: 100.271581ms
```

## Conditional Deployment

The pipeline implements conditional deployment logic:

```go
// Conditional deployment - only deploy if all tests pass
if !allTestsPassed {
    a.Agent.Status = "failed"
    a.Agent.CompletedAt = time.Now()
    return nil, fmt.Errorf("deployment skipped: tests failed")
}
```

If any test fails:
- Deployment is skipped
- Deploy agent status is set to "failed"
- Error message indicates deployment was skipped due to test failures
- Other checks (security scan, lint) still complete

## Real-World Extensions

This example can be extended with:

### Multiple Environments
```go
builder.AddNode("deploy_staging", "Deploy to Staging", "deploy")
builder.AddNode("deploy_production", "Deploy to Production", "deploy")
builder.AddEdge("deploy_staging", "deploy_production", 1.0)
```

### Manual Approval Gates
```go
builder.AddNode("approval", "Manual Approval", "approval")
builder.AddEdge("deploy_staging", "approval", 1.0)
builder.AddEdge("approval", "deploy_production", 1.0)
```

### Rollback on Failure
```go
builder.AddNode("rollback", "Rollback", "rollback")
builder.AddEdge("deploy_production", "rollback", 1.0)
```

### Notification Agents
```go
builder.AddNode("notify_slack", "Slack Notification", "notification")
builder.AddEdge("deploy_production", "notify_slack", 1.0)
```

### Performance Testing
```go
builder.AddNode("perf_test", "Performance Tests", "test")
builder.AddEdge("build", "perf_test", 1.0)
builder.AddEdge("perf_test", "deploy_staging", 1.0)
```

### Database Migrations
```go
builder.AddNode("migrate_db", "Database Migration", "migration")
builder.AddEdge("deploy_staging", "migrate_db", 1.0)
builder.AddEdge("migrate_db", "deploy_production", 1.0)
```

## Platform-Specific Testing

The example demonstrates testing on multiple platforms:

1. **Linux** - Most common for server applications
2. **Windows** - For Windows-specific applications
3. **macOS** - For cross-platform validation
4. **Integration Tests** - Full system testing

Each platform can have:
- Different test suites
- Different runtime configurations
- Platform-specific assertions

## Security Integration

The security scan agent can be configured with:
- **Snyk** - Vulnerability scanning
- **SonarQube** - Code quality and security
- **Trivy** - Container scanning
- **OWASP ZAP** - Web application scanning

Vulnerability severity levels:
- **Critical** - Immediate action required
- **High** - Fix as soon as possible
- **Medium** - Fix in next release
- **Low** - Fix when convenient

## Quality Gates

The pipeline implements quality gates:

1. **Build Gate** - Application must compile successfully
2. **Test Gate** - All tests must pass on all platforms
3. **Security Gate** - No critical vulnerabilities
4. **Lint Gate** - No linting errors
5. **Deployment Gate** - All previous gates must pass

## Monitoring and Metrics

To add monitoring:

```go
type MetricsAgent struct {
    *agent.Agent
    MetricsEndpoint string
}

func (a *MetricsAgent) Execute(ctx context.Context, input interface{}) (interface{}, error) {
    // Collect metrics from all previous steps
    // Send to monitoring system (Prometheus, Datadog, etc.)
    // Track:
    // - Build duration
    // - Test coverage
    // - Test failure rate
    // - Deployment frequency
    // - Lead time for changes
}
```

## Customizing the Pipeline

### Adding More Test Platforms

```go
builder.AddNode("test_android", "Android Tests", "test")
builder.AddNode("test_ios", "iOS Tests", "test")
builder.AddEdge("build", "test_android", 1.0)
builder.AddEdge("build", "test_ios", 1.0)
builder.AddEdge("test_android", "deploy_staging", 1.0)
builder.AddEdge("test_ios", "deploy_staging", 1.0)
```

### Adding Canary Deployment

```go
builder.AddNode("deploy_canary", "Deploy Canary", "deploy")
builder.AddNode("monitor_canary", "Monitor Canary", "monitor")
builder.AddEdge("deploy_staging", "deploy_canary", 1.0)
builder.AddEdge("deploy_canary", "monitor_canary", 1.0)
builder.AddEdge("monitor_canary", "deploy_production", 1.0)
```

### Adding Blue-Green Deployment

```go
builder.AddNode("deploy_blue", "Deploy Blue", "deploy")
builder.AddNode("deploy_green", "Deploy Green", "deploy")
builder.AddNode("switch_traffic", "Switch Traffic", "switch")
builder.AddEdge("deploy_staging", "deploy_blue", 1.0)
builder.AddEdge("deploy_staging", "deploy_green", 1.0)
builder.AddEdge("deploy_blue", "switch_traffic", 1.0)
builder.AddEdge("deploy_green", "switch_traffic", 1.0)
```

## File Structure

```
examples/
├── cicd.go             # CI/CD-specific agent implementations
├── etl.go              # ETL pipeline example
├── workflow.go         # General workflow examples
└── cmd/
    └── main.go         # CLI entry point with CI/CD workflow runner
```

## Key Takeaways

1. **Parallel Testing**: Tests run concurrently on different platforms, significantly reducing pipeline duration
2. **Conditional Deployment**: Deployment only happens if all quality gates pass
3. **Multi-Platform Support**: Easy to add support for additional platforms
4. **Security Integration**: Security scanning is integrated into the pipeline
5. **Quality Gates**: Multiple checkpoints ensure code quality before deployment
6. **Extensibility**: Easy to add new stages, notifications, or monitoring

This CI/CD example demonstrates how the multi-agent graph system can handle complex software delivery workflows with parallel execution, conditional logic, and quality gates.
