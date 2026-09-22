#!/bin/sh
set -e

python - <<'PY'
import os
import socket
import time

if os.getenv('DB_ENGINE') == 'postgresql':
    host = os.getenv('DB_HOST', 'db')
    port = int(os.getenv('DB_PORT', '5432'))
    for _ in range(60):
        try:
            with socket.create_connection((host, port), timeout=2):
                break
        except OSError:
            time.sleep(1)
    else:
        raise SystemExit('Database is unavailable')
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput

python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', '')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
if username and password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
PY

if [ "${LOAD_DEMO_DATA:-0}" = "1" ]; then
python manage.py shell <<'PY'
from django.core.management import call_command
from shop.models import Product
if not Product.objects.exists():
    call_command('loaddata', 'demo_data')
PY
fi

exec gunicorn voltmarket.wsgi:application --bind 0.0.0.0:8000 --workers 3 --access-logfile - --error-logfile -
