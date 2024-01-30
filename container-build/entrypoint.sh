#!/usr/bin/env bash
set -e
echo "Status SKIP_APP_INIT: $SKIP_APP_INIT"

if [ -z "$SKIP_APP_INIT" ]; then
    echo "Running application initialization scripts.."
    python manage.py compilemessages
    python manage.py collectstatic --noinput
    python manage.py migrate --database db_owner
fi
    
exec "$@"



