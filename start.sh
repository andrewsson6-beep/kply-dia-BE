#!/bin/bash
set -e

# Render nginx config from template using Cloud Run's PORT env var
envsubst '${PORT}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Start the app server
uvicorn main:app --app-dir /app/src --host 127.0.0.1 --port 8000 &
UVICORN_PID=$!

# Start nginx
nginx -g 'daemon off;' &
NGINX_PID=$!

# If either process dies, exit so Cloud Run marks the container unhealthy
# and surfaces the failure instead of silently serving 502s forever
wait -n "$UVICORN_PID" "$NGINX_PID"
exit $?