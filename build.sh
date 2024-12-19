#!/bin/bash

echo "Updating pip..."
python3.12 pip install -U pip

#Install whitenoise
echo "Installing white noise..."
python3.12 manage.py whitenoise
# Collect staticfiles
echo "Collect static..."
python3.12 manage.py collectstatic --noinput --clear

echo "Build process completed!"```
