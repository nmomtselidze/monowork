# Multi-Agent Graph System

A Go-based multi-agent workflow orchestration system using graph engineering with Directed Acyclic Graphs (DAGs).

## Overview

This project provides a framework for building and executing multi-agent workflows using graph-based orchestration. 
Agents are represented as nodes in a DAG, and the orchestrator manages their execution based on dependencies defined by edges.

## Features

- **Graph Engine**: Full DAG implementation with cycle detection and topological sorting
- **Agent Framework**: Extensible agent types with custom execution logic
- **Orchestrator**: Sequential and parallel workflow execution modes
- **Workflow Builder**: DSL for building complex workflows
- **Built-in Agent Types**: Data processors, transformers, validators, and aggregators
- **Example Workflows**: Linear, parallel, and complex workflow patterns

## Project Structure

```
multi-agent-graph/
├── graph/              # Graph engine implementation
│   ├── node.go        # Node representation
│   ├── edge.go        # Edge representation
│   └── dag.go         # DAG with cycle detection and topological sort
├── agent/             # Agent framework
│   ├── agent.go       # Base agent interface
│   ├── registry.go    # Agent type registry
│   └── examples.go    # Built-in agent implementations
├── orchestrator/      # Workflow orchestration
│   ├── orchestrator.go # Main orchestrator with execution logic
│   └── builder.go     # Workflow builder DSL
├── examples/          # Example workflows
│   ├── workflow.go    # Pre-built workflow examples
│   └── cmd/
│       └── main.go    # CLI entry point
└── README.md
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd multi-agent-graph

# Build the CLI
go build -o multi-agent-graph examples/cmd/main.go
```

## Usage

### Running Example Workflows

The project includes six example workflows:

1. **Linear Workflow**: Simple sequential processing
2. **Parallel Workflow**: Parallel branch processing with merge
3. **Complex Workflow**: Multi-source processing with complex dependencies
4. **ETL Pipeline**: Real-world ETL workflow extracting from 3 databases, validating, merging, and loading to warehouse
5. **CI/CD Pipeline**: Build, test on multiple platforms, lint, security scan, and deploy with conditional deployment
6. **ML Pipeline**: Data collection, feature extraction, parallel model training with hyperparameter tuning, model comparison, and deployment

```bash
# Run linear workflow (sequential)
./multi-agent-graph linear

# Run parallel workflow (parallel execution)
./multi-agent-graph parallel --parallel

# Run complex workflow (sequential)
./multi-agent-graph complex --parallel

# Run ETL pipeline (parallel mode for best performance)
./multi-agent-graph etl --parallel

# Run CI/CD pipeline (parallel mode for best performance)
./multi-agent-graph cicd --parallel

# Run ML pipeline (parallel mode for best performance)
./multi-agent-graph ml --parallel

# Run Flight_booking pipeline (parallel mode for best performance)
./multi-agent-graph book-flight --parallel
```

### CLI Options

```
Usage: ./multi-agent-graph <workflow-type> [--parallel]

Workflow Types:
  linear   - Simple linear workflow (validate -> process -> transform -> aggregate)
  parallel - Workflow with parallel branches
  complex  - Complex workflow with multiple dependencies

Options:
  --parallel - Execute workflow in parallel mode (where possible)
```

## API Usage

### Creating a Custom Workflow

```go
package main

import (
    "multi-agent-graph/agent"
    "multi-agent-graph/orchestrator"
)

func main() {
    // Build workflow using the builder
    builder := orchestrator.NewWorkflowBuilder()

    // Add nodes
    builder.AddNode("node1", "First Node", "data_processor")
    builder.AddNode("node2", "Second Node", "transform")
    builder.AddNode("node3", "Third Node", "aggregator")

    // Add edges (dependencies)
    builder.AddEdge("node1", "node2", 1.0)
    builder.AddEdge("node2", "node3", 1.0)

    // Validate workflow
    if err := builder.Validate(); err != nil {
        panic(err)
    }

    // Get DAG
    dag := builder.Build()

    // Create orchestrator
    orc := orchestrator.NewOrchestrator(dag)

    // Register agents
    orc.RegisterAgent("node1", agent.NewDataProcessorAgent("agent-1", "Processor 1"))
    orc.RegisterAgent("node2", agent.NewTransformAgent("agent-2", "Transformer"))
    orc.RegisterAgent("node3", agent.NewAggregatorAgent("agent-3", "Aggregator"))

    // Execute workflow
    input := map[string]interface{}{"data": "sample"}
    err := orc.Execute(input)
    if err != nil {
        panic(err)
    }

    // Get results
    results := orc.GetAllResults()
}
```

### Creating Custom Agents

```go
package main

import (
    "context"
    "multi-agent-graph/agent"
)

// CustomAgent implements custom processing logic
type CustomAgent struct {
    *agent.Agent
    CustomFunc func(interface{}) (interface{}, error)
}

func NewCustomAgent(id, name string) *CustomAgent {
    return &CustomAgent{
        Agent: agent.NewAgent(id, name, "custom"),
    }
}

func (a *CustomAgent) Execute(ctx context.Context, input interface{}) (interface{}, error) {
    a.Agent.Status = "running"
    a.Agent.StartedAt = time.Now()

    // Your custom logic here
    output, err := a.CustomFunc(input)
    if err != nil {
        a.Agent.Status = "failed"
        a.Agent.CompletedAt = time.Now()
        return nil, err
    }

    a.Agent.Status = "completed"
    a.Agent.CompletedAt = time.Now()
    return output, nil
}
```

## Core Components

### Graph Engine

The graph engine provides:

- **Nodes**: Represent tasks or agents with metadata
- **Edges**: Define dependencies between nodes with optional weights
- **Cycle Detection**: Ensures workflows remain acyclic
- **Topological Sort**: Determines execution order based on dependencies

Key methods:
- `AddNode(node)`: Add a node to the graph
- `AddEdge(from, to, weight)`: Add a directed edge
- `TopologicalSort()`: Get nodes in execution order
- `GetRootNodes()`: Get nodes with no dependencies
- `GetLeafNodes()`: Get nodes with no dependents

### Agent Framework

Agents are autonomous units that execute tasks:

- **DataProcessorAgent**: Processes and transforms data
- **TransformAgent**: Applies transformations to data
- **ValidationAgent**: Validates data integrity
- **AggregatorAgent**: Aggregates results from multiple sources

All agents support:
- Custom execution functions
- Status tracking (idle, running, completed, failed)
- Execution duration measurement
- Context-based cancellation

### Orchestrator

The orchestrator manages workflow execution:

- **Sequential Execution**: Executes nodes one at a time in topological order
- **Parallel Execution**: Executes independent nodes concurrently
- **Result Management**: Tracks results and errors for each node
- **Cancellation**: Supports context-based workflow cancellation

Key methods:
- `Execute(input)`: Execute workflow sequentially
- `ExecuteParallel(input)`: Execute workflow with parallelization
- `GetResult(nodeID)`: Get result for a specific node
- `GetStatus()`: Get status of all nodes
- `CancelExecution()`: Cancel running workflow

## Design Patterns

### DAG-Based Orchestration

Workflows are modeled as Directed Acyclic Graphs where:
- Nodes represent agents/tasks
- Edges represent dependencies
- Topological sort determines execution order
- Cycle detection prevents circular dependencies

### Agent Pattern

Each agent:
- Encapsulates specific processing logic
- Maintains its own state and metadata
- Can be independently tested and reused
- Supports custom execution functions

### Builder Pattern

The WorkflowBuilder provides a fluent interface for:
- Declarative workflow construction
- Validation before execution
- Separation of definition and execution

## Examples

### Linear Workflow

```
validate -> process -> transform -> aggregate
```

### Parallel Workflow

```
        -> branch1 ->
input  -> branch2 -> merge -> output
        -> branch3 ->
```

### Complex Workflow

```
data_source1 \                 / process1 -> transform1 \
             -> validate1 -> /                           -> merge -> final
data_source2 /                 \ process2 -> transform2 /
data_source3 -> validate2 -> /
```

### ETL Pipeline

```
db1_extract -> db1_validate \
                           -> merge -> warehouse_load
db2_extract -> db2_validate /
db3_extract -> db3_validate /
```

A real-world ETL workflow that:
- Extracts data from 3 different databases (PostgreSQL, MySQL, MongoDB)
- Validates each source independently (parallel)
- Merges all validated data
- Loads to data warehouse (Snowflake) in batches

### CI/CD Pipeline

```
        build
       /  |  \
      /   |   \
test_ test_ test_ test_ security lint
linux windows macos integration  scan
      \   |   /      |        |      |
       \  |  /       |        |      |
        deploy_staging
```

A modern CI/CD workflow that:
- Builds the application
- Runs tests on multiple platforms in parallel (Linux, Windows, macOS)
- Executes integration tests
- Scans for security vulnerabilities
- Lints code for quality
- Deploys to staging (conditional on all tests passing)

## Testing

```bash
# Run tests
go test ./...

# Run tests with coverage
go test -cover ./...
```

## Extending the System

### Adding New Agent Types

1. Create a new agent struct embedding `*agent.Agent`
2. Implement the `Execute(ctx, input)` method
3. Register the agent with the orchestrator
4. Add type handling in the orchestrator's `executeAgent` method

### Adding Graph Features

The graph engine can be extended with:
- Edge weights for priority-based execution
- Conditional edges for dynamic workflows
- Sub-graphs for modular workflows
- Graph visualization utilities

## Performance Considerations

- **Sequential Mode**: Simpler, predictable execution order
- **Parallel Mode**: Faster for independent nodes, but higher resource usage
- **Cycle Detection**: O(V + E) complexity using DFS
- **Topological Sort**: O(V + E) complexity using Kahn's algorithm

## License

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
