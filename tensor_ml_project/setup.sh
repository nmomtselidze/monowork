#!/bin/bash

# Setup script for Tensor ML Project
# This script helps set up the environment and install dependencies

echo "=========================================="
echo "Tensor ML Project - Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Check if pip is available
echo ""
echo "Checking pip availability..."
python3 -m pip --version

# Create virtual environment (optional but recommended)
echo ""
echo "Do you want to create a virtual environment? (recommended) [y/n]"
read -r create_venv

if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Virtual environment created successfully!"
    echo "Activating virtual environment..."
    source .venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Skipping virtual environment creation."
fi

# Install dependencies
echo ""
echo "Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Dependencies installed successfully!"
else
    echo "Error: requirements.txt not found!"
    exit 1
fi

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p data models
echo "Directories created: data/, models/"

# Verify installation
echo ""
echo "Verifying installation..."
python3 -c "import torch; print(f'PyTorch version: {torch.__version__}')"
python3 -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
python3 -c "import sklearn; print(f'Scikit-learn version: {sklearn.__version__}')"

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Run the quick start example: cd examples && python quick_start.py"
echo "2. Or explore the notebook: jupyter notebook notebooks/tensor_ml_demo.ipynb"
echo "3. Read the README.md for detailed documentation"
echo ""