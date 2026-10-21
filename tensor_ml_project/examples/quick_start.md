user@user:/media/user/FE75-F816/AI_Developer/tensor_ml_project/examples$ python quick_start.py
Note: Visualization modules not available (seaborn not installed)
============================================================
Tensor ML Project - Quick Start Guide
============================================================

Step 1: Initialize Tensor Engineer
----------------------------------------
TensorEngineer initialized on device: cpu
✓ Tensor engineer initialized

Step 2: Create Sample Data
----------------------------------------
✓ Created 16 text samples
✓ Classes: {0, 1}
✓ Sample: 'This is a great product I love it' -> Label: 1

Step 3: Prepare Data Pipeline
----------------------------------------
✓ Vocabulary size: 11
✓ Training samples: 12
✓ Validation samples: 4

Step 4: Create Data Loaders
----------------------------------------
✓ Training batches: 3
✓ Validation batches: 2

Step 5: Build Transformer Model
----------------------------------------
✓ Model created with 100,802 parameters
✓ Architecture: 64-dim embeddings, 2 attention heads, 2 layers

Step 6: Train Model
----------------------------------------
Training started...
Starting training on cpu...
Model parameters: 100,802
/home/user/.local/lib/python3.12/site-packages/torch/nn/modules/transformer.py:531: UserWarning: The PyTorch API of nested tensors is in prototype stage and will change in the near future. We recommend specifying layout=torch.jagged when constructing a nested tensor, as this layout receives active development, has better operator coverage, and works with torch.compile. (Triggered internally at /pytorch/aten/src/ATen/NestedTensorImpl.cpp:178.)
  output = torch._nested_tensor_from_mask(
Epoch 1/10
  Train Loss: 0.7760, Train Acc: 33.33%
  Val Loss: 0.7088, Val Acc: 50.00%
  Learning Rate: 0.001000
Epoch 2/10
  Train Loss: 0.7369, Train Acc: 66.67%
  Val Loss: 0.7117, Val Acc: 50.00%
  Learning Rate: 0.001000
Epoch 3/10
  Train Loss: 0.6914, Train Acc: 58.33%
  Val Loss: 0.7010, Val Acc: 50.00%
  Learning Rate: 0.001000
Epoch 4/10
  Train Loss: 0.7615, Train Acc: 16.67%
  Val Loss: 0.6982, Val Acc: 50.00%
  Learning Rate: 0.001000
Epoch 5/10
  Train Loss: 0.6507, Train Acc: 66.67%
  Val Loss: 0.7054, Val Acc: 50.00%
  Learning Rate: 0.001000
Epoch 6/10
  Train Loss: 0.6931, Train Acc: 50.00%
  Val Loss: 0.7209, Val Acc: 50.00%
  Learning Rate: 0.001000
Epoch 7/10
  Train Loss: 0.6188, Train Acc: 58.33%
  Val Loss: 0.7241, Val Acc: 50.00%
  Learning Rate: 0.000500
Early stopping triggered after 7 epochs
✓ Training completed

Step 7: Evaluate Model
----------------------------------------
✓ Skipping detailed evaluation (seaborn not installed)
  Training completed successfully

Step 8: Analyze Results
----------------------------------------
✓ Skipping visualization (seaborn not installed)

Step 9: Loop Engineering Optimization
----------------------------------------
✓ Loop optimization completed
  Vectorized operation time: 0.0001s
  Result shape: torch.Size([10, 64])

============================================================
Quick Start Complete!
============================================================

You have successfully:
  ✓ Set up tensor operations
  ✓ Processed text data
  ✓ Built a transformer model
  ✓ Trained and evaluated the model
  ⊘ Skipped visualization (seaborn not installed)
  ✓ Applied loop engineering optimizations

Next Steps:
  • Try with your own data
  • Experiment with model hyperparameters
  • Explore loop engineering optimizations (examples/loop_engineering_demo.py)
  • Try real data training (examples/real_data_demo.py)
  • Install seaborn for full visualization support: pip install seaborn
  • Check the README.md for detailed documentation

