#!/usr/bin/env bash
set -e

python manage.py compilemessages
python manage.py collectstatic --noinput
python manage.py migrate --database db_owner

exec "$@"
