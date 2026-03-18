#!/bin/bash
# Render build script

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser if needed (optional)
# python manage.py shell < create_superuser.py

echo "Build completed successfully!"
