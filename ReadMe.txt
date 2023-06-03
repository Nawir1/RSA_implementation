#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and run this script again."
    exit 1
fi

# Install pip3
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip3..."
    sudo easy_install pip3
    echo "pip3 installed successfully."
else
    echo "pip3 is already installed."
fi

# Install tk
if ! command -v wish &> /dev/null; then
    echo "Installing tk..."
    brew install tk
    echo "tk installed successfully."
else
    echo "tk is already installed."
fi

# Install customtkinter
echo "Installing customtkinter..."
pip3 install customtkinter
echo "customtkinter installed successfully."

echo "Installation completed."