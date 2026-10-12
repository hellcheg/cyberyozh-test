#!/bin/sh

set -e

cd /app

python manage.py migrate --noinput

echo "Создание админа..."
python manage.py init_admin

exec "$@"
