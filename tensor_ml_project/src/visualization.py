"""
Visualization and Analysis for Tensor ML Operations
Production-ready visualization tools for ML model analysis and tensor insights
"""

import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional, Tuple
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA


class TensorVisualizer:
    """
    Advanced visualization tools for tensor operations and ML model analysis.
    """
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize tensor visualizer with plotting style.
        
        Args:
            style: matplotlib style to use
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('seaborn-v0_8-darkgrid')
        
        sns.set_palette("husl")
        self.colors = sns.color_palette("husl", 10)
    
    def plot_tensor_distribution(
        self,
        tensor: torch.Tensor,
        title: str = "Tensor Distribution",
        save_path: Optional[str] = None
    ) -> None:
        """
        Visualize distribution of tensor values.
        
        Args:
            tensor: Input tensor
            title: Plot title
            save_path: Optional path to save plot
        """
        # Convert to numpy for plotting
        if isinstance(tensor, torch.Tensor):
            data = tensor.cpu().numpy().flatten()
        else:
            data = tensor.flatten()
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        axes[0].hist(data, bins=50, alpha=0.7, edgecolor='black')
        axes[0].set_title(f'{title} - Histogram')
        axes[0].set_xlabel('Value')
        axes[0].set_ylabel('Frequency')
        axes[0].grid(True, alpha=0.3)
        
        # Box plot
        axes[1].boxplot(data, vert=True)
        axes[1].set_title(f'{title} - Box Plot')
        axes[1].set_ylabel('Value')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_attention_weights(
        self,
        attention_weights: torch.Tensor,
        tokens: Optional[List[str]] = None,
        title: str = "Attention Weights",
        save_path: Optional[str] = None
    ) -> None:
        """
        Visualize attention weights as a heatmap.
        
        Args:
            attention_weights: Attention weight tensor (seq_len, seq_len)
            tokens: Optional list of tokens for labels
            title: Plot title
            save_path: Optional path to save plot
        """
        if isinstance(attention_weights, torch.Tensor):
            attention_weights = attention_weights.cpu().numpy()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            attention_weights,
            cmap='viridis',
            xticklabels=tokens if tokens else False,
            yticklabels=tokens if tokens else False,
            cbar_kws={'label': 'Attention Weight'}
        )
        plt.title(title)
        plt.xlabel('Key Position')
        plt.ylabel('Query Position')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_tensor_statistics(
        self,
        tensors: Dict[str, torch.Tensor],
        save_path: Optional[str] = None
    ) -> None:
        """
        Compare statistics across multiple tensors.
        
        Args:
            tensors: Dictionary mapping names to tensors
            save_path: Optional path to save plot
        """
        stats_data = []
        
        for name, tensor in tensors.items():
            if isinstance(tensor, torch.Tensor):
                data = tensor.cpu().numpy().flatten()
            else:
                data = tensor.flatten()
            
            stats_data.append({
                'Tensor': name,
                'Mean': np.mean(data),
                'Std': np.std(data),
                'Min': np.min(data),
                'Max': np.max(data),
                'Median': np.median(data)
            })
        
        df = pd.DataFrame(stats_data)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Mean comparison
        axes[0, 0].bar(df['Tensor'], df['Mean'], color=self.colors[:len(df)])
        axes[0, 0].set_title('Mean Values')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # Std comparison
        axes[0, 1].bar(df['Tensor'], df['Std'], color=self.colors[:len(df)])
        axes[0, 1].set_title('Standard Deviation')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3)
        
        # Range comparison
        x_pos = np.arange(len(df))
        width = 0.35
        axes[1, 0].bar(x_pos - width/2, df['Min'], width, label='Min', color=self.colors[0])
        axes[1, 0].bar(x_pos + width/2, df['Max'], width, label='Max', color=self.colors[1])
        axes[1, 0].set_title('Value Range')
        axes[1, 0].set_xticks(x_pos)
        axes[1, 0].set_xticklabels(df['Tensor'])
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Statistics table
        axes[1, 1].axis('tight')
        axes[1, 1].axis('off')
        table = axes[1, 1].table(
            cellText=df.round(4).values,
            colLabels=df.columns,
            cellLoc='center',
            loc='center'
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.2)
        axes[1, 1].set_title('Statistics Summary')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_embedding_space(
        self,
        embeddings: torch.Tensor,
        labels: Optional[np.ndarray] = None,
        method: str = 'tsne',
        title: str = "Embedding Space Visualization",
        save_path: Optional[str] = None
    ) -> None:
        """
        Visualize high-dimensional embeddings in 2D space.
        
        Args:
            embeddings: Embedding tensor (n_samples, embedding_dim)
            labels: Optional labels for coloring
            method: Dimensionality reduction method ('tsne' or 'pca')
            title: Plot title
            save_path: Optional path to save plot
        """
        if isinstance(embeddings, torch.Tensor):
            embeddings = embeddings.cpu().numpy()
        
        # Apply dimensionality reduction
        if method.lower() == 'tsne':
            reducer = TSNE(n_components=2, random_state=42)
        elif method.lower() == 'pca':
            reducer = PCA(n_components=2)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        embeddings_2d = reducer.fit_transform(embeddings)
        
        plt.figure(figsize=(10, 8))
        
        if labels is not None:
            scatter = plt.scatter(
                embeddings_2d[:, 0],
                embeddings_2d[:, 1],
                c=labels,
                cmap='viridis',
                alpha=0.6,
                s=50
            )
            plt.colorbar(scatter, label='Class')
        else:
            plt.scatter(
                embeddings_2d[:, 0],
                embeddings_2d[:, 1],
                alpha=0.6,
                s=50,
                color=self.colors[0]
            )
        
        plt.title(f'{title} ({method.upper()})')
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_learning_curves(
        self,
        history: Dict[str, List[float]],
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot training and validation learning curves.
        
        Args:
            history: Dictionary containing training history
            save_path: Optional path to save plot
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        epochs = range(1, len(history['train_losses']) + 1)
        
        # Loss curves
        axes[0].plot(epochs, history['train_losses'], 'o-', label='Train Loss', color=self.colors[0])
        axes[0].plot(epochs, history['val_losses'], 's-', label='Val Loss', color=self.colors[1])
        axes[0].set_title('Learning Curves - Loss')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Loss')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Accuracy curves
        axes[1].plot(epochs, history['train_accuracies'], 'o-', label='Train Acc', color=self.colors[2])
        axes[1].plot(epochs, history['val_accuracies'], 's-', label='Val Acc', color=self.colors[3])
        axes[1].set_title('Learning Curves - Accuracy')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Accuracy (%)')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_gradient_flow(
        self,
        named_parameters: List[Tuple[str, torch.Tensor]],
        save_path: Optional[str] = None
    ) -> None:
        """
        Visualize gradient flow through the network.
        
        Args:
            named_parameters: List of (name, parameter) tuples
            save_path: Optional path to save plot
        """
        gradients = []
        names = []
        
        for name, param in named_parameters:
            if param.grad is not None:
                gradients.append(param.grad.cpu().numpy().flatten())
                names.append(name)
        
        if not gradients:
            print("No gradients to visualize")
            return
        
        plt.figure(figsize=(12, 6))
        
        # Gradient distribution plot
        plt.boxplot(gradients, labels=names)
        plt.title('Gradient Flow Distribution')
        plt.ylabel('Gradient Value')
        plt.xlabel('Layer')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_model_architecture(
        self,
        layer_sizes: List[int],
        layer_names: Optional[List[str]] = None,
        save_path: Optional[str] = None
    ) -> None:
        """
        Visualize neural network architecture.
        
        Args:
            layer_sizes: List of layer sizes
            layer_names: Optional list of layer names
            save_path: Optional path to save plot
        """
        if layer_names is None:
            layer_names = [f'Layer {i}' for i in range(len(layer_sizes))]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Calculate positions
        max_size = max(layer_sizes)
        x_positions = np.arange(len(layer_sizes))
        
        # Draw layers
        for i, (size, name) in enumerate(zip(layer_sizes, layer_names)):
            y_positions = np.arange(size)
            y_positions = y_positions - size / 2  # Center around 0
            
            # Draw neurons
            for y in y_positions:
                circle = plt.Circle((x_positions[i], y), 0.3, 
                                   color=self.colors[i % len(self.colors)], 
                                   alpha=0.7)
                ax.add_patch(circle)
            
            # Draw connections to next layer
            if i < len(layer_sizes) - 1:
                next_size = layer_sizes[i + 1]
                next_y = np.arange(next_size) - next_size / 2
                
                for y1 in y_positions:
                    for y2 in next_y:
                        ax.plot([x_positions[i], x_positions[i] + 1],
                               [y1, y2], 'gray', alpha=0.2, linewidth=0.5)
            
            # Label layer
            ax.text(x_positions[i], max_size / 2 + 1, name,
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_xlim(-0.5, len(layer_sizes) - 0.5)
        ax.set_ylim(-max_size / 2 - 1, max_size / 2 + 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Neural Network Architecture', fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()


class TensorAnalyzer:
    """
    Advanced analysis tools for tensor operations and ML models.
    """
    
    @staticmethod
    def analyze_tensor_properties(tensor: torch.Tensor) -> Dict[str, any]:
        """
        Analyze comprehensive properties of a tensor.
        
        Args:
            tensor: Input tensor
            
        Returns:
            Dictionary of tensor properties
        """
        if isinstance(tensor, torch.Tensor):
            data = tensor.cpu().numpy()
            device = str(tensor.device)
            dtype = str(tensor.dtype)
        else:
            data = tensor
            device = 'cpu'
            dtype = str(tensor.dtype)
        
        properties = {
            'shape': data.shape,
            'size': data.size,
            'device': device,
            'dtype': dtype,
            'mean': np.mean(data),
            'std': np.std(data),
            'min': np.min(data),
            'max': np.max(data),
            'median': np.median(data),
            'nnz': np.count_nonzero(data),
            'sparsity': 1.0 - (np.count_nonzero(data) / data.size),
            'memory_usage_mb': data.nbytes / (1024 * 1024)
        }
        
        return properties
    
    @staticmethod
    def compare_tensors(tensor1: torch.Tensor, tensor2: torch.Tensor) -> Dict[str, any]:
        """
        Compare two tensors comprehensively.
        
        Args:
            tensor1: First tensor
            tensor2: Second tensor
            
        Returns:
            Dictionary of comparison metrics
        """
        if isinstance(tensor1, torch.Tensor):
            tensor1 = tensor1.cpu().numpy()
        if isinstance(tensor2, torch.Tensor):
            tensor2 = tensor2.cpu().numpy()
        
        comparison = {
            'shape_equal': tensor1.shape == tensor2.shape,
            'mean_diff': np.mean(tensor1) - np.mean(tensor2),
            'std_diff': np.std(tensor1) - np.std(tensor2),
            'mse': np.mean((tensor1 - tensor2) ** 2),
            'mae': np.mean(np.abs(tensor1 - tensor2)),
            'cosine_similarity': np.dot(tensor1.flatten(), tensor2.flatten()) / 
                                (np.linalg.norm(tensor1) * np.linalg.norm(tensor2) + 1e-8)
        }
        
        return comparison
    
    @staticmethod
    def detect_anomalies(tensor: torch.Tensor, threshold: float = 3.0) -> Dict[str, any]:
        """
        Detect anomalies in tensor using statistical methods.
        
        Args:
            tensor: Input tensor
            threshold: Z-score threshold for anomaly detection
            
        Returns:
            Dictionary with anomaly information
        """
        if isinstance(tensor, torch.Tensor):
            data = tensor.cpu().numpy().flatten()
        else:
            data = tensor.flatten()
        
        mean = np.mean(data)
        std = np.std(data)
        z_scores = np.abs((data - mean) / std)
        
        anomalies = z_scores > threshold
        anomaly_indices = np.where(anomalies)[0]
        anomaly_values = data[anomalies]
        
        return {
            'total_anomalies': len(anomaly_indices),
            'anomaly_rate': len(anomaly_indices) / len(data),
            'anomaly_indices': anomaly_indices,
            'anomaly_values': anomaly_values,
            'max_z_score': np.max(z_scores),
            'mean_z_score': np.mean(z_scores)
        }


def demonstrate_visualization():
    """
    Demonstrate visualization and analysis capabilities.
    """
    print("=== Tensor Visualization and Analysis Demo ===\n")
    
    # Initialize visualizer
    visualizer = TensorVisualizer()
    analyzer = TensorAnalyzer()
    
    # Create sample tensors
    torch.manual_seed(42)
    tensor1 = torch.randn(100, 50)
    tensor2 = torch.randn(100, 50) * 0.5
    tensor3 = torch.randn(100, 50) + 2.0
    
    print("1. Tensor Properties Analysis:")
    props1 = analyzer.analyze_tensor_properties(tensor1)
    print(f"   Tensor 1 shape: {props1['shape']}")
    print(f"   Mean: {props1['mean']:.4f}, Std: {props1['std']:.4f}")
    print(f"   Memory usage: {props1['memory_usage_mb']:.2f} MB")
    print(f"   Sparsity: {props1['sparsity']:.2%}\n")
    
    print("2. Tensor Comparison:")
    comparison = analyzer.compare_tensors(tensor1, tensor2)
    print(f"   Shape equal: {comparison['shape_equal']}")
    print(f"   Mean difference: {comparison['mean_diff']:.4f}")
    print(f"   MSE: {comparison['mse']:.4f}")
    print(f"   Cosine similarity: {comparison['cosine_similarity']:.4f}\n")
    
    print("3. Anomaly Detection:")
    anomaly_tensor = torch.cat([torch.randn(95), torch.tensor([10, -10, 15, -15, 20])])
    anomalies = analyzer.detect_anomalies(anomaly_tensor)
    print(f"   Total anomalies: {anomalies['total_anomalies']}")
    print(f"   Anomaly rate: {anomalies['anomaly_rate']:.2%}")
    print(f"   Max Z-score: {anomalies['max_z_score']:.2f}\n")
    
    print("4. Sample Training History:")
    history = {
        'train_losses': [0.8, 0.6, 0.5, 0.4, 0.35, 0.3, 0.28],
        'val_losses': [0.85, 0.65, 0.55, 0.5, 0.48, 0.47, 0.46],
        'train_accuracies': [70, 75, 80, 82, 84, 85, 86],
        'val_accuracies': [68, 72, 76, 78, 79, 80, 80]
    }
    print("   Training progress over 7 epochs:")
    for i in range(len(history['train_losses'])):
        print(f"   Epoch {i+1}: Train Loss={history['train_losses'][i]:.3f}, "
              f"Val Acc={history['val_accuracies'][i]:.1f}%")
    
    print("\n5. Sample Embedding Statistics:")
    embeddings = torch.randn(100, 128)
    embedding_props = analyzer.analyze_tensor_properties(embeddings)
    print(f"   Embedding shape: {embedding_props['shape']}")
    print(f"   Mean: {embedding_props['mean']:.4f}")
    print(f"   Memory per embedding: {embedding_props['memory_usage_mb']/100:.3f} MB\n")
    
    print("=== Visualization and Analysis Demo Complete ===")
    print("Note: Actual plots would be displayed when running in interactive mode")


if __name__ == "__main__":
    demonstrate_visualization()
