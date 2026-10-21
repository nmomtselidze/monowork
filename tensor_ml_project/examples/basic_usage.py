"""
Basic Usage Examples for Tensor ML Project
Run this script to verify the installation and basic functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import torch
import numpy as np

def test_tensor_operations():
    """Test basic tensor operations"""
    print("=== Testing Tensor Operations ===")
    
    try:
        from tensor_ops import TensorEngineer
        
        engineer = TensorEngineer(device='cpu')
        
        # Test basic operations
        tensor_a = torch.randn(3, 4)
        tensor_b = torch.randn(3, 4)
        
        # Test attention mask creation
        mask = engineer.create_attention_mask(seq_len=10, batch_size=2)
        print(f"✓ Attention mask created: {mask.shape}")
        
        # Test positional encoding
        pos_enc = engineer.positional_encoding(seq_len=10, d_model=64)
        print(f"✓ Positional encoding created: {pos_enc.shape}")
        
        # Test normalization
        test_tensor = torch.randn(2, 5, 10)
        normalized = engineer.tensor_normalization(test_tensor)
        print(f"✓ Tensor normalization works: {normalized.shape}")
        
        print("✓ Tensor operations test passed!\n")
        return True
        
    except Exception as e:
        print(f"✗ Tensor operations test failed: {e}\n")
        return False


def test_data_pipeline():
    """Test data preprocessing pipeline"""
    print("=== Testing Data Pipeline ===")
    
    try:
        from data_pipeline import DataPreprocessor, TensorDataPipeline
        
        preprocessor = DataPreprocessor(device='cpu')
        pipeline = TensorDataPipeline(preprocessor)
        
        # Test text processing
        sample_texts = ["This is a test", "Another test sentence"]
        vocab = preprocessor.build_vocabulary(sample_texts)
        print(f"✓ Vocabulary built: {len(vocab)} words")
        
        # Test text to tensor conversion
        text_tensor = preprocessor.text_to_tensor(sample_texts[0], vocab, max_length=10)
        print(f"✓ Text converted to tensor: {text_tensor.shape}")
        
        # Test numerical processing
        numerical_data = np.random.randn(10, 5)
        normalized = preprocessor.normalize_numerical(numerical_data, fit=True)
        print(f"✓ Numerical data normalized: {normalized.shape}")
        
        print("✓ Data pipeline test passed!\n")
        return True
        
    except Exception as e:
        print(f"✗ Data pipeline test failed: {e}\n")
        return False


def test_text_classifier():
    """Test text classifier model"""
    print("=== Testing Text Classifier ===")
    
    try:
        from text_classifier import TransformerClassifier, TextDataset, create_sample_data
        from torch.utils.data import DataLoader
        
        # Create sample data
        texts, labels = create_sample_data()
        print(f"✓ Sample data created: {len(texts)} samples")
        
        # Create dataset
        dataset = TextDataset(texts, labels, max_length=32)
        print(f"✓ Dataset created: {len(dataset)} samples")
        print(f"✓ Vocabulary size: {dataset.vocab_size}")
        
        # Create model
        model = TransformerClassifier(
            vocab_size=dataset.vocab_size,
            embed_dim=32,
            num_heads=2,
            num_layers=1,
            num_classes=2,
            max_length=32
        )
        print(f"✓ Model created: {sum(p.numel() for p in model.parameters())} parameters")
        
        # Test forward pass
        sample_input = dataset[0][0].unsqueeze(0)
        output = model(sample_input)
        print(f"✓ Forward pass successful: {output.shape}")
        
        print("✓ Text classifier test passed!\n")
        return True
        
    except Exception as e:
        print(f"✗ Text classifier test failed: {e}\n")
        return False


def test_model_evaluator():
    """Test model evaluation"""
    print("=== Testing Model Evaluator ===")
    
    try:
        from model_evaluator import ModelEvaluator
        from text_classifier import TransformerClassifier, TextDataset, create_sample_data
        from torch.utils.data import DataLoader
        
        # Create simple model and data
        texts, labels = create_sample_data()
        dataset = TextDataset(texts, labels, max_length=16)
        model = TransformerClassifier(
            vocab_size=dataset.vocab_size,
            embed_dim=16,
            num_heads=1,
            num_layers=1,
            num_classes=2,
            max_length=16
        )
        
        # Create evaluator
        evaluator = ModelEvaluator(model, device='cpu')
        print("✓ Evaluator created")
        
        # Create small data loader
        loader = DataLoader(dataset, batch_size=2, shuffle=False)
        
        # Test prediction
        predictions, true_labels, probabilities = evaluator.predict(loader)
        print(f"✓ Predictions generated: {predictions.shape}")
        
        # Test metrics computation
        metrics = evaluator.compute_metrics(true_labels, predictions, probabilities)
        print(f"✓ Metrics computed: {list(metrics.keys())}")
        
        print("✓ Model evaluator test passed!\n")
        return True
        
    except Exception as e:
        print(f"✗ Model evaluator test failed: {e}\n")
        return False


def test_visualization():
    """Test visualization capabilities"""
    print("=== Testing Visualization ===")
    
    try:
        from visualization import TensorVisualizer, TensorAnalyzer
        
        visualizer = TensorVisualizer()
        analyzer = TensorAnalyzer()
        
        # Test tensor analysis
        test_tensor = torch.randn(50, 25)
        properties = analyzer.analyze_tensor_properties(test_tensor)
        print(f"✓ Tensor analysis completed: {list(properties.keys())}")
        
        # Test tensor comparison
        tensor1 = torch.randn(10, 10)
        tensor2 = torch.randn(10, 10)
        comparison = analyzer.compare_tensors(tensor1, tensor2)
        print(f"✓ Tensor comparison completed: {list(comparison.keys())}")
        
        # Test anomaly detection
        anomaly_tensor = torch.cat([torch.randn(95), torch.tensor([10, -10])])
        anomalies = analyzer.detect_anomalies(anomaly_tensor)
        print(f"✓ Anomaly detection completed: {anomalies['total_anomalies']} anomalies")
        
        print("✓ Visualization test passed!\n")
        return True
        
    except Exception as e:
        print(f"✗ Visualization test failed: {e}\n")
        return False


def test_loop_engineering():
    """Test loop engineering capabilities"""
    print("=== Testing Loop Engineering ===")
    
    try:
        from loop_engineering import LoopOptimizer, PerformanceMonitor
        
        optimizer = LoopOptimizer(device='cpu')
        monitor = PerformanceMonitor()
        
        # Test vectorization
        data = [torch.randn(10, 10) for _ in range(5)]
        vectorized_result = optimizer.vectorize_loop(lambda x: x.mean(dim=1), data)
        print(f"✓ Vectorization works: {vectorized_result.shape}")
        
        # Test memory-efficient iteration
        large_tensor = torch.randn(100, 50)
        chunk_count = 0
        for chunk in optimizer.memory_efficient_iteration(large_tensor, chunk_size=25):
            chunk_count += 1
        print(f"✓ Memory-efficient iteration: {chunk_count} chunks")
        
        # Test optimized accumulation
        tensors = [torch.randn(10) for _ in range(10)]
        accumulated = optimizer.optimized_accumulation(tensors, operation='sum')
        print(f"✓ Optimized accumulation: {accumulated.shape}")
        
        # Test performance monitoring
        with monitor.measure_time("test_operation"):
            result = torch.randn(100, 100).matmul(torch.randn(100, 100))
        stats = monitor.get_stats("test_operation")
        print(f"✓ Performance monitoring: {stats['mean_time']:.4f}s")
        
        print("✓ Loop engineering test passed!\n")
        return True
        
    except Exception as e:
        print(f"✗ Loop engineering test failed: {e}\n")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("Tensor Project - Basic Usage Test")
    print("=" * 50)
    print()
    
    results = []
    
    # Run all tests
    results.append(("Tensor Operations", test_tensor_operations()))
    results.append(("Data Pipeline", test_data_pipeline()))
    results.append(("Text Classifier", test_text_classifier()))
    results.append(("Model Evaluator", test_model_evaluator()))
    results.append(("Visualization", test_visualization()))
    results.append(("Loop Engineering", test_loop_engineering()))
    
    # Print summary
    print("=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:<20} {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The project is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit(main())
