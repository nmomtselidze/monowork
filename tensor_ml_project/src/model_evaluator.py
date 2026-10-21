"""
Model Training and Evaluation System
Production-ready evaluation pipeline with comprehensive metrics and analysis
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns
from torch.utils.data import DataLoader


class ModelEvaluator:
    """
    Comprehensive model evaluation with production-grade metrics.
    """
    
    def __init__(self, model: nn.Module, device: str = 'cpu'):
        """
        Initialize model evaluator.
        
        Args:
            model: PyTorch model to evaluate
            device: Device for evaluation
        """
        self.model = model.to(device)
        self.device = device
        self.model.eval()
    
    def predict(self, data_loader: DataLoader) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate predictions from data loader.
        
        Args:
            data_loader: DataLoader for evaluation data
            
        Returns:
            Tuple of (predictions, true_labels)
        """
        all_predictions = []
        all_labels = []
        all_probabilities = []
        
        with torch.no_grad():
            for batch in data_loader:
                if len(batch) == 2:
                    inputs, labels = batch
                    mask = None
                else:
                    inputs, labels, mask = batch
                
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)
                
                if mask is not None:
                    mask = mask.to(self.device)
                    outputs = self.model(inputs, mask)
                else:
                    outputs = self.model(inputs)
                
                probabilities = torch.softmax(outputs, dim=1)
                predictions = torch.argmax(outputs, dim=1)
                
                all_predictions.extend(predictions.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
                all_probabilities.extend(probabilities.cpu().numpy())
        
        return np.array(all_predictions), np.array(all_labels), np.array(all_probabilities)
    
    def compute_metrics(
        self, 
        y_true: np.ndarray, 
        y_pred: np.ndarray,
        y_prob: Optional[np.ndarray] = None
    ) -> Dict[str, float]:
        """
        Compute comprehensive evaluation metrics.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_prob: Prediction probabilities (optional, for ROC-AUC)
            
        Returns:
            Dictionary of metrics
        """
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision_macro': precision_score(y_true, y_pred, average='macro', zero_division=0),
            'recall_macro': recall_score(y_true, y_pred, average='macro', zero_division=0),
            'f1_macro': f1_score(y_true, y_pred, average='macro', zero_division=0),
            'precision_weighted': precision_score(y_true, y_pred, average='weighted', zero_division=0),
            'recall_weighted': recall_score(y_true, y_pred, average='weighted', zero_division=0),
            'f1_weighted': f1_score(y_true, y_pred, average='weighted', zero_division=0),
        }
        
        # Add ROC-AUC if probabilities available and binary classification
        if y_prob is not None and len(np.unique(y_true)) == 2:
            metrics['roc_auc'] = roc_auc_score(y_true, y_prob[:, 1])
        
        return metrics
    
    def generate_confusion_matrix(
        self, 
        y_true: np.ndarray, 
        y_pred: np.ndarray,
        class_names: Optional[List[str]] = None
    ) -> np.ndarray:
        """
        Generate confusion matrix.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            class_names: Optional class names for labeling
            
        Returns:
            Confusion matrix
        """
        cm = confusion_matrix(y_true, y_pred)
        return cm
    
    def plot_confusion_matrix(
        self, 
        y_true: np.ndarray, 
        y_pred: np.ndarray,
        class_names: Optional[List[str]] = None,
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot confusion matrix with seaborn.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            class_names: Optional class names
            save_path: Optional path to save the plot
        """
        cm = self.generate_confusion_matrix(y_true, y_pred, class_names)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=class_names, yticklabels=class_names)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_training_history(
        self, 
        history: Dict[str, List[float]],
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot training history (loss and accuracy).
        
        Args:
            history: Dictionary containing training history
            save_path: Optional path to save the plot
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot loss
        axes[0].plot(history['train_losses'], label='Train Loss', marker='o')
        axes[0].plot(history['val_losses'], label='Validation Loss', marker='s')
        axes[0].set_title('Model Loss')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Loss')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Plot accuracy
        axes[1].plot(history['train_accuracies'], label='Train Accuracy', marker='o')
        axes[1].plot(history['val_accuracies'], label='Validation Accuracy', marker='s')
        axes[1].set_title('Model Accuracy')
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
    
    def plot_roc_curve(
        self,
        y_true: np.ndarray,
        y_prob: np.ndarray,
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot ROC curve for binary classification.
        
        Args:
            y_true: True labels
            y_prob: Prediction probabilities
            save_path: Optional path to save the plot
        """
        fpr, tpr, thresholds = roc_curve(y_true, y_prob[:, 1])
        auc_score = roc_auc_score(y_true, y_prob[:, 1])
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc_score:.3f})')
        plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def generate_evaluation_report(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        class_names: Optional[List[str]] = None
    ) -> str:
        """
        Generate comprehensive evaluation report.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            class_names: Optional class names
            
        Returns:
            Formatted evaluation report string
        """
        report = classification_report(y_true, y_pred, target_names=class_names)
        return report
    
    def analyze_errors(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        data: Optional[np.ndarray] = None
    ) -> Dict[str, any]:
        """
        Analyze prediction errors.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            data: Optional original data for error analysis
            
        Returns:
            Dictionary containing error analysis
        """
        errors = y_true != y_pred
        error_indices = np.where(errors)[0]
        
        analysis = {
            'total_errors': len(error_indices),
            'error_rate': len(error_indices) / len(y_true),
            'error_indices': error_indices,
        }
        
        # Error distribution by class
        unique_classes = np.unique(y_true)
        class_errors = {}
        for cls in unique_classes:
            class_mask = y_true == cls
            class_error_count = np.sum(errors[class_mask])
            class_total = np.sum(class_mask)
            class_errors[int(cls)] = {
                'errors': class_error_count,
                'total': class_total,
                'error_rate': class_error_count / class_total if class_total > 0 else 0
            }
        
        analysis['class_errors'] = class_errors
        
        return analysis
    
    def compare_models(
        self,
        model_metrics: Dict[str, Dict[str, float]]
    ) -> None:
        """
        Compare multiple models based on metrics.
        
        Args:
            model_metrics: Dictionary mapping model names to their metrics
        """
        print("=== Model Comparison ===\n")
        
        # Create comparison table
        metric_names = list(next(iter(model_metrics.values())).keys())
        
        print(f"{'Model':<20}", end='')
        for metric in metric_names:
            print(f"{metric:<20}", end='')
        print()
        
        for model_name, metrics in model_metrics.items():
            print(f"{model_name:<20}", end='')
            for metric in metric_names:
                value = metrics.get(metric, 0)
                print(f"{value:<20.4f}", end='')
            print()
        
        # Find best model for each metric
        print("\n=== Best Models by Metric ===")
        for metric in metric_names:
            best_model = max(model_metrics.items(), key=lambda x: x[1].get(metric, 0))
            print(f"{metric}: {best_model[0]} ({best_model[1][metric]:.4f})")


class ProductionTrainer:
    """
    Production-ready training pipeline with advanced features.
    """
    
    def __init__(
        self,
        model: nn.Module,
        device: str = 'cpu',
        learning_rate: float = 0.001,
        weight_decay: float = 0.01,
        gradient_clip: float = 1.0
    ):
        """
        Initialize production trainer.
        
        Args:
            model: PyTorch model
            device: Device for training
            learning_rate: Learning rate
            weight_decay: Weight decay for regularization
            gradient_clip: Gradient clipping threshold
        """
        self.model = model.to(device)
        self.device = device
        self.gradient_clip = gradient_clip
        
        self.optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay
        )
        
        self.criterion = nn.CrossEntropyLoss()
        
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer,
            mode='min',
            factor=0.5,
            patience=2
        )
        
        self.history = {
            'train_losses': [],
            'val_losses': [],
            'train_accuracies': [],
            'val_accuracies': []
        }
    
    def train_epoch(self, train_loader: DataLoader) -> Tuple[float, float]:
        """Train for one epoch with gradient accumulation support."""
        self.model.train()
        total_loss = 0.0
        correct = 0
        total = 0
        
        for batch in train_loader:
            if len(batch) == 2:
                inputs, labels = batch
                mask = None
            else:
                inputs, labels, mask = batch
            
            inputs = inputs.to(self.device)
            labels = labels.to(self.device)
            
            if mask is not None:
                mask = mask.to(self.device)
            
            self.optimizer.zero_grad()
            
            if mask is not None:
                outputs = self.model(inputs, mask)
            else:
                outputs = self.model(inputs)
            
            loss = self.criterion(outputs, labels)
            loss.backward()
            
            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.gradient_clip)
            
            self.optimizer.step()
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        avg_loss = total_loss / len(train_loader)
        accuracy = 100.0 * correct / total
        
        return avg_loss, accuracy
    
    def validate(self, val_loader: DataLoader) -> Tuple[float, float]:
        """Validate the model."""
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for batch in val_loader:
                if len(batch) == 2:
                    inputs, labels = batch
                    mask = None
                else:
                    inputs, labels, mask = batch
                
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)
                
                if mask is not None:
                    mask = mask.to(self.device)
                
                if mask is not None:
                    outputs = self.model(inputs, mask)
                else:
                    outputs = self.model(inputs)
                
                loss = self.criterion(outputs, labels)
                
                total_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        avg_loss = total_loss / len(val_loader)
        accuracy = 100.0 * correct / total
        
        return avg_loss, accuracy
    
    def train(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader,
        epochs: int = 10,
        patience: int = 3,
        verbose: bool = True
    ) -> Dict[str, List[float]]:
        """
        Complete training loop with early stopping.
        
        Args:
            train_loader: Training data loader
            val_loader: Validation data loader
            epochs: Maximum number of epochs
            patience: Early stopping patience
            verbose: Whether to print progress
            
        Returns:
            Training history
        """
        best_val_loss = float('inf')
        patience_counter = 0
        
        if verbose:
            print(f"Training on {self.device}")
            print(f"Model parameters: {sum(p.numel() for p in self.model.parameters()):,}")
        
        for epoch in range(epochs):
            train_loss, train_acc = self.train_epoch(train_loader)
            val_loss, val_acc = self.validate(val_loader)
            
            self.history['train_losses'].append(train_loss)
            self.history['val_losses'].append(val_loss)
            self.history['train_accuracies'].append(train_acc)
            self.history['val_accuracies'].append(val_acc)
            
            self.scheduler.step(val_loss)
            
            if verbose:
                print(f"Epoch {epoch+1}/{epochs}")
                print(f"  Train Loss: {train_loss:.4f}, Acc: {train_acc:.2f}%")
                print(f"  Val Loss: {val_loss:.4f}, Acc: {val_acc:.2f}%")
                print(f"  LR: {self.optimizer.param_groups[0]['lr']:.6f}")
            
            # Early stopping and model saving
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                torch.save(self.model.state_dict(), 'best_model.pt')
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    if verbose:
                        print(f"Early stopping at epoch {epoch+1}")
                    break
        
        return self.history


def demonstrate_evaluation():
    """
    Demonstrate model evaluation capabilities.
    """
    print("=== Model Evaluation Demonstration ===\n")
    
    # Create dummy data for demonstration
    np.random.seed(42)
    y_true = np.random.randint(0, 2, 100)
    y_pred = np.random.randint(0, 2, 100)
    y_prob = np.random.rand(100, 2)
    y_prob = y_prob / y_prob.sum(axis=1, keepdims=True)  # Normalize
    
    # Create evaluator
    class DummyModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = nn.Linear(10, 2)
        
        def forward(self, x):
            return self.linear(x)
    
    model = DummyModel()
    evaluator = ModelEvaluator(model, device='cpu')
    
    # Compute metrics
    metrics = evaluator.compute_metrics(y_true, y_pred, y_prob)
    print("1. Computed Metrics:")
    for metric, value in metrics.items():
        print(f"   {metric}: {value:.4f}")
    
    # Generate confusion matrix
    print("\n2. Confusion Matrix:")
    cm = evaluator.generate_confusion_matrix(y_true, y_pred, class_names=['Negative', 'Positive'])
    print(cm)
    
    # Error analysis
    print("\n3. Error Analysis:")
    error_analysis = evaluator.analyze_errors(y_true, y_pred)
    print(f"   Total errors: {error_analysis['total_errors']}")
    print(f"   Error rate: {error_analysis['error_rate']:.2%}")
    
    # Compare models
    print("\n4. Model Comparison:")
    model_metrics = {
        'Model A': {'accuracy': 0.85, 'f1_macro': 0.82, 'precision_macro': 0.84},
        'Model B': {'accuracy': 0.88, 'f1_macro': 0.86, 'precision_macro': 0.87},
        'Model C': {'accuracy': 0.82, 'f1_macro': 0.80, 'precision_macro': 0.81}
    }
    evaluator.compare_models(model_metrics)
    
    print("\n=== Evaluation Demo Complete ===")


if __name__ == "__main__":
    demonstrate_evaluation()
