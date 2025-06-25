#!/bin/bash
# Build script for Railway deployment

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT fire_calculator.wsgi:application 