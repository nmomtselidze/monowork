"""
Advanced Tensor Operations for Machine Learning
Demonstrates tensor engineering techniques used in production ML systems
"""

import torch
import numpy as np
from typing import Tuple, Optional, List
import torch.nn.functional as F


class TensorEngineer:
    """
    Advanced tensor operations for efficient ML computations.
    Demonstrates tensor engineering techniques relevant to production AI systems.
    """
    
    def __init__(self, device: str = 'cpu'):
        """
        Initialize tensor engineer with specified device.
        
        Args:
            device: 'cpu' or 'cuda' for GPU acceleration
        """
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        print(f"TensorEngineer initialized on device: {self.device}")
    
    def create_attention_mask(self, seq_len: int, batch_size: int = 1) -> torch.Tensor:
        """
        Create causal attention mask for transformer models.
        
        Args:
            seq_len: Length of the sequence
            batch_size: Batch size for the mask
            
        Returns:
            Boolean tensor mask where True indicates valid attention positions
        """
        mask = torch.tril(torch.ones(seq_len, seq_len, device=self.device))
        mask = mask.unsqueeze(0).expand(batch_size, -1, -1)
        return mask.bool()
    
    def scaled_dot_product_attention(
        self, 
        query: torch.Tensor, 
        key: torch.Tensor, 
        value: torch.Tensor,
        mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Implement scaled dot-product attention mechanism.
        
        Args:
            query: Query tensor of shape (batch_size, seq_len, d_k)
            key: Key tensor of shape (batch_size, seq_len, d_k)
            value: Value tensor of shape (batch_size, seq_len, d_v)
            mask: Optional attention mask
            
        Returns:
            Tuple of (output, attention_weights)
        """
        d_k = query.size(-1)
        scores = torch.matmul(query, key.transpose(-2, -1)) / np.sqrt(d_k)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        attention_weights = F.softmax(scores, dim=-1)
        output = torch.matmul(attention_weights, value)
        
        return output, attention_weights
    
    def positional_encoding(self, seq_len: int, d_model: int) -> torch.Tensor:
        """
        Generate sinusoidal positional encoding for transformer models.
        
        Args:
            seq_len: Maximum sequence length
            d_model: Dimension of the model
            
        Returns:
            Positional encoding tensor of shape (seq_len, d_model)
        """
        position = torch.arange(seq_len, dtype=torch.float, device=self.device).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2, dtype=torch.float, device=self.device) * 
                             (-np.log(10000.0) / d_model))
        
        pe = torch.zeros(seq_len, d_model, device=self.device)
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        return pe.unsqueeze(0)
    
    def tensor_memory_optimization(self, tensor: torch.Tensor) -> torch.Tensor:
        """
        Optimize tensor memory usage through techniques like quantization.
        
        Args:
            tensor: Input tensor to optimize
            
        Returns:
            Optimized tensor with reduced memory footprint
        """
        # Convert to half precision if on GPU
        if self.device.type == 'cuda':
            return tensor.half()
        return tensor
    
    def batch_tensor_operations(
        self, 
        tensors: List[torch.Tensor], 
        operation: str = 'stack'
    ) -> torch.Tensor:
        """
        Perform efficient batch operations on multiple tensors.
        
        Args:
            tensors: List of tensors to batch
            operation: 'stack', 'concat', or 'mean'
            
        Returns:
            Batched tensor result
        """
        if operation == 'stack':
            return torch.stack(tensors)
        elif operation == 'concat':
            return torch.cat(tensors)
        elif operation == 'mean':
            return torch.mean(torch.stack(tensors), dim=0)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    def gradient_accumulation_step(
        self, 
        loss: torch.Tensor, 
        optimizer: torch.optim.Optimizer,
        accumulation_steps: int,
        step: int
    ) -> None:
        """
        Implement gradient accumulation for larger effective batch sizes.
        
        Args:
            loss: Computed loss tensor
            optimizer: PyTorch optimizer
            accumulation_steps: Number of steps to accumulate gradients
            step: Current step number
        """
        loss = loss / accumulation_steps
        loss.backward()
        
        if (step + 1) % accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()
    
    def tensor_normalization(
        self, 
        tensor: torch.Tensor, 
        dim: int = -1,
        eps: float = 1e-5
    ) -> torch.Tensor:
        """
        Implement layer normalization for tensor stability.
        
        Args:
            tensor: Input tensor
            dim: Dimension to normalize over
            eps: Small constant for numerical stability
            
        Returns:
            Normalized tensor
        """
        mean = tensor.mean(dim=dim, keepdim=True)
        std = tensor.std(dim=dim, keepdim=True)
        return (tensor - mean) / (std + eps)
    
    def create_tensor_pipeline(
        self, 
        input_data: np.ndarray,
        preprocessing_steps: List[str] = ['normalize', 'to_tensor', 'to_device']
    ) -> torch.Tensor:
        """
        Create a tensor preprocessing pipeline.
        
        Args:
            input_data: NumPy array input
            preprocessing_steps: List of preprocessing operations
            
        Returns:
            Processed tensor ready for model input
        """
        tensor = torch.from_numpy(input_data).float()
        
        for step in preprocessing_steps:
            if step == 'normalize':
                tensor = self.tensor_normalization(tensor)
            elif step == 'to_tensor':
                pass  # Already converted
            elif step == 'to_device':
                tensor = tensor.to(self.device)
        
        return tensor


def demonstrate_tensor_operations():
    """
    Demonstrate various tensor operations with examples.
    """
    print("=== Tensor Engineering Demonstration ===\n")
    
    # Initialize tensor engineer
    engineer = TensorEngineer()
    
    # 1. Basic tensor creation and operations
    print("1. Basic Tensor Operations:")
    tensor_a = torch.randn(3, 4)
    tensor_b = torch.randn(3, 4)
    print(f"   Tensor A shape: {tensor_a.shape}")
    print(f"   Element-wise multiplication: {(tensor_a * tensor_b).shape}")
    print(f"   Matrix multiplication: {torch.matmul(tensor_a, tensor_b.T).shape}\n")
    
    # 2. Attention mechanisms
    print("2. Attention Mechanism:")
    seq_len, d_model = 10, 64
    query = torch.randn(1, seq_len, d_model)
    key = torch.randn(1, seq_len, d_model)
    value = torch.randn(1, seq_len, d_model)
    
    mask = engineer.create_attention_mask(seq_len, batch_size=1)
    output, attention_weights = engineer.scaled_dot_product_attention(query, key, value, mask)
    print(f"   Attention output shape: {output.shape}")
    print(f"   Attention weights shape: {attention_weights.shape}\n")
    
    # 3. Positional encoding
    print("3. Positional Encoding:")
    pos_encoding = engineer.positional_encoding(seq_len, d_model)
    print(f"   Positional encoding shape: {pos_encoding.shape}")
    print(f"   First position encoding (first 5 dims): {pos_encoding[0, 0, :5]}\n")
    
    # 4. Tensor normalization
    print("4. Tensor Normalization:")
    unnormalized = torch.randn(2, 5, 10)
    normalized = engineer.tensor_normalization(unnormalized, dim=-1)
    print(f"   Original mean: {unnormalized.mean().item():.4f}, std: {unnormalized.std().item():.4f}")
    print(f"   Normalized mean: {normalized.mean().item():.4f}, std: {normalized.std().item():.4f}\n")
    
    # 5. Memory optimization
    print("5. Memory Optimization:")
    large_tensor = torch.randn(1000, 1000)
    optimized = engineer.tensor_memory_optimization(large_tensor)
    print(f"   Original dtype: {large_tensor.dtype}")
    print(f"   Optimized dtype: {optimized.dtype}")
    print(f"   Memory reduction: {large_tensor.element_size() / optimized.element_size():.1f}x\n")
    
    print("=== Tensor Engineering Demo Complete ===")


if __name__ == "__main__":
    demonstrate_tensor_operations()
