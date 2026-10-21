python loop_engineering_demo.py
============================================================
Loop Engineering Examples
============================================================

=== Vectorization Demonstration ===

Matrix Multiplication Performance:
  Slow (loop-based): 0.4284s
  Fast (vectorized): 0.4162s
  Speedup: 1.03x

=== Memory-Efficient Processing ===

Large tensor shape: torch.Size([100000, 100])
Memory usage: 38.15 MB

Processing in memory-efficient chunks:
  Processed chunk 10/10
Processed 10 chunks
Final result shape: torch.Size([10, 100])

=== Batch Processing Demonstration ===

Processing 1000 text samples:
Processed batch 10/10
Processed 1000 items
Sample results: ['SAMPLE TEXT NUMBER 0', 'SAMPLE TEXT NUMBER 1', 'SAMPLE TEXT NUMBER 2']

=== Performance Monitoring ===

Running heavy computation multiple times:
heavy_computation executed in 0.0064s
heavy_computation executed in 0.0060s
heavy_computation executed in 0.0052s
heavy_computation executed in 0.0054s
heavy_computation executed in 0.0034s

Performance Statistics:
  Total time: 0.0266s
  Mean time: 0.0053s
  Std time: 0.0010s
  Throughput: 187.94 ops/sec

=== Adaptive Batch Size ===

Adaptive batch size based on memory constraints:
  Normal load: 32 -> 32 (target: 1000 MB)
  High load: 64 -> 64 (target: 1000 MB)
  Very high load: 128 -> 128 (target: 1000 MB)

=== Accumulation Optimization ===

Accumulation Performance (100 tensors of shape 1000x100):
  Manual loop: 0.0027s
  Optimized: 0.0194s
  Speedup: 0.14x

=== Lazy Evaluation ===

Lazy evaluation for large dataset:
  Created lazy iterator for 100000 items
  Memory usage: Minimal (not computed yet)
  First 10 results: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
  Only computed 10 items instead of 100000

=== Function Performance Comparison ===

Implementation Comparison:
  Vectorized is faster
  Speedup: 1.78x
  Improvement: 43.7%

============================================================
Loop Engineering Examples Complete

