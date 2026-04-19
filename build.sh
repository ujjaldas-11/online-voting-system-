#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files (important for production)
python manage.py collectstatic --no-input

# Run migrations (this creates all tables, including voting_vote)
python manage.py migrate --no-input


python manage.py createsuperuser --noinput || true