python3 -m venv ~/.venvs/tensor_ml
source ~/.venvs/tensor_ml/bin/activate
pip install seaborn torch scikit-learn
python examples/real_data_demo.py
#--------------------------------
Matplotlib is building the font cache; this may take a moment.
(tensor_ml) user@user:/media/user/FE75-F816/AI_Developer/tensor_ml_project$ uv run python examples/real_data_demo.py
Real Data Demonstration Options:
1. Full training with real data
2. Balanced dataset training
3. Both demonstrations

Enter your choice (1-3): 1
============================================================
Real Data Training Demonstration
============================================================

Step 1: Loading Real Sentiment Data
----------------------------------------
Loaded 153 samples from sentiment_dataset.csv
Label distribution: [76 77]
Dataset Statistics:
  Total samples: 153
  Classes: 2
  Class distribution: {np.int64(0): np.int64(76), np.int64(1): np.int64(77)}
  Avg text length: 7.5 words
  Max text length: 18 words

Step 2: Preparing Data for Training
----------------------------------------

Preparing data for training...
Vocabulary size: 211
Number of classes: 2
Max sequence length: 64
Training batches: 7
Validation batches: 1
Test batches: 2

Step 3: Building Transformer Model
----------------------------------------
Model created with 423,810 parameters
Architecture: 128-dim embeddings, 4 attention heads, 2 layers

Step 4: Training Model with Loop Engineering
----------------------------------------
Starting training on cpu...
Model parameters: 423,810
/home/user/.venvs/tensor_ml/lib/python3.12/site-packages/torch/nn/modules/transformer.py:533: UserWarning: The PyTorch API of nested tensors is in prototype stage and will change in the near future. We recommend specifying layout=torch.jagged when constructing a nested tensor, as this layout receives active development, has better operator coverage, and works with torch.compile. (Triggered internally at /__w/pytorch/pytorch/aten/src/ATen/NestedTensorImpl.cpp:177.)
  output = torch._nested_tensor_from_mask(
Epoch 1/15
  Train Loss: 0.9305, Train Acc: 48.11%
  Val Loss: 0.6807, Val Acc: 75.00%
  Learning Rate: 0.001000
Epoch 2/15
  Train Loss: 0.5339, Train Acc: 72.64%
  Val Loss: 0.6583, Val Acc: 75.00%
  Learning Rate: 0.001000
Epoch 3/15
  Train Loss: 0.3918, Train Acc: 80.19%
  Val Loss: 0.6616, Val Acc: 62.50%
  Learning Rate: 0.001000
Epoch 4/15
  Train Loss: 0.3117, Train Acc: 84.91%
  Val Loss: 0.6178, Val Acc: 75.00%
  Learning Rate: 0.001000
Epoch 5/15
  Train Loss: 0.1992, Train Acc: 94.34%
  Val Loss: 0.6110, Val Acc: 68.75%
  Learning Rate: 0.001000
Epoch 6/15
  Train Loss: 0.0771, Train Acc: 97.17%
  Val Loss: 0.5996, Val Acc: 62.50%
  Learning Rate: 0.001000
Epoch 7/15
  Train Loss: 0.0196, Train Acc: 100.00%
  Val Loss: 0.5769, Val Acc: 68.75%
  Learning Rate: 0.001000
Epoch 8/15
  Train Loss: 0.0201, Train Acc: 99.06%
  Val Loss: 0.5839, Val Acc: 68.75%
  Learning Rate: 0.001000
Epoch 9/15
  Train Loss: 0.0045, Train Acc: 100.00%
  Val Loss: 0.6369, Val Acc: 56.25%
  Learning Rate: 0.001000
Epoch 10/15
  Train Loss: 0.0209, Train Acc: 99.06%
  Val Loss: 0.6078, Val Acc: 68.75%
  Learning Rate: 0.000500
Epoch 11/15
  Train Loss: 0.0055, Train Acc: 100.00%
  Val Loss: 0.6066, Val Acc: 68.75%
  Learning Rate: 0.000500
Epoch 12/15
  Train Loss: 0.0005, Train Acc: 100.00%
  Val Loss: 0.6167, Val Acc: 68.75%
  Learning Rate: 0.000500
Early stopping triggered after 12 epochs

Training completed in 7.10s

Step 5: Evaluating Model Performance
----------------------------------------
Evaluation completed in 0.04s

Model Performance Metrics:
  accuracy: 0.4516
  precision_macro: 0.7167
  recall_macro: 0.5278
  f1_macro: 0.3550
  precision_weighted: 0.7624
  recall_weighted: 0.4516
  f1_weighted: 0.3147
  roc_auc: 0.8803

Step 6: Error Analysis
----------------------------------------
Total errors: 17
Error rate: 54.84%

Errors by class:
  Class 0: 0/13 (0.00%)
  Class 1: 17/18 (94.44%)

Step 7: Visualizing Results
----------------------------------------
✓ Learning curves plotted
✓ Embedding analysis completed
  Shape: (1, 10, 64, 128)
  Mean: -0.0003
  Memory: 0.3125 MB

Step 8: Performance Engineering Analysis
----------------------------------------
Loop optimization speedup: 3.07x
Performance improvement: 67.5%

============================================================
Real Data Training Summary
============================================================
Dataset: 153 real product reviews
Model: 423,810 parameters
Training time: 7.10s
Test accuracy: 0.4516
Test F1-score: 0.3550
Loop optimization benefit: 3.07x faster

✓ Successfully trained transformer model on real sentiment data
✓ Applied loop engineering optimizations for performance
✓ Achieved production-ready model with comprehensive evaluation
###============================================================###
Real Data Demonstration Options:
1. Full training with real data
2. Balanced dataset training
3. Both demonstrations

Enter your choice (1-3): 2
============================================================
Balanced Dataset Training Demonstration
============================================================

Loaded 153 samples from sentiment_dataset.csv
Label distribution: [76 77]
Original dataset:
  Class distribution: {np.int64(0): np.int64(76), np.int64(1): np.int64(77)}

Creating balanced dataset...
Created balanced dataset: 152 samples
Samples per class: 76
Balanced dataset:
  Class distribution: {np.int64(0): np.int64(76), np.int64(1): np.int64(76)}

Preparing balanced data for training...

Preparing data for training...
Vocabulary size: 209
Number of classes: 2
Max sequence length: 64
Training batches: 7
Validation batches: 1
Test batches: 2
Building compact model for balanced training...
Training on balanced dataset...
Starting training on cpu...
Model parameters: 63,490
/home/user/.venvs/tensor_ml/lib/python3.12/site-packages/torch/nn/modules/transformer.py:533: UserWarning: The PyTorch API of nested tensors is in prototype stage and will change in the near future. We recommend specifying layout=torch.jagged when constructing a nested tensor, as this layout receives active development, has better operator coverage, and works with torch.compile. (Triggered internally at /__w/pytorch/pytorch/aten/src/ATen/NestedTensorImpl.cpp:177.)
  output = torch._nested_tensor_from_mask(
Epoch 1/10
  Train Loss: 0.7709, Train Acc: 48.57%
  Val Loss: 0.6801, Val Acc: 62.50%
  Learning Rate: 0.001000
Epoch 2/10
  Train Loss: 0.6827, Train Acc: 55.24%
  Val Loss: 0.6796, Val Acc: 62.50%
  Learning Rate: 0.001000
Epoch 3/10
  Train Loss: 0.6524, Train Acc: 64.76%
  Val Loss: 0.6798, Val Acc: 68.75%
  Learning Rate: 0.001000
Epoch 4/10
  Train Loss: 0.5881, Train Acc: 71.43%
  Val Loss: 0.6678, Val Acc: 68.75%
  Learning Rate: 0.001000
Epoch 5/10
  Train Loss: 0.4855, Train Acc: 80.00%
  Val Loss: 0.6592, Val Acc: 68.75%
  Learning Rate: 0.001000
Epoch 6/10
  Train Loss: 0.3992, Train Acc: 82.86%
  Val Loss: 0.6507, Val Acc: 75.00%
  Learning Rate: 0.001000
Epoch 7/10
  Train Loss: 0.2908, Train Acc: 84.76%
  Val Loss: 0.6324, Val Acc: 62.50%
  Learning Rate: 0.001000
Epoch 8/10
  Train Loss: 0.2254, Train Acc: 91.43%
  Val Loss: 0.6380, Val Acc: 56.25%
  Learning Rate: 0.001000
Epoch 9/10
  Train Loss: 0.1578, Train Acc: 95.24%
  Val Loss: 0.6199, Val Acc: 68.75%
  Learning Rate: 0.001000
Epoch 10/10
  Train Loss: 0.0811, Train Acc: 99.05%
  Val Loss: 0.6164, Val Acc: 75.00%
  Learning Rate: 0.001000

✓ Balanced training completed
Final validation accuracy: 75.00%

