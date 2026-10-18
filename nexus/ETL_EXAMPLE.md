# ETL Pipeline Example

This document explains the ETL (Extract, Transform, Load) pipeline example included in the multi-agent graph system.

## Overview

The ETL pipeline demonstrates a real-world data processing workflow that:
1. **Extracts** data from 3 different databases in parallel
2. **Validates** each data source independently
3. **Merges** all validated data into a single dataset
4. **Loads** the merged data to a data warehouse

## Workflow Structure

```
                    ┌─────────────┐
                    │ db1_extract │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ db1_validate│
                    └──────┬──────┘
                           │
┌─────────────┐      ┌────▼────┐      ┌─────────────┐
│ db2_extract │      │  merge  │      │warehouse_load│
└──────┬──────┘      └────┬────┘      └─────────────┘
       │                  │
┌──────▼──────┐      ┌────▲────┐
│ db2_validate│      │ db3_validate│
└──────┬──────┘      └────┬────┘
       │                  │
┌──────▼──────┐      ┌────▼────┐
│ db3_extract │      │         │
└─────────────┘      └─────────┘
```

## Agents

### 1. DatabaseExtractor

Extracts data from a database connection.

**Properties:**
- Connection string (e.g., `postgres://db1`, `mysql://db2`, `mongodb://db3`)
- SQL query or database operation
- Simulates extracting 10 records per database

**Output:** `DatabaseData` struct containing:
- Source name
- Records (array of maps)
- Record count
- Extraction timestamp

### 2. DataValidator

Validates data integrity using configurable rules.

**Properties:**
- Validation rules (e.g., `has_id`, `has_name`)
- Checks each record against all rules
- Collects validation issues

**Output:** `ValidatedData` struct containing:
- Source name
- Valid records (filtered)
- Validation status
- List of issues found

### 3. DataMerger

Merges data from multiple validated sources.

**Properties:**
- Accepts multiple `ValidatedData` inputs
- Combines all records into single dataset
- Tracks source information

**Output:** `MergedData` struct containing:
- List of source names
- All merged records
- Total record count
- Merge timestamp

### 4. WarehouseLoader

Loads merged data to data warehouse in batches.

**Properties:**
- Warehouse URL (e.g., `snowflake://warehouse`)
- Batch size for loading
- Simulates batch loading with delays

**Output:** `WarehouseLoadResult` struct containing:
- Success status
- Row count loaded
- Load time duration
- Load timestamp

## Running the ETL Pipeline

### Sequential Mode
```bash
./multi-agent-graph etl
```
Executes each node one at a time in topological order. Good for debugging and understanding the flow.

### Parallel Mode (Recommended)
```bash
./multi-agent-graph etl --parallel
```
Executes independent nodes concurrently:
- All 3 database extractions run in parallel
- All 3 validations run in parallel after their extractions complete
- Merge and load run sequentially (they depend on all validations)

**Performance comparison:**
- Sequential: ~733ms
- Parallel: ~347ms (2x faster)

## Example Output

```
=== ETL Pipeline Results ===

Database Extraction:
  DB1: 10 records from DB1
  DB2: 10 records from DB2
  DB3: 10 records from DB3

Validation:
  DB1: 10 valid records, 0 issues
  DB2: 10 valid records, 0 issues
  DB3: 10 valid records, 0 issues

Merge: 30 total records from 3 sources
  Sources: [DB1 DB2 DB3]

Warehouse Load: SUCCESS
  Rows loaded: 30
  Load time: 50.145225ms
```

## Real-World Extensions

This example can be extended with:

### Error Handling
- Retry logic for failed database connections
- Dead letter queue for invalid records
- Circuit breakers for failing sources

### Data Quality
- Schema validation
- Data type checking
- Business rule validation
- Data profiling

### Performance
- Connection pooling
- Batch processing configuration
- Streaming for large datasets
- Incremental loading

### Monitoring
- Metrics collection (records per second, error rates)
- Logging to external systems
- Alerting on failures
- Progress tracking

### Additional Features
- Data transformation (type conversion, normalization)
- Data enrichment (lookup tables, API calls)
- Data masking (PII protection)
- Partitioning strategy

## Customizing the Pipeline

### Adding More Data Sources

```go
builder.AddNode("db4_extract", "Database 4 Extract", "database_extractor")
builder.AddNode("db4_validate", "Database 4 Validate", "data_validator")
builder.AddEdge("db4_extract", "db4_validate", 1.0)
builder.AddEdge("db4_validate", "merge", 1.0)

orc.RegisterAgent("db4_extract", NewDatabaseExtractor("extract-4", "DB4", "oracle://db4", "SELECT * FROM products"))
orc.RegisterAgent("db4_validate", NewDataValidator("validate-4", "Validator 4"))
```

### Adding Transformation Steps

```go
builder.AddNode("transform", "Transform Data", "data_transformer")
builder.AddEdge("merge", "transform", 1.0)
builder.AddEdge("transform", "warehouse_load", 1.0)
```

### Adding Conditional Branches

```go
builder.AddNode("quality_check", "Quality Check", "quality_checker")
builder.AddEdge("merge", "quality_check", 1.0)

// Only load if quality passes
builder.AddEdge("quality_check", "warehouse_load", 1.0)
```

## File Structure

```
examples/
├── etl.go              # ETL-specific agent implementations
├── workflow.go         # General workflow examples
└── cmd/
    └── main.go         # CLI entry point with ETL workflow runner
```

## Key Takeaways

1. **Parallel Execution**: The graph automatically identifies which nodes can run in parallel (the 3 database extractions and validations)
2. **Dependency Management**: The merge node waits for all 3 validations to complete before executing
3. **Type Safety**: Each agent has strongly-typed input/output for compile-time safety
4. **Extensibility**: Easy to add new data sources, validation rules, or transformation steps
5. **Monitoring**: Each node tracks status, duration, and results independently

This ETL example demonstrates how the multi-agent graph system can handle real-world data processing workflows with complex dependencies and parallel execution.
