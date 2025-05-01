#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip and install required packages
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete. To run the app, execute ./run_app.sh"
