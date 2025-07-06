#!/bin/bash
set -e

# echo "Waiting for postgres..."
# while ! nc -z db 5432; do
#   sleep 0.1
# done
# echo "PostgreSQL started"

mkdir -p /var/log/supervisor
mkdir -p /var/log/django
mkdir -p /var/log/gunicorn

echo "Collect static files..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Creating default admin user..."
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username='admin').exists() else None"

python manage.py runserver 0.0.0.0:9009
# echo "Starting supervisord..."
# exec /usr/bin/supervisord -n -c /etc/supervisor/conf.d/supervisord.conf
