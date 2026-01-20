#!/bin/bash

# PDF to EPUB Converter - Installation Helper Script
# This script installs all required Python packages using a virtual environment

echo "📦 Installing Python dependencies for PDF to EPUB Converter..."
echo ""

# Check if pip3 is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed. Please install Python 3 first."
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$SCRIPT_DIR/venv"

# Check if virtual environment already exists
if [ -d "$VENV_DIR" ]; then
    echo "📦 Virtual environment already exists. Activating..."
    source "$VENV_DIR/bin/activate"
    echo "✅ Virtual environment activated!"
    echo ""
else
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to create virtual environment."
        echo "   Make sure Python 3 is installed: python3 --version"
        exit 1
    fi
    
    echo "✅ Virtual environment created!"
    echo ""
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    echo "✅ Virtual environment activated!"
    echo ""
fi

# Upgrade pip in virtual environment
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install packages from requirements.txt
echo "📥 Installing packages from requirements.txt..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation complete!"
    echo ""
    echo "📝 Important: To use the script, activate the virtual environment first:"
    echo "   source venv/bin/activate"
    echo ""
    echo "Next steps:"
    echo "1. Make sure Tesseract OCR is installed: brew install tesseract tesseract-lang"
    echo "2. Activate virtual environment: source venv/bin/activate"
    echo "3. Edit convert_pdf_to_epub.py and set your PDF path"
    echo "4. Run: python3 convert_pdf_to_epub.py"
    echo ""
    echo "💡 Tip: You can deactivate the virtual environment later with: deactivate"
else
    echo ""
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi
