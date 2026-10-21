"""
Real Data Loading Script for Tensor ML Project
Handles loading and preprocessing of real sentiment analysis datasets
"""

import pandas as pd
import numpy as np
import torch
from typing import Tuple, List, Optional
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_pipeline import DataPreprocessor, TensorDataPipeline


class RealDataLoader:
    """
    Load and preprocess real sentiment analysis datasets.
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize real data loader.
        
        Args:
            data_dir: Directory containing data files
        """
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__))
        
        self.data_dir = data_dir
        self.preprocessor = DataPreprocessor(device='cpu')
        self.pipeline = TensorDataPipeline(self.preprocessor)
    
    def load_sentiment_csv(
        self,
        filename: str = "sentiment_dataset.csv",
        text_column: str = "text",
        label_column: str = "label"
    ) -> Tuple[List[str], List[int]]:
        """
        Load sentiment data from CSV file.
        
        Args:
            filename: Name of the CSV file
            text_column: Column name for text data
            label_column: Column name for labels
            
        Returns:
            Tuple of (texts, labels)
        """
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Data file not found: {filepath}")
        
        df = pd.read_csv(filepath)
        
        if text_column not in df.columns or label_column not in df.columns:
            raise ValueError(f"Columns {text_column} or {label_column} not found in CSV")
        
        texts = df[text_column].tolist()
        labels = df[label_column].tolist()
        
        print(f"Loaded {len(texts)} samples from {filename}")
        print(f"Label distribution: {np.bincount(labels)}")
        
        return texts, labels
    
    def load_custom_dataset(
        self,
        texts: List[str],
        labels: List[int]
    ) -> Tuple[List[str], List[int]]:
        """
        Load custom dataset from provided lists.
        
        Args:
            texts: List of text samples
            labels: List of corresponding labels
            
        Returns:
            Tuple of (texts, labels)
        """
        if len(texts) != len(labels):
            raise ValueError("Number of texts and labels must match")
        
        print(f"Loaded {len(texts)} custom samples")
        print(f"Label distribution: {np.bincount(labels)}")
        
        return texts, labels
    
    def prepare_for_training(
        self,
        texts: List[str],
        labels: List[int],
        max_length: int = 128,
        test_size: float = 0.2,
        val_size: float = 0.1
    ) -> dict:
        """
        Prepare data for training using the data pipeline.
        
        Args:
            texts: List of text samples
            labels: List of labels
            max_length: Maximum sequence length
            test_size: Test set proportion
            val_size: Validation set proportion
            
        Returns:
            Dictionary containing processed data and metadata
        """
        print("\nPreparing data for training...")
        
        processed_data = self.pipeline.process_text_classification_data(
            texts=texts,
            labels=labels,
            max_length=max_length,
            test_size=test_size,
            val_size=val_size
        )
        
        print(f"Vocabulary size: {processed_data['vocab_size']}")
        print(f"Number of classes: {processed_data['num_classes']}")
        print(f"Max sequence length: {processed_data['max_length']}")
        print(f"Training batches: {len(processed_data['train_loader'])}")
        print(f"Validation batches: {len(processed_data['val_loader'])}")
        print(f"Test batches: {len(processed_data['test_loader'])}")
        
        return processed_data
    
    def create_balanced_dataset(
        self,
        texts: List[str],
        labels: List[int],
        samples_per_class: Optional[int] = None
    ) -> Tuple[List[str], List[int]]:
        """
        Create a balanced dataset by undersampling majority classes.
        
        Args:
            texts: List of text samples
            labels: List of labels
            samples_per_class: Number of samples per class (default: min class size)
            
        Returns:
            Tuple of balanced (texts, labels)
        """
        df = pd.DataFrame({'text': texts, 'label': labels})
        
        if samples_per_class is None:
            samples_per_class = df['label'].value_counts().min()
        
        balanced_dfs = []
        for label in df['label'].unique():
            class_df = df[df['label'] == label]
            if len(class_df) > samples_per_class:
                class_df = class_df.sample(n=samples_per_class, random_state=42)
            balanced_dfs.append(class_df)
        
        balanced_df = pd.concat(balanced_dfs)
        balanced_texts = balanced_df['text'].tolist()
        balanced_labels = balanced_df['label'].tolist()
        
        print(f"Created balanced dataset: {len(balanced_texts)} samples")
        print(f"Samples per class: {samples_per_class}")
        
        return balanced_texts, balanced_labels
    
    def create_augmented_dataset(
        self,
        texts: List[str],
        labels: List[int],
        augment_factor: int = 2
    ) -> Tuple[List[str], List[int]]:
        """
        Create augmented dataset by simple text augmentation.
        
        Args:
            texts: List of text samples
            labels: List of labels
            augment_factor: How many times to augment the dataset
            
        Returns:
            Tuple of augmented (texts, labels)
        """
        augmented_texts = texts.copy()
        augmented_labels = labels.copy()
        
        for _ in range(augment_factor - 1):
            for text, label in zip(texts, labels):
                # Simple augmentation: add random words (very basic)
                words = text.split()
                if len(words) > 3:
                    # Remove one random word
                    import random
                    new_words = words.copy()
                    new_words.pop(random.randint(0, len(new_words) - 1))
                    augmented_texts.append(' '.join(new_words))
                    augmented_labels.append(label)
        
        print(f"Created augmented dataset: {len(augmented_texts)} samples")
        print(f"Original: {len(texts)}, Augmented: {len(augmented_texts)}")
        
        return augmented_texts, augmented_labels
    
    def get_data_statistics(self, texts: List[str], labels: List[int]) -> dict:
        """
        Get statistics about the dataset.
        
        Args:
            texts: List of text samples
            labels: List of labels
            
        Returns:
            Dictionary with dataset statistics
        """
        text_lengths = [len(text.split()) for text in texts]
        
        stats = {
            'total_samples': len(texts),
            'num_classes': len(set(labels)),
            'class_distribution': dict(zip(*np.unique(labels, return_counts=True))),
            'avg_text_length': np.mean(text_lengths),
            'max_text_length': max(text_lengths),
            'min_text_length': min(text_lengths),
            'std_text_length': np.std(text_lengths)
        }
        
        return stats


def load_sample_real_data():
    """
    Convenience function to load the sample real dataset.
    """
    loader = RealDataLoader()
    texts, labels = loader.load_sentiment_csv()
    return texts, labels


def prepare_sample_for_training():
    """
    Convenience function to prepare sample data for training.
    """
    loader = RealDataLoader()
    texts, labels = loader.load_sentiment_csv()
    processed_data = loader.prepare_for_training(texts, labels)
    return processed_data


if __name__ == "__main__":
    print("=" * 60)
    print("Real Data Loading Demonstration")
    print("=" * 60)
    print()
    
    # Initialize loader
    loader = RealDataLoader()
    
    # Load the sample dataset
    print("Loading sample sentiment dataset...")
    texts, labels = loader.load_sentiment_csv()
    
    # Get statistics
    print("\nDataset Statistics:")
    stats = loader.get_data_statistics(texts, labels)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Prepare for training
    print("\n" + "=" * 60)
    print("Preparing data for training...")
    print("=" * 60)
    processed_data = loader.prepare_for_training(texts, labels)
    
    # Create balanced dataset
    print("\n" + "=" * 60)
    print("Creating balanced dataset...")
    print("=" * 60)
    balanced_texts, balanced_labels = loader.create_balanced_dataset(texts, labels)
    
    # Prepare balanced data for training
    balanced_processed = loader.prepare_for_training(balanced_texts, balanced_labels)
    
    print("\n" + "=" * 60)
    print("Real Data Loading Complete")
    print("=" * 60)