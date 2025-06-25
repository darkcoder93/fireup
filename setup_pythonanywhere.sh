#!/bin/bash

# PythonAnywhere Setup Script for FIRE Calculator
# Run this script in your PythonAnywhere Bash console

echo "Setting up FIRE Calculator on PythonAnywhere..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv fire_calculator_env

# Activate virtual environment
echo "Activating virtual environment..."
source fire_calculator_env/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (interactive)
echo "Creating superuser account..."
python manage.py createsuperuser

echo "Setup complete!"
echo "Next steps:"
echo "1. Configure your web app in the Web tab"
echo "2. Update WSGI file"
echo "3. Configure static files"
echo "4. Reload your web app"
echo "5. Visit your domain to test" 