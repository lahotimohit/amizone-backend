#!/bin/bash

echo "Updating pip..."
python3.10 pip install -U pip

# Install dependencies

echo "Installing project dependencies..."
python3.10 -m pip install -r requirements.txt

#Install whitenoise
echo "Installing white noise..."
python3.10 manage.py whitenoise
# Collect staticfiles
echo "Collect static..."
python3.10 manage.py collectstatic --noinput --clear

echo "Build process completed!"```
