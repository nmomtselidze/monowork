"""
Loop Engineering and Optimization for ML Applications
Advanced techniques for optimizing loops, vectorization, and iterative operations
"""

import torch
import numpy as np
import time
import multiprocessing
from typing import Callable, List, Tuple, Optional, Any, Generator, Dict
from contextlib import contextmanager
from functools import wraps
import warnings


class LoopOptimizer:
    """
    Advanced loop optimization techniques for ML applications.
    Focuses on vectorization, memory efficiency, and performance optimization.
    """
    
    def __init__(self, device: str = 'cpu'):
        """
        Initialize loop optimizer.
        
        Args:
            device: Device for tensor operations
        """
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        self.optimization_stats = {}
    
    def vectorize_loop(
        self,
        func: Callable,
        data: List[Any],
        batch_size: Optional[int] = None
    ) -> torch.Tensor:
        """
        Convert a loop-based operation to vectorized tensor operations.
        
        Args:
            func: Function to apply to each element
            data: List of input data
            batch_size: Optional batch size for processing
            
        Returns:
            Vectorized result tensor
        """
        if batch_size is None:
            # Try full vectorization
            try:
                stacked_data = torch.stack(data).to(self.device)
                return func(stacked_data)
            except:
                # Fall back to batch processing
                batch_size = min(32, len(data))
        
        # Batch processing
        results = []
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            try:
                stacked_batch = torch.stack(batch).to(self.device)
                batch_result = func(stacked_batch)
                results.append(batch_result)
            except:
                # Fall back to element-wise processing
                for item in batch:
                    result = func(item)
                    results.append(result)
        
        return torch.cat(results) if all(isinstance(r, torch.Tensor) for r in results) else results
    
    def parallel_map(
        self,
        func: Callable,
        data: List[Any],
        num_workers: Optional[int] = None
    ) -> List[Any]:
        """
        Apply function to data in parallel using multiprocessing.
        
        Args:
            func: Function to apply
            data: List of input data
            num_workers: Number of parallel workers (default: CPU count)
            
        Returns:
            List of results
        """
        if num_workers is None:
            num_workers = multiprocessing.cpu_count()
        
        if num_workers <= 1 or len(data) < 10:
            return [func(item) for item in data]
        
        try:
            with multiprocessing.Pool(num_workers) as pool:
                results = pool.map(func, data)
            return results
        except Exception as e:
            # Fallback to sequential processing if multiprocessing fails
            warnings.warn(f"Multiprocessing failed: {e}. Falling back to sequential processing.")
            return [func(item) for item in data]
    
    def memory_efficient_iteration(
        self,
        data: torch.Tensor,
        chunk_size: int = 1000,
        operation: Callable = lambda x: x
    ) -> Generator[torch.Tensor, None, None]:
        """
        Iterate over large tensors in memory-efficient chunks.
        
        Args:
            data: Large input tensor
            chunk_size: Size of each chunk
            operation: Operation to apply to each chunk
            
        Yields:
            Processed chunks
        """
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            yield operation(chunk)
    
    def lazy_evaluation(
        self,
        data: List[Any],
        transform: Callable
    ) -> Generator[Any, None, None]:
        """
        Lazy evaluation pattern for memory-efficient processing.
        
        Args:
            data: Input data
            transform: Transformation function
            
        Yields:
            Transformed data items on demand
        """
        for item in data:
            yield transform(item)
    
    def optimized_accumulation(
        self,
        values: List[torch.Tensor],
        operation: str = 'sum'
    ) -> torch.Tensor:
        """
        Optimized accumulation operation to reduce loop overhead.
        
        Args:
            values: List of tensors to accumulate
            operation: 'sum', 'mean', 'max', 'min'
            
        Returns:
            Accumulated result
        """
        if not values:
            raise ValueError("Cannot accumulate empty list")
        
        stacked = torch.stack(values)
        
        if operation == 'sum':
            return torch.sum(stacked, dim=0)
        elif operation == 'mean':
            return torch.mean(stacked, dim=0)
        elif operation == 'max':
            return torch.max(stacked, dim=0)[0]
        elif operation == 'min':
            return torch.min(stacked, dim=0)[0]
        else:
            raise ValueError(f"Unknown operation: {operation}")


class PerformanceMonitor:
    """
    Performance monitoring and profiling utilities for loop optimization.
    """
    
    def __init__(self):
        """Initialize performance monitor."""
        self.timings = {}
        self.memory_usage = {}
    
    @contextmanager
    def measure_time(self, operation_name: str):
        """
        Context manager to measure execution time.
        
        Args:
            operation_name: Name of the operation being measured
        """
        start_time = time.time()
        start_memory = torch.cuda.memory_allocated() if torch.cuda.is_available() else 0
        
        try:
            yield
        finally:
            end_time = time.time()
            end_memory = torch.cuda.memory_allocated() if torch.cuda.is_available() else 0
            
            elapsed = end_time - start_time
            memory_delta = (end_memory - start_memory) / (1024 ** 2)  # MB
            
            if operation_name not in self.timings:
                self.timings[operation_name] = []
            self.timings[operation_name].append(elapsed)
            
            if operation_name not in self.memory_usage:
                self.memory_usage[operation_name] = []
            self.memory_usage[operation_name].append(memory_delta)
    
    def get_stats(self, operation_name: str) -> Dict[str, float]:
        """
        Get performance statistics for an operation.
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            Dictionary with statistics
        """
        if operation_name not in self.timings:
            return {}
        
        times = self.timings[operation_name]
        memories = self.memory_usage.get(operation_name, [0] * len(times))
        
        return {
            'count': len(times),
            'total_time': sum(times),
            'mean_time': np.mean(times),
            'std_time': np.std(times),
            'min_time': min(times),
            'max_time': max(times),
            'total_memory_mb': sum(memories),
            'mean_memory_mb': np.mean(memories),
            'throughput': len(times) / sum(times) if sum(times) > 0 else 0
        }
    
    def compare_performance(
        self,
        func1: Callable,
        func2: Callable,
        data: Any,
        name1: str = "Function 1",
        name2: str = "Function 2",
        iterations: int = 10
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare performance of two functions.
        
        Args:
            func1: First function to compare
            func2: Second function to compare
            data: Input data
            name1: Name for first function
            name2: Name for second function
            iterations: Number of iterations to run
            
        Returns:
            Performance comparison dictionary
        """
        results = {}
        
        # Test function 1
        with self.measure_time(name1):
            for _ in range(iterations):
                result1 = func1(data)
        
        # Test function 2
        with self.measure_time(name2):
            for _ in range(iterations):
                result2 = func2(data)
        
        results[name1] = self.get_stats(name1)
        results[name2] = self.get_stats(name2)
        
        # Calculate speedup
        mean_time1 = results[name1]['mean_time']
        mean_time2 = results[name2]['mean_time']
        speedup = mean_time1 / mean_time2 if mean_time2 > 0 else float('inf')
        
        results['comparison'] = {
            'speedup': speedup,
            'faster': name2 if speedup > 1 else name1,
            'improvement_percent': ((mean_time1 - mean_time2) / mean_time1 * 100) if mean_time1 > 0 else 0
        }
        
        return results
    
    def print_report(self, operation_name: Optional[str] = None):
        """
        Print performance report.
        
        Args:
            operation_name: Specific operation to report, or None for all
        """
        if operation_name:
            stats = self.get_stats(operation_name)
            if stats:
                print(f"\n=== Performance Report: {operation_name} ===")
                print(f"Count: {stats['count']}")
                print(f"Total Time: {stats['total_time']:.4f}s")
                print(f"Mean Time: {stats['mean_time']:.4f}s")
                print(f"Std Time: {stats['std_time']:.4f}s")
                print(f"Min Time: {stats['min_time']:.4f}s")
                print(f"Max Time: {stats['max_time']:.4f}s")
                print(f"Total Memory: {stats['total_memory_mb']:.2f} MB")
                print(f"Mean Memory: {stats['mean_memory_mb']:.2f} MB")
                print(f"Throughput: {stats['throughput']:.2f} ops/sec")
        else:
            print("\n=== Overall Performance Report ===")
            for op_name in self.timings.keys():
                self.print_report(op_name)


def loop_timer(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to time
        
    Returns:
        Wrapped function with timing
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f}s")
        return result
    return wrapper


def batch_processor(
    data: List[Any],
    process_func: Callable,
    batch_size: int = 32,
    show_progress: bool = False
) -> List[Any]:
    """
    Process data in batches for better performance.
    
    Args:
        data: Input data list
        process_func: Function to process each batch
        batch_size: Size of each batch
        show_progress: Whether to show progress
        
    Returns:
        List of processed results
    """
    results = []
    total_batches = (len(data) + batch_size - 1) // batch_size
    
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        batch_result = process_func(batch)
        results.extend(batch_result if isinstance(batch_result, list) else [batch_result])
        
        if show_progress:
            batch_num = i // batch_size + 1
            print(f"Processed batch {batch_num}/{total_batches}", end='\r')
    
    if show_progress:
        print()  # New line after progress
    
    return results


def adaptive_batch_size(
    initial_size: int = 32,
    min_size: int = 1,
    max_size: int = 512,
    target_memory_mb: float = 1000
) -> int:
    """
    Dynamically adjust batch size based on memory constraints.
    
    Args:
        initial_size: Initial batch size
        min_size: Minimum batch size
        max_size: Maximum batch size
        target_memory_mb: Target memory usage in MB
        
    Returns:
        Optimal batch size
    """
    if not torch.cuda.is_available():
        return initial_size
    
    current_memory = torch.cuda.memory_allocated() / (1024 ** 2)  # MB
    
    if current_memory > target_memory_mb:
        # Reduce batch size
        new_size = max(min_size, int(initial_size * (target_memory_mb / current_memory)))
        warnings.warn(f"Reducing batch size from {initial_size} to {new_size} due to memory constraints")
        return new_size
    else:
        # Try to increase batch size
        available_memory = target_memory_mb - current_memory
        memory_per_sample = current_memory / initial_size if initial_size > 0 else 1
        potential_increase = int(available_memory / memory_per_sample)
        new_size = min(max_size, initial_size + potential_increase)
        return new_size


def early_stopping_loop(
    metric_history: List[float],
    patience: int = 5,
    min_delta: float = 0.001,
    mode: str = 'min'
) -> bool:
    """
    Check if training should stop early based on metric history.
    
    Args:
        metric_history: List of metric values
        patience: Number of epochs to wait for improvement
        min_delta: Minimum change to qualify as improvement
        mode: 'min' or 'max' for metric optimization
        
    Returns:
        True if should stop, False otherwise
    """
    if len(metric_history) < patience + 1:
        return False
    
    if mode == 'min':
        best = min(metric_history[:-patience])
        current = metric_history[-1]
        return current >= best - min_delta
    else:
        best = max(metric_history[:-patience])
        current = metric_history[-1]
        return current <= best + min_delta


def demonstrate_loop_engineering():
    """
    Demonstrate loop engineering capabilities.
    """
    print("=== Loop Engineering Demonstration ===\n")
    
    # Initialize optimizer and monitor
    optimizer = LoopOptimizer(device='cpu')
    monitor = PerformanceMonitor()
    
    # 1. Vectorization demonstration
    print("1. Vectorization Example:")
    data = [torch.randn(100, 50) for _ in range(10)]
    
    def slow_sum(data_list):
        """Slow loop-based sum"""
        result = data_list[0].clone()
        for tensor in data_list[1:]:
            result += tensor
        return result
    
    def fast_sum(data_list):
        """Fast vectorized sum"""
        return torch.sum(torch.stack(data_list), dim=0)
    
    with monitor.measure_time("slow_loop"):
        result_slow = slow_sum(data)
    
    with monitor.measure_time("vectorized"):
        result_fast = fast_sum(data)
    
    print(f"   Slow loop: {monitor.get_stats('slow_loop')['mean_time']:.4f}s")
    print(f"   Vectorized: {monitor.get_stats('vectorized')['mean_time']:.4f}s")
    print(f"   Speedup: {monitor.get_stats('slow_loop')['mean_time'] / monitor.get_stats('vectorized')['mean_time']:.2f}x\n")
    
    # 2. Memory-efficient iteration
    print("2. Memory-Efficient Iteration:")
    large_tensor = torch.randn(10000, 100)
    chunk_count = 0
    
    for chunk in optimizer.memory_efficient_iteration(large_tensor, chunk_size=1000):
        chunk_count += 1
        # Process chunk (in this case, just counting)
    
    print(f"   Processed {chunk_count} chunks of 1000 samples each")
    print(f"   Total samples: {large_tensor.shape[0]}\n")
    
    # 3. Batch processing
    print("3. Batch Processing:")
    sample_data = list(range(100))
    
    def process_batch(batch):
        return [x * 2 for x in batch]
    
    results = batch_processor(sample_data, process_batch, batch_size=10, show_progress=True)
    print(f"   Processed {len(results)} items in batches")
    print(f"   Sample result: {results[:5]}\n")
    
    # 4. Optimized accumulation
    print("4. Optimized Accumulation:")
    tensors = [torch.randn(1000, 100) for _ in range(100)]
    
    with monitor.measure_time("loop_accumulation"):
        # Manual loop accumulation
        manual_result = tensors[0].clone()
        for t in tensors[1:]:
            manual_result += t
    
    with monitor.measure_time("optimized_accumulation"):
        optimized_result = optimizer.optimized_accumulation(tensors, operation='sum')
    
    print(f"   Manual accumulation: {monitor.get_stats('loop_accumulation')['mean_time']:.4f}s")
    print(f"   Optimized accumulation: {monitor.get_stats('optimized_accumulation')['mean_time']:.4f}s")
    print(f"   Speedup: {monitor.get_stats('loop_accumulation')['mean_time'] / monitor.get_stats('optimized_accumulation')['mean_time']:.2f}x\n")
    
    # 5. Performance comparison
    print("5. Performance Comparison:")
    comparison_data = [torch.randn(50, 50) for _ in range(20)]
    
    def func1(data):
        return [t.mean() for t in data]
    
    def func2(data):
        stacked = torch.stack(data)
        return torch.mean(stacked, dim=[1, 2])
    
    comparison = monitor.compare_performance(
        func1, func2, comparison_data,
        "List Comprehension", "Vectorized Operation", iterations=5
    )
    
    print(f"   Speedup: {comparison['comparison']['speedup']:.2f}x")
    print(f"   Improvement: {comparison['comparison']['improvement_percent']:.1f}%")
    print(f"   Faster method: {comparison['comparison']['faster']}\n")
    
    print("=== Loop Engineering Demo Complete ===")


if __name__ == "__main__":
    demonstrate_loop_engineering()