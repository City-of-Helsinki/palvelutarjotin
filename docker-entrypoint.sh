#!/bin/bash
set -e

if [ -z "$SKIP_DATABASE_CHECK" -o "$SKIP_DATABASE_CHECK" = "0" ]; then
  until nc -z -v -w30 "$DATABASE_HOST" 5432
  do
    echo "Waiting for postgres database connection..."
    sleep 1
  done
  echo "Database is up!"
fi


# Apply database migrations
if [[ "$APPLY_MIGRATIONS" = "1" ]]; then
    echo "Applying database migrations..."
    ./manage.py migrate --noinput
fi

# Start server
if [[ ! -z "$@" ]]; then
    "$@"
elif [[ "$DEV_SERVER" = "1" ]]; then
    python ./manage.py runserver 0.0.0.0:8081
else
    export UWSGI_PROCESSES=${UWSGI_PROCESSES:-4}
    uwsgi --ini .prod/uwsgi.ini
fi
