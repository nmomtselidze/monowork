"""
Loop Engineering Examples for Tensor ML Project
Demonstrates advanced loop optimization techniques and performance improvements
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import torch
import numpy as np
from typing import List


def demonstrate_vectorization():
    """Show vectorization benefits"""
    print("=== Vectorization Demonstration ===\n")
    
    from loop_engineering import LoopOptimizer, PerformanceMonitor
    
    optimizer = LoopOptimizer(device='cpu')
    monitor = PerformanceMonitor()
    
    # Create sample data
    data = [torch.randn(1000, 500) for _ in range(50)]
    
    # Slow loop-based approach
    def slow_matrix_multiply(tensors):
        result = []
        for tensor in tensors:
            result.append(torch.matmul(tensor, tensor.T))
        return result
    
    # Fast vectorized approach
    def fast_matrix_multiply(tensors):
        stacked = torch.stack(tensors)
        # Batch matrix multiplication
        return torch.bmm(stacked, stacked.transpose(1, 2))
    
    with monitor.measure_time("slow_multiply"):
        slow_result = slow_matrix_multiply(data)
    
    with monitor.measure_time("vectorized_multiply"):
        fast_result = fast_matrix_multiply(data)
    
    print("Matrix Multiplication Performance:")
    print(f"  Slow (loop-based): {monitor.get_stats('slow_multiply')['mean_time']:.4f}s")
    print(f"  Fast (vectorized): {monitor.get_stats('vectorized_multiply')['mean_time']:.4f}s")
    speedup = monitor.get_stats('slow_multiply')['mean_time'] / monitor.get_stats('vectorized_multiply')['mean_time']
    print(f"  Speedup: {speedup:.2f}x\n")


def demonstrate_memory_efficiency():
    """Show memory-efficient processing"""
    print("=== Memory-Efficient Processing ===\n")
    
    from loop_engineering import LoopOptimizer
    
    optimizer = LoopOptimizer(device='cpu')
    
    # Create a large tensor
    large_tensor = torch.randn(100000, 100)
    print(f"Large tensor shape: {large_tensor.shape}")
    print(f"Memory usage: {large_tensor.element_size() * large_tensor.numel() / (1024**2):.2f} MB\n")
    
    # Process in chunks
    def process_chunk(chunk):
        return chunk.mean(dim=0)
    
    chunk_results = []
    chunk_count = 0
    
    print("Processing in memory-efficient chunks:")
    for chunk in optimizer.memory_efficient_iteration(large_tensor, chunk_size=10000, operation=process_chunk):
        chunk_results.append(chunk)
        chunk_count += 1
        print(f"  Processed chunk {chunk_count}/10", end='\r')
    
    print()  # New line
    print(f"Processed {chunk_count} chunks")
    print(f"Final result shape: {torch.stack(chunk_results).shape}\n")


def demonstrate_batch_processing():
    """Show batch processing benefits"""
    print("=== Batch Processing Demonstration ===\n")
    
    from loop_engineering import batch_processor
    
    # Create sample data
    texts = [f"Sample text number {i}" for i in range(1000)]
    
    def process_batch(batch):
        """Simulate text processing"""
        return [text.upper() for text in batch]
    
    print("Processing 1000 text samples:")
    results = batch_processor(texts, process_batch, batch_size=100, show_progress=True)
    
    print(f"Processed {len(results)} items")
    print(f"Sample results: {results[:3]}\n")


def demonstrate_performance_monitoring():
    """Show performance monitoring capabilities"""
    print("=== Performance Monitoring ===\n")
    
    from loop_engineering import PerformanceMonitor, loop_timer
    
    monitor = PerformanceMonitor()
    
    # Function to monitor
    @loop_timer
    def heavy_computation(size=1000):
        """Simulate heavy computation"""
        matrix = torch.randn(size, size)
        return torch.matmul(matrix, matrix.T)
    
    # Run multiple times
    print("Running heavy computation multiple times:")
    for i in range(5):
        with monitor.measure_time("computation"):
            result = heavy_computation(500)
    
    stats = monitor.get_stats("computation")
    print(f"\nPerformance Statistics:")
    print(f"  Total time: {stats['total_time']:.4f}s")
    print(f"  Mean time: {stats['mean_time']:.4f}s")
    print(f"  Std time: {stats['std_time']:.4f}s")
    print(f"  Throughput: {stats['throughput']:.2f} ops/sec\n")


def demonstrate_adaptive_batching():
    """Show adaptive batch size adjustment"""
    print("=== Adaptive Batch Size ===\n")
    
    from loop_engineering import adaptive_batch_size
    
    # Simulate different memory scenarios
    scenarios = [
        (32, 1000, "Normal load"),
        (64, 1000, "High load"),
        (128, 1000, "Very high load")
    ]
    
    print("Adaptive batch size based on memory constraints:")
    for initial, target, description in scenarios:
        optimal = adaptive_batch_size(initial_size=initial, target_memory_mb=target)
        print(f"  {description}: {initial} -> {optimal} (target: {target} MB)")
    
    print()


def demonstrate_accumulation_optimization():
    """Show optimized accumulation"""
    print("=== Accumulation Optimization ===\n")
    
    from loop_engineering import LoopOptimizer, PerformanceMonitor
    
    optimizer = LoopOptimizer(device='cpu')
    monitor = PerformanceMonitor()
    
    # Create many tensors
    tensors = [torch.randn(1000, 100) for _ in range(100)]
    
    # Manual accumulation
    with monitor.measure_time("manual_accumulation"):
        manual_result = tensors[0].clone()
        for tensor in tensors[1:]:
            manual_result += tensor
    
    # Optimized accumulation
    with monitor.measure_time("optimized_accumulation"):
        optimized_result = optimizer.optimized_accumulation(tensors, operation='sum')
    
    print("Accumulation Performance (100 tensors of shape 1000x100):")
    print(f"  Manual loop: {monitor.get_stats('manual_accumulation')['mean_time']:.4f}s")
    print(f"  Optimized: {monitor.get_stats('optimized_accumulation')['mean_time']:.4f}s")
    speedup = monitor.get_stats('manual_accumulation')['mean_time'] / monitor.get_stats('optimized_accumulation')['mean_time']
    print(f"  Speedup: {speedup:.2f}x\n")


def demonstrate_lazy_evaluation():
    """Show lazy evaluation benefits"""
    print("=== Lazy Evaluation ===\n")
    
    from loop_engineering import LoopOptimizer
    
    optimizer = LoopOptimizer(device='cpu')
    
    # Create large dataset
    data = list(range(100000))
    
    def expensive_transform(x):
        """Simulate expensive transformation"""
        return x ** 2 + 2 * x + 1
    
    print("Lazy evaluation for large dataset:")
    
    # Lazy evaluation - doesn't process immediately
    lazy_results = optimizer.lazy_evaluation(data, expensive_transform)
    
    print(f"  Created lazy iterator for {len(data)} items")
    print(f"  Memory usage: Minimal (not computed yet)")
    
    # Process only first 10 items
    first_10 = [next(lazy_results) for _ in range(10)]
    print(f"  First 10 results: {first_10}")
    print(f"  Only computed 10 items instead of {len(data)}\n")


def demonstrate_function_comparison():
    """Compare different implementations"""
    print("=== Function Performance Comparison ===\n")
    
    from loop_engineering import PerformanceMonitor
    
    monitor = PerformanceMonitor()
    
    # Create test data
    data = [torch.randn(100, 100) for _ in range(50)]
    
    def implementation1(tensors):
        """Implementation 1: List comprehension"""
        return [tensor.mean() for tensor in tensors]
    
    def implementation2(tensors):
        """Implementation 2: Vectorized"""
        stacked = torch.stack(tensors)
        return torch.mean(stacked, dim=[1, 2])
    
    comparison = monitor.compare_performance(
        implementation1, implementation2, data,
        "List Comprehension", "Vectorized", iterations=10
    )
    
    print("Implementation Comparison:")
    print(f"  {comparison['comparison']['faster']} is faster")
    print(f"  Speedup: {comparison['comparison']['speedup']:.2f}x")
    print(f"  Improvement: {comparison['comparison']['improvement_percent']:.1f}%\n")


def main():
    """Run all demonstrations"""
    print("=" * 60)
    print("Loop Engineering Examples")
    print("=" * 60)
    print()
    
    demonstrations = [
        ("Vectorization", demonstrate_vectorization),
        ("Memory Efficiency", demonstrate_memory_efficiency),
        ("Batch Processing", demonstrate_batch_processing),
        ("Performance Monitoring", demonstrate_performance_monitoring),
        ("Adaptive Batching", demonstrate_adaptive_batching),
        ("Accumulation Optimization", demonstrate_accumulation_optimization),
        ("Lazy Evaluation", demonstrate_lazy_evaluation),
        ("Function Comparison", demonstrate_function_comparison)
    ]
    
    for name, demo_func in demonstrations:
        try:
            demo_func()
        except Exception as e:
            print(f"Error in {name}: {e}\n")
    
    print("=" * 60)
    print("Loop Engineering Examples Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()