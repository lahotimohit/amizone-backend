#!/bin/bash

echo "Updating pip..."
python3.12 pip install -U pip

# Install dependencies

echo "Installing project dependencies..."
python -m pip install -r requirements.txt

# Make migrations
echo "Making migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
#Install whitenoise
echo "Installing white noise..."
python manage.py whitenoise
# Collect staticfiles
echo "Collect static..."
python3.12 manage.py collectstatic --noinput --clear

echo "Build process completed!"```
