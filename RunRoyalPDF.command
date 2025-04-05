#!/bin/bash

# -------- ROYAL PDF LAUNCHER --------
cd "$(dirname "$0")"

# Check for Python 3
if ! command -v python3 &> /dev/null
then
    echo "🐍 Python 3 not found! Installing via Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python
else
    echo "✅ Python 3 is already installed."
fi

# Check for pip
if ! command -v pip3 &> /dev/null
then
    echo "📦 Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
else
    echo "✅ pip is already installed."
fi

# Create virtual environment if it doesn’t exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install required package
pip install --upgrade pip
pip install PyMuPDF

# Run the magic script
python3 royal_pdf_replacer.py

echo "\n👑 All done! Close this window when you're ready. 💖"
