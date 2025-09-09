#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies required for tiktoken and other packages
apt-get update
apt-get install -y build-essential python3-dev

# Upgrade pip
python -m pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt
