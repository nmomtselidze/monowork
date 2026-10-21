"""
Real Data Demonstration for Tensor ML Project
Shows how to use real sentiment data with the ML pipeline
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

import torch
from torch.utils.data import DataLoader
from text_classifier import TransformerClassifier, TextDataset, TensorTrainer
from model_evaluator import ModelEvaluator
from visualization import TensorVisualizer, TensorAnalyzer
from loop_engineering import LoopOptimizer, PerformanceMonitor
from load_real_data import RealDataLoader


def demonstrate_real_data_training():
    """Demonstrate training with real sentiment data"""
    print("=" * 60)
    print("Real Data Training Demonstration")
    print("=" * 60)
    print()
    
    # Step 1: Load real data
    print("Step 1: Loading Real Sentiment Data")
    print("-" * 40)
    loader = RealDataLoader()
    texts, labels = loader.load_sentiment_csv()
    
    # Get data statistics
    stats = loader.get_data_statistics(texts, labels)
    print(f"Dataset Statistics:")
    print(f"  Total samples: {stats['total_samples']}")
    print(f"  Classes: {stats['num_classes']}")
    print(f"  Class distribution: {stats['class_distribution']}")
    print(f"  Avg text length: {stats['avg_text_length']:.1f} words")
    print(f"  Max text length: {stats['max_text_length']} words")
    print()
    
    # Step 2: Prepare data for training
    print("Step 2: Preparing Data for Training")
    print("-" * 40)
    processed_data = loader.prepare_for_training(
        texts, labels,
        max_length=64,  # Adjusted for our dataset
        test_size=0.2,
        val_size=0.1
    )
    print()
    
    # Step 3: Build model
    print("Step 3: Building Transformer Model")
    print("-" * 40)
    model = TransformerClassifier(
        vocab_size=processed_data['vocab_size'],
        embed_dim=128,
        num_heads=4,
        num_layers=2,
        num_classes=processed_data['num_classes'],
        max_length=processed_data['max_length']
    )
    
    param_count = sum(p.numel() for p in model.parameters())
    print(f"Model created with {param_count:,} parameters")
    print(f"Architecture: 128-dim embeddings, 4 attention heads, 2 layers")
    print()
    
    # Step 4: Train model with loop engineering
    print("Step 4: Training Model with Loop Engineering")
    print("-" * 40)
    
    # Initialize loop engineering components
    loop_optimizer = LoopOptimizer(device='cpu')
    loop_monitor = PerformanceMonitor()
    
    # Use loop monitoring for training
    with loop_monitor.measure_time("model_training"):
        trainer = TensorTrainer(model, learning_rate=0.001, device='cpu')
        history = trainer.train(
            processed_data['train_loader'],
            processed_data['val_loader'],
            epochs=15,
            patience=5,
            verbose=True
        )
    
    training_stats = loop_monitor.get_stats("model_training")
    print(f"\nTraining completed in {training_stats['mean_time']:.2f}s")
    print()
    
    # Step 5: Evaluate model
    print("Step 5: Evaluating Model Performance")
    print("-" * 40)
    
    # Load best model
    model.load_state_dict(torch.load('best_model.pt', map_location='cpu'))
    evaluator = ModelEvaluator(model, device='cpu')
    
    # Evaluate on test set
    with loop_monitor.measure_time("model_evaluation"):
        predictions, true_labels, probabilities = evaluator.predict(
            processed_data['test_loader']
        )
        metrics = evaluator.compute_metrics(true_labels, predictions, probabilities)
    
    eval_stats = loop_monitor.get_stats("model_evaluation")
    print(f"Evaluation completed in {eval_stats['mean_time']:.2f}s")
    
    print("\nModel Performance Metrics:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")
    print()
    
    # Step 6: Error analysis
    print("Step 6: Error Analysis")
    print("-" * 40)
    error_analysis = evaluator.analyze_errors(true_labels, predictions)
    print(f"Total errors: {error_analysis['total_errors']}")
    print(f"Error rate: {error_analysis['error_rate']:.2%}")
    print("\nErrors by class:")
    for class_id, class_info in error_analysis['class_errors'].items():
        print(f"  Class {class_id}: {class_info['errors']}/{class_info['total']} "
              f"({class_info['error_rate']:.2%})")
    print()
    
    # Step 7: Visualize results
    print("Step 7: Visualizing Results")
    print("-" * 40)
    visualizer = TensorVisualizer()
    analyzer = TensorAnalyzer()
    
    # Plot learning curves
    visualizer.plot_learning_curves(history)
    print("✓ Learning curves plotted")
    
    # Analyze model embeddings
    sample_texts = processed_data['train_loader'].dataset[:10][0]
    with torch.no_grad():
        embeddings = model.embedding(sample_texts.unsqueeze(0))
    
    embedding_props = analyzer.analyze_tensor_properties(embeddings)
    print(f"✓ Embedding analysis completed")
    print(f"  Shape: {embedding_props['shape']}")
    print(f"  Mean: {embedding_props['mean']:.4f}")
    print(f"  Memory: {embedding_props['memory_usage_mb']:.4f} MB")
    print()
    
    # Step 8: Performance comparison
    print("Step 8: Performance Engineering Analysis")
    print("-" * 40)
    
    # Compare with vs without loop optimization
    sample_data = [torch.randn(50, 100) for _ in range(20)]
    
    def without_optimization(data):
        return [tensor.mean() for tensor in data]
    
    def with_optimization(data):
        stacked = torch.stack(data)
        return torch.mean(stacked, dim=[1, 2])
    
    comparison = loop_monitor.compare_performance(
        without_optimization, with_optimization, sample_data,
        "Without Loop Optimization", "With Loop Optimization", iterations=5
    )
    
    print(f"Loop optimization speedup: {comparison['comparison']['speedup']:.2f}x")
    print(f"Performance improvement: {comparison['comparison']['improvement_percent']:.1f}%")
    print()
    
    # Summary
    print("=" * 60)
    print("Real Data Training Summary")
    print("=" * 60)
    print(f"Dataset: {stats['total_samples']} real product reviews")
    print(f"Model: {param_count:,} parameters")
    print(f"Training time: {training_stats['mean_time']:.2f}s")
    print(f"Test accuracy: {metrics['accuracy']:.4f}")
    print(f"Test F1-score: {metrics['f1_macro']:.4f}")
    print(f"Loop optimization benefit: {comparison['comparison']['speedup']:.2f}x faster")
    print()
    print("✓ Successfully trained transformer model on real sentiment data")
    print("✓ Applied loop engineering optimizations for performance")
    print("✓ Achieved production-ready model with comprehensive evaluation")


def demonstrate_balanced_training():
    """Demonstrate training with balanced dataset"""
    print("=" * 60)
    print("Balanced Dataset Training Demonstration")
    print("=" * 60)
    print()
    
    loader = RealDataLoader()
    texts, labels = loader.load_sentiment_csv()
    
    # Show original distribution
    original_stats = loader.get_data_statistics(texts, labels)
    print("Original dataset:")
    print(f"  Class distribution: {original_stats['class_distribution']}")
    print()
    
    # Create balanced dataset
    print("Creating balanced dataset...")
    balanced_texts, balanced_labels = loader.create_balanced_dataset(texts, labels)
    
    # Show balanced distribution
    balanced_stats = loader.get_data_statistics(balanced_texts, balanced_labels)
    print("Balanced dataset:")
    print(f"  Class distribution: {balanced_stats['class_distribution']}")
    print()
    
    # Prepare balanced data for training
    print("Preparing balanced data for training...")
    processed_data = loader.prepare_for_training(
        balanced_texts, balanced_labels,
        max_length=64,
        test_size=0.2,
        val_size=0.1
    )
    
    # Build and train a smaller model for demonstration
    print("Building compact model for balanced training...")
    model = TransformerClassifier(
        vocab_size=processed_data['vocab_size'],
        embed_dim=64,
        num_heads=2,
        num_layers=1,
        num_classes=processed_data['num_classes'],
        max_length=processed_data['max_length']
    )
    
    print(f"Training on balanced dataset...")
    trainer = TensorTrainer(model, learning_rate=0.001, device='cpu')
    history = trainer.train(
        processed_data['train_loader'],
        processed_data['val_loader'],
        epochs=10,
        patience=3,
        verbose=True
    )
    
    print("\n✓ Balanced training completed")
    print(f"Final validation accuracy: {history['val_accuracies'][-1]:.2f}%")


def main():
    """Run real data demonstrations"""
    print("Real Data Demonstration Options:")
    print("1. Full training with real data")
    print("2. Balanced dataset training")
    print("3. Both demonstrations")
    print()
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == '1':
        demonstrate_real_data_training()
    elif choice == '2':
        demonstrate_balanced_training()
    elif choice == '3':
        demonstrate_real_data_training()
        print("\n" + "=" * 60 + "\n")
        demonstrate_balanced_training()
    else:
        print("Invalid choice. Running full demonstration...")
        demonstrate_real_data_training()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDemonstration interrupted by user")
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()