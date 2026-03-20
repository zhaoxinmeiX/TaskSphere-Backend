#!/bin/bash
# Install dependencies
python3 -m pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput

# Run migrations (Optional but highly recommended on Vercel)
python3 manage.py migrate
