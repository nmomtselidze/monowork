user@user:/media/user/FE75-F816/AI_Developer/tensor_ml_project/examples$ python basic_usage.py
==================================================
Tensor Project - Basic Usage Test
==================================================

=== Testing Tensor Operations ===
TensorEngineer initialized on device: cpu
✓ Attention mask created: torch.Size([2, 10, 10])
✓ Positional encoding created: torch.Size([1, 10, 64])
✓ Tensor normalization works: torch.Size([2, 5, 10])
✓ Tensor operations test passed!

=== Testing Data Pipeline ===
✓ Vocabulary built: 3 words
✓ Text converted to tensor: torch.Size([10])
✓ Numerical data normalized: torch.Size([10, 5])
✓ Data pipeline test passed!

=== Testing Text Classifier ===
✓ Sample data created: 16 samples
✓ Dataset created: 16 samples
✓ Vocabulary size: 16
✓ Model created: 13282 parameters
✓ Forward pass successful: torch.Size([1, 2])
✓ Text classifier test passed!

=== Testing Model Evaluator ===
✗ Model evaluator test failed: No module named 'seaborn'

=== Testing Visualization ===
✗ Visualization test failed: No module named 'seaborn'

=== Testing Loop Engineering ===
✓ Vectorization works: torch.Size([5, 10])
✓ Memory-efficient iteration: 4 chunks
✓ Optimized accumulation: torch.Size([10])
✓ Performance monitoring: 0.0003s
✓ Loop engineering test passed!

==================================================
Test Summary
==================================================
Tensor Operations    ✓ PASSED
Data Pipeline        ✓ PASSED
Text Classifier      ✓ PASSED
Model Evaluator      ✗ FAILED
Visualization        ✗ FAILED
Loop Engineering     ✓ PASSED

Total: 4/6 tests passed
⚠️  Some tests failed. Please check the errors above.

