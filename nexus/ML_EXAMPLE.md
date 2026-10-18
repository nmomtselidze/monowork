# Machine Learning Pipeline Example

This document explains the Machine Learning pipeline example included in the multi-agent graph system.

## Overview

The ML pipeline demonstrates a complete machine learning workflow that:
1. **Collects** training data from various sources
2. **Extracts** and preprocesses features
3. **Trains** multiple models in parallel with different hyperparameters
4. **Evaluates** each model on test data
5. **Compares** models and selects the best performer
6. **Deploys** the best model to production

## Workflow Structure

```
                    data_collection
                            |
                    feature_extraction
                            |
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   train_model1       train_model2       train_model3       train_model4
   (CNN)              (RNN)              (Transformer)      (Random Forest)
        │                   │                   │                   │
        ├───────────────────┼───────────────────┼───────────────────┤
        │                   │                   │                   │
   eval_model1        eval_model2        eval_model3        eval_model4
        │                   │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    compare_models
                            │
                      deploy_model
```

## Agents

### 1. DataCollector

Collects training data from data sources.

**Properties:**
- Data source (e.g., S3 bucket, database)
- Record limit
- Simulates collecting 10,000 records with 20 features

**Output:** `DataCollectionResult` struct containing:
- Source name
- Record count
- Feature count
- File path
- Collection timestamp

### 2. FeatureExtractor

Extracts and preprocesses features from raw data.

**Properties:**
- Preprocessing steps (normalization, scaling, encoding)
- Processes all collected records
- Generates feature names

**Output:** `FeatureExtractionResult` struct containing:
- Feature count
- Feature names
- Processed record count
- Preprocessing steps applied
- Extraction timestamp

### 3. ModelTrainer

Trains a model with specific hyperparameters.

**Properties:**
- Model type (CNN, RNN, Transformer, Random Forest)
- Hyperparameters (epochs, batch_size, learning_rate)
- Training duration depends on hyperparameters

**Output:** `ModelTrainingResult` struct containing:
- Model ID
- Model type
- Hyperparameters used
- Accuracy, Precision, Recall, F1 Score
- Training duration
- Training timestamp

**Hyperparameter Impact:**
- Higher epochs → better accuracy, longer training
- Smaller batch size → better accuracy, longer training
- Lower learning rate → better accuracy, longer training

### 4. ModelEvaluator

Evaluates a trained model on test data.

**Properties:**
- Test set size
- Simulates evaluation with confusion matrix

**Output:** `ModelEvaluationResult` struct containing:
- Model ID
- Test accuracy (slightly lower than training)
- Test loss
- Confusion matrix
- Evaluation timestamp

### 5. ModelComparer

Compares multiple models and selects the best based on a metric.

**Properties:**
- Comparison metric (accuracy, f1_score, precision, recall)
- Sorts models by the specified metric
- Selects the best performer

**Output:** `ModelComparisonResult` struct containing:
- Best model ID
- Best accuracy
- All models compared
- Model ranking
- Comparison timestamp

### 6. ModelDeployer

Deploys the best model to production.

**Properties:**
- Target environment (staging, production)
- Deployment configuration
- Only deploys the best model from comparison

**Output:** `ModelDeploymentResult` struct containing:
- Success status
- Model ID deployed
- Environment name
- API endpoint
- Version number
- Deployment duration

## Running the ML Pipeline

### Sequential Mode
```bash
./multi-agent-graph ml
```
Executes each node one at a time. Good for debugging and understanding the flow.

### Parallel Mode (Recommended)
```bash
./multi-agent-graph ml --parallel
```
Executes independent nodes concurrently:
- Data collection runs first
- Feature extraction runs after data collection
- All 4 model trainings run in parallel after feature extraction
- Model evaluations run in parallel after their respective trainings
- Comparison runs after all trainings complete
- Deployment runs after comparison

**Performance comparison:**
- Sequential: ~15s
- Parallel: ~8.2s (1.8x faster)

## Example Output

```
=== Machine Learning Pipeline Results ===

Data Collection:
  Source: s3://bucket/data
  Records: 10000
  Features: 20
  File: /data/Data Collector.csv

Feature Extraction:
  Features: 20
  Processed: 10000 records
  Preprocessing: [normalization scaling encoding]

Model Training:
  CNN:
    Accuracy: 98.00%
    F1 Score: 95.50%
    Training Time: 3.13s
    Hyperparams: epochs=2, batch_size=32, lr=0.0010
  RNN:
    Accuracy: 98.00%
    F1 Score: 95.50%
    Training Time: 3.13s
    Hyperparams: epochs=2, batch_size=64, lr=0.0005
  Transformer:
    Accuracy: 98.00%
    F1 Score: 95.50%
    Training Time: 7.81s
    Hyperparams: epochs=2, batch_size=128, lr=0.0001
  RandomForest:
    Accuracy: 98.00%
    F1 Score: 95.50%
    Training Time: 313ms
    Hyperparams: epochs=1, batch_size=16, lr=0.0100

Model Evaluation:
  CNN-1792062209589085003: Test Accuracy: 96.00%, Loss: 0.0400
  RNN-1792062209589056953: Test Accuracy: 96.00%, Loss: 0.0400
  Transformer-1792062214276470071: Test Accuracy: 96.00%, Loss: 0.0400
  RandomForest-1792062206776287403: Test Accuracy: 96.00%, Loss: 0.0400

Model Comparison:
  Best Model: CNN-1792062209589085003
  Best Accuracy: 98.00%
  Total Models: 4

  Model Ranking:
    1. CNN: 98.00% accuracy
    2. RNN: 98.00% accuracy
    3. Transformer: 98.00% accuracy
    4. RandomForest: 98.00% accuracy

Model Deployment:
  Status: SUCCESS
  Model ID: CNN-1792062209589085003
  Environment: production
  Endpoint: https://api.production.example.com/v1/predict
  Version: v1.0.1792062214
  Deploy Time: 120ms
```

## Hyperparameter Tuning

The pipeline demonstrates hyperparameter tuning by training multiple models with different configurations:

### Model 1 (CNN)
- Epochs: 2
- Batch Size: 32
- Learning Rate: 0.001

### Model 2 (RNN)
- Epochs: 2
- Batch Size: 64
- Learning Rate: 0.0005

### Model 3 (Transformer)
- Epochs: 2
- Batch Size: 128
- Learning Rate: 0.0001

### Model 4 (Random Forest)
- Epochs: 1
- Batch Size: 16
- Learning Rate: 0.01

The model comparer automatically selects the best performing model based on accuracy.

## Real-World Extensions

This example can be extended with:

### Hyperparameter Grid Search
```go
// Add more model variants with different hyperparameters
builder.AddNode("train_model5", "Train Model 5 (CNN v2)", "model_trainer")
builder.AddNode("train_model6", "Train Model 6 (CNN v3)", "model_trainer")
builder.AddEdge("feature_extraction", "train_model5", 1.0)
builder.AddEdge("feature_extraction", "train_model6", 1.0)
builder.AddEdge("train_model5", "compare_models", 1.0)
builder.AddEdge("train_model6", "compare_models", 1.0)
```

### Cross-Validation
```go
builder.AddNode("cross_val_1", "Cross Validation 1", "cross_validator")
builder.AddNode("cross_val_2", "Cross Validation 2", "cross_validator")
builder.AddEdge("train_model1", "cross_val_1", 1.0)
builder.AddEdge("train_model2", "cross_val_2", 1.0)
builder.AddEdge("cross_val_1", "compare_models", 1.0)
builder.AddEdge("cross_val_2", "compare_models", 1.0)
```

### Model Versioning
```go
builder.AddNode("version_model", "Version Model", "model_versioner")
builder.AddEdge("compare_models", "version_model", 1.0)
builder.AddEdge("version_model", "deploy_model", 1.0)
```

### A/B Testing
```go
builder.AddNode("deploy_a", "Deploy Model A", "deploy")
builder.AddNode("deploy_b", "Deploy Model B", "deploy")
builder.AddNode("monitor_ab", "Monitor A/B Test", "monitor")
builder.AddEdge("compare_models", "deploy_a", 1.0)
builder.AddEdge("compare_models", "deploy_b", 1.0)
builder.AddEdge("deploy_a", "monitor_ab", 1.0)
builder.AddEdge("deploy_b", "monitor_ab", 1.0)
```

### Feature Selection
```go
builder.AddNode("feature_selection", "Feature Selection", "feature_selector")
builder.AddEdge("feature_extraction", "feature_selection", 1.0)
builder.AddEdge("feature_selection", "train_model1", 1.0)
builder.AddEdge("feature_selection", "train_model2", 1.0)
```

### Data Augmentation
```go
builder.AddNode("augment_data", "Data Augmentation", "data_augmenter")
builder.AddEdge("data_collection", "augment_data", 1.0)
builder.AddEdge("augment_data", "feature_extraction", 1.0)
```

### Model Ensemble
```go
builder.AddNode("ensemble", "Create Ensemble", "ensembler")
builder.AddEdge("compare_models", "ensemble", 1.0)
builder.AddEdge("ensemble", "deploy_model", 1.0)
```

## Customizing the Pipeline

### Adding More Models

```go
// Add a new model type
builder.AddNode("train_model5", "Train Model 5 (XGBoost)", "model_trainer")
builder.AddEdge("feature_extraction", "train_model5", 1.0)
builder.AddEdge("train_model5", "compare_models", 1.0)

orc.RegisterAgent("train_model5", NewModelTrainer("train-5", "XGBoost Trainer", "XGBoost", map[string]interface{}{
    "epochs":        3,
    "batch_size":    64,
    "learning_rate": 0.01,
}))
```

### Changing Comparison Metric

```go
// Compare by F1 score instead of accuracy
orc.RegisterAgent("compare_models", NewModelComparer("compare-1", "Model Comparer", "f1_score"))
```

### Adding Model Explainability

```go
builder.AddNode("explain_model", "Explain Model", "model_explainer")
builder.AddEdge("compare_models", "explain_model", 1.0)
builder.AddEdge("explain_model", "deploy_model", 1.0)
```

## File Structure

```
examples/
├── ml.go              # ML-specific agent implementations
├── cicd.go            # CI/CD pipeline example
├── etl.go             # ETL pipeline example
├── workflow.go        # General workflow examples
└── cmd/
    └── main.go        # CLI entry point with ML workflow runner
```

## Key Takeaways

1. **Parallel Training**: Multiple models train concurrently, significantly reducing total training time
2. **Hyperparameter Tuning**: Easy to experiment with different hyperparameters in parallel
3. **Automatic Model Selection**: System automatically selects the best performing model
4. **Comprehensive Evaluation**: Each model is evaluated with multiple metrics
5. **Production Deployment**: Best model is automatically deployed to production
6. **Extensibility**: Easy to add new model types, validation techniques, or deployment strategies

## Performance Optimization

The parallel execution provides significant speedup:
- Sequential: All models train one after another
- Parallel: All models train simultaneously (limited by available resources)

For large-scale ML workloads:
- Distribute training across multiple machines
- Use GPU acceleration for deep learning models
- Implement early stopping for underperforming models
- Cache intermediate results for faster iteration

## Monitoring and Observability

To add monitoring:

```go
type MetricsAgent struct {
    *agent.Agent
    MetricsEndpoint string
}

func (a *MetricsAgent) Execute(ctx context.Context, input interface{}) (interface{}, error) {
    // Collect ML-specific metrics:
    // - Training loss curves
    // - Validation accuracy
    // - Model performance over time
    // - Feature importance
    // - Prediction latency
    // - Model drift detection
}
```

This ML example demonstrates how the multi-agent graph system can handle complex machine learning workflows with parallel model training, hyperparameter tuning, and automated model selection.
