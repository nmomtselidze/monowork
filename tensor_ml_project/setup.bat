@echo off
REM Setup script for Tensor ML Project (Windows)
REM This script helps set up the environment and install dependencies

echo ==========================================
echo Tensor ML Project - Setup Script
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version

REM Check if pip is available
echo.
echo Checking pip availability...
python -m pip --version

REM Create virtual environment (optional but recommended)
echo.
echo Do you want to create a virtual environment? (recommended) [y/n]
set /p create_venv=

if /i "%create_venv%"=="y" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created successfully!
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo Skipping virtual environment creation.
)

REM Install dependencies
echo.
echo Installing dependencies from requirements.txt...
if exist requirements.txt (
    pip install -r requirements.txt
    echo Dependencies installed successfully!
) else (
    echo Error: requirements.txt not found!
    exit /b 1
)

REM Create necessary directories
echo.
echo Creating necessary directories...
if not exist data mkdir data
if not exist models mkdir models
echo Directories created: data/, models/

REM Verify installation
echo.
echo Verifying installation...
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
python -c "import sklearn; print(f'Scikit-learn version: {sklearn.__version__}')"

echo.
echo ==========================================
echo Setup completed successfully!
echo ==========================================
echo.
echo Next steps:
echo 1. Run the quick start example: cd examples && python quick_start.py
echo 2. Or explore the notebook: jupyter notebook notebooks/tensor_ml_demo.ipynb
echo 3. Read the README.md for detailed documentation
echo.

pause