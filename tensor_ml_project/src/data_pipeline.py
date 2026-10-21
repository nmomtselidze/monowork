"""
Data Preprocessing Pipeline for ML Applications
Demonstrates production-ready data engineering with tensor operations
"""

import torch
import numpy as np
import pandas as pd
from typing import List, Tuple, Optional, Union
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import re
from collections import Counter


class DataPreprocessor:
    """
    Comprehensive data preprocessing pipeline for ML applications.
    Handles text, numerical, and categorical data with tensor optimizations.
    """
    
    def __init__(self, device: str = 'cpu'):
        """
        Initialize data preprocessor.
        
        Args:
            device: Device for tensor operations
        """
        self.device = torch.device(device)
        self.scalers = {}
        self.encoders = {}
        self.vocabs = {}
        self.fitted = False
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text data.
        
        Args:
            text: Raw text string
            
        Returns:
            Cleaned text string
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_text(self, text: str, max_length: Optional[int] = None) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text: Input text
            max_length: Maximum number of tokens to return
            
        Returns:
            List of tokens
        """
        tokens = text.split()
        if max_length and len(tokens) > max_length:
            tokens = tokens[:max_length]
        return tokens
    
    def build_vocabulary(
        self, 
        texts: List[str], 
        min_freq: int = 2,
        max_vocab_size: Optional[int] = None
    ) -> dict:
        """
        Build vocabulary from text corpus.
        
        Args:
            texts: List of text samples
            min_freq: Minimum frequency for word inclusion
            max_vocab_size: Maximum vocabulary size
            
        Returns:
            Vocabulary dictionary mapping words to indices
        """
        word_freq = Counter()
        
        for text in texts:
            cleaned_text = self.clean_text(text)
            tokens = self.tokenize_text(cleaned_text)
            word_freq.update(tokens)
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Build vocabulary
        vocab = {'<PAD>': 0, '<UNK>': 1}
        idx = 2
        
        for word, freq in sorted_words:
            if freq >= min_freq:
                if max_vocab_size and idx >= max_vocab_size:
                    break
                vocab[word] = idx
                idx += 1
        
        return vocab
    
    def text_to_tensor(
        self, 
        text: str, 
        vocab: dict, 
        max_length: int = 128
    ) -> torch.Tensor:
        """
        Convert text to tensor using vocabulary.
        
        Args:
            text: Input text
            vocab: Vocabulary dictionary
            max_length: Maximum sequence length
            
        Returns:
            Tensor of indices
        """
        cleaned_text = self.clean_text(text)
        tokens = self.tokenize_text(cleaned_text, max_length)
        
        indices = [vocab.get(token, vocab['<UNK>']) for token in tokens]
        
        # Pad sequence
        if len(indices) < max_length:
            indices = indices + [vocab['<PAD>']] * (max_length - len(indices))
        
        return torch.tensor(indices, dtype=torch.long, device=self.device)
    
    def handle_missing_values(
        self, 
        data: Union[pd.DataFrame, np.ndarray],
        strategy: str = 'mean'
    ) -> Union[pd.DataFrame, np.ndarray]:
        """
        Handle missing values in data.
        
        Args:
            data: Input data
            strategy: 'mean', 'median', 'mode', or 'drop'
            
        Returns:
            Data with missing values handled
        """
        if isinstance(data, pd.DataFrame):
            if strategy == 'drop':
                return data.dropna()
            elif strategy == 'mean':
                return data.fillna(data.mean())
            elif strategy == 'median':
                return data.fillna(data.median())
            elif strategy == 'mode':
                return data.fillna(data.mode().iloc[0])
        else:
            # For numpy arrays
            if strategy == 'drop':
                mask = ~np.isnan(data).any(axis=1)
                return data[mask]
            elif strategy == 'mean':
                col_means = np.nanmean(data, axis=0)
                return np.where(np.isnan(data), col_means, data)
            elif strategy == 'median':
                col_medians = np.nanmedian(data, axis=0)
                return np.where(np.isnan(data), col_medians, data)
        
        return data
    
    def normalize_numerical(
        self, 
        data: np.ndarray, 
        fit: bool = True,
        feature_name: str = 'default'
    ) -> torch.Tensor:
        """
        Normalize numerical data using standardization.
        
        Args:
            data: Input numerical data
            fit: Whether to fit the scaler
            feature_name: Name for storing the scaler
            
        Returns:
            Normalized tensor
        """
        if fit:
            scaler = StandardScaler()
            normalized = scaler.fit_transform(data)
            self.scalers[feature_name] = scaler
        else:
            scaler = self.scalers.get(feature_name)
            if scaler is None:
                raise ValueError(f"Scaler for {feature_name} not found. Call with fit=True first.")
            normalized = scaler.transform(data)
        
        return torch.tensor(normalized, dtype=torch.float32, device=self.device)
    
    def encode_categorical(
        self, 
        data: np.ndarray, 
        fit: bool = True,
        feature_name: str = 'default'
    ) -> torch.Tensor:
        """
        Encode categorical data using label encoding.
        
        Args:
            data: Input categorical data
            fit: Whether to fit the encoder
            feature_name: Name for storing the encoder
            
        Returns:
            Encoded tensor
        """
        if fit:
            encoder = LabelEncoder()
            encoded = encoder.fit_transform(data)
            self.encoders[feature_name] = encoder
        else:
            encoder = self.encoders.get(feature_name)
            if encoder is None:
                raise ValueError(f"Encoder for {feature_name} not found. Call with fit=True first.")
            encoded = encoder.transform(data)
        
        return torch.tensor(encoded, dtype=torch.long, device=self.device)
    
    def create_attention_mask(self, tensor: torch.Tensor, pad_idx: int = 0) -> torch.Tensor:
        """
        Create attention mask for padded sequences.
        
        Args:
            tensor: Input tensor
            pad_idx: Padding index
            
        Returns:
            Boolean mask tensor
        """
        return (tensor != pad_idx).to(self.device)
    
    def create_data_loader(
        self,
        features: torch.Tensor,
        labels: torch.Tensor,
        batch_size: int = 32,
        shuffle: bool = True
    ) -> torch.utils.data.DataLoader:
        """
        Create PyTorch DataLoader from tensors.
        
        Args:
            features: Feature tensor
            labels: Label tensor
            batch_size: Batch size
            shuffle: Whether to shuffle data
            
        Returns:
            DataLoader instance
        """
        if not isinstance(features, torch.Tensor):
            features = torch.tensor(features, dtype=torch.long)
        if not isinstance(labels, torch.Tensor):
            labels = torch.tensor(labels, dtype=torch.long)
        dataset = torch.utils.data.TensorDataset(features, labels)
        return torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    
    def split_data(
        self,
        features: Union[np.ndarray, torch.Tensor],
        labels: Union[np.ndarray, torch.Tensor],
        test_size: float = 0.2,
        val_size: float = 0.1,
        random_state: int = 42
    ) -> Tuple:
        """
        Split data into train, validation, and test sets.
        
        Args:
            features: Feature data
            labels: Label data
            test_size: Proportion of test data
            val_size: Proportion of validation data
            random_state: Random seed
            
        Returns:
            Tuple of (X_train, X_val, X_test, y_train, y_val, y_test)
        """
        # Convert to numpy if needed
        if isinstance(features, torch.Tensor):
            features = features.cpu().numpy()
        if isinstance(labels, torch.Tensor):
            labels = labels.cpu().numpy()
        
        # First split: train+val vs test
        X_temp, X_test, y_temp, y_test = train_test_split(
            features, labels, test_size=test_size, random_state=random_state
        )
        
        # Second split: train vs val
        val_ratio = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_ratio, random_state=random_state
        )
        
        return X_train, X_val, X_test, y_train, y_val, y_test


class TensorDataPipeline:
    """
    End-to-end data pipeline with tensor engineering optimizations.
    """
    
    def __init__(self, preprocessor: DataPreprocessor):
        """
        Initialize tensor data pipeline.
        
        Args:
            preprocessor: DataPreprocessor instance
        """
        self.preprocessor = preprocessor
    
    def process_text_classification_data(
        self,
        texts: List[str],
        labels: List[int],
        max_length: int = 128,
        test_size: float = 0.2,
        val_size: float = 0.1
    ) -> dict:
        """
        Complete pipeline for text classification data.
        
        Args:
            texts: List of text samples
            labels: List of labels
            max_length: Maximum sequence length
            test_size: Test set proportion
            val_size: Validation set proportion
            
        Returns:
            Dictionary containing processed data and metadata
        """
        # Build vocabulary
        vocab = self.preprocessor.build_vocabulary(texts, min_freq=2)
        self.preprocessor.vocabs['text'] = vocab
        
        # Convert texts to tensors
        text_tensors = torch.stack([
            self.preprocessor.text_to_tensor(text, vocab, max_length)
            for text in texts
        ])
        
        # Convert labels to tensors
        label_tensor = torch.tensor(labels, dtype=torch.long, device=self.preprocessor.device)
        
        # Split data
        splits = self.preprocessor.split_data(
            text_tensors, label_tensor, test_size, val_size
        )
        
        X_train, X_val, X_test, y_train, y_val, y_test = splits
        
        # Create data loaders
        train_loader = self.preprocessor.create_data_loader(X_train, y_train, batch_size=16, shuffle=True)
        val_loader = self.preprocessor.create_data_loader(X_val, y_val, batch_size=16, shuffle=False)
        test_loader = self.preprocessor.create_data_loader(X_test, y_test, batch_size=16, shuffle=False)
        
        return {
            'train_loader': train_loader,
            'val_loader': val_loader,
            'test_loader': test_loader,
            'vocab': vocab,
            'vocab_size': len(vocab),
            'num_classes': len(set(labels)),
            'max_length': max_length
        }
    
    def process_numerical_data(
        self,
        features: np.ndarray,
        labels: np.ndarray,
        test_size: float = 0.2,
        val_size: float = 0.1
    ) -> dict:
        """
        Complete pipeline for numerical data.
        
        Args:
            features: Numerical feature array
            labels: Label array
            test_size: Test set proportion
            val_size: Validation set proportion
            
        Returns:
            Dictionary containing processed data and metadata
        """
        # Handle missing values
        features = self.preprocessor.handle_missing_values(features, strategy='mean')
        
        # Split data
        X_train, X_val, X_test, y_train, y_val, y_test = self.preprocessor.split_data(
            features, labels, test_size, val_size
        )
        
        # Normalize features
        X_train_norm = self.preprocessor.normalize_numerical(X_train, fit=True, feature_name='features')
        X_val_norm = self.preprocessor.normalize_numerical(X_val, fit=False, feature_name='features')
        X_test_norm = self.preprocessor.normalize_numerical(X_test, fit=False, feature_name='features')
        
        # Convert labels to tensors
        y_train_tensor = torch.tensor(y_train, dtype=torch.long, device=self.preprocessor.device)
        y_val_tensor = torch.tensor(y_val, dtype=torch.long, device=self.preprocessor.device)
        y_test_tensor = torch.tensor(y_test, dtype=torch.long, device=self.preprocessor.device)
        
        # Create data loaders
        train_loader = self.preprocessor.create_data_loader(X_train_norm, y_train_tensor, batch_size=32, shuffle=True)
        val_loader = self.preprocessor.create_data_loader(X_val_norm, y_val_tensor, batch_size=32, shuffle=False)
        test_loader = self.preprocessor.create_data_loader(X_test_norm, y_test_tensor, batch_size=32, shuffle=False)
        
        return {
            'train_loader': train_loader,
            'val_loader': val_loader,
            'test_loader': test_loader,
            'num_features': X_train.shape[1],
            'num_classes': len(set(labels))
        }


def demonstrate_data_pipeline():
    """
    Demonstrate the data preprocessing pipeline.
    """
    print("=== Data Preprocessing Pipeline Demonstration ===\n")
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor(device='cpu')
    pipeline = TensorDataPipeline(preprocessor)
    
    # Sample text data
    texts = [
        "This product is amazing and I love it!",
        "Terrible quality, would not recommend",
        "Great service and fast delivery",
        "Worst purchase ever made",
        "Outstanding performance and features",
        "Poor customer support experience"
    ]
    labels = [1, 0, 1, 0, 1, 0]
    
    print("1. Text Classification Pipeline:")
    print(f"   Input texts: {len(texts)}")
    print(f"   Labels: {set(labels)}")
    
    # Process text data
    text_data = pipeline.process_text_classification_data(
        texts, labels, max_length=16, test_size=0.3, val_size=0.1
    )
    
    print(f"   Vocabulary size: {text_data['vocab_size']}")
    print(f"   Number of classes: {text_data['num_classes']}")
    print(f"   Train batches: {len(text_data['train_loader'])}")
    print(f"   Validation batches: {len(text_data['val_loader'])}")
    print(f"   Test batches: {len(text_data['test_loader'])}\n")
    
    # Sample numerical data
    print("2. Numerical Data Pipeline:")
    np.random.seed(42)
    features = np.random.randn(100, 5)  # 100 samples, 5 features
    labels = np.random.randint(0, 2, 100)  # Binary classification
    
    print(f"   Input features shape: {features.shape}")
    print(f"   Labels shape: {labels.shape}")
    
    # Process numerical data
    numerical_data = pipeline.process_numerical_data(
        features, labels, test_size=0.2, val_size=0.1
    )
    
    print(f"   Number of features: {numerical_data['num_features']}")
    print(f"   Number of classes: {numerical_data['num_classes']}")
    print(f"   Train batches: {len(numerical_data['train_loader'])}")
    print(f"   Validation batches: {len(numerical_data['val_loader'])}")
    print(f"   Test batches: {len(numerical_data['test_loader'])}\n")
    
    print("=== Data Pipeline Demo Complete ===")


if __name__ == "__main__":
    demonstrate_data_pipeline()
