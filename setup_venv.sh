#!/bin/bash

# Set the name of the virtual environment directory
VENV_DIR="book_discovery_venv"
REQUIREMENTS_FILE="requirements.txt"

# Try to find Python command (could be python or python3)
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python not found. Please install Python 3.6+ and try again."
    exit 1
fi

echo "Using Python command: $PYTHON_CMD"

# Check if the virtual environment already exists
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  $PYTHON_CMD -m venv "$VENV_DIR"
  
  if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Failed to create virtual environment. Please check your Python installation."
    exit 1
  fi

  source "$VENV_DIR/bin/activate" || { echo "Error: Failed to activate virtual environment."; exit 1; }

  # Install dependencies from requirements.txt if it exists
  if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install --no-cache-dir -r "$REQUIREMENTS_FILE"
  else
    echo "Error: $REQUIREMENTS_FILE not found."
    exit 1
  fi
else
  source "$VENV_DIR/bin/activate" || { echo "Error: Failed to activate virtual environment."; exit 1; }
  echo "Virtual environment already exists. Activated."
fi

echo "Virtual environment setup complete. You can now run the application with '$PYTHON_CMD app.py'."