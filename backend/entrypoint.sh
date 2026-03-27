#!/bin/sh
set -e

echo "Starting backend container..."

required_vars="POSTGRES_HOST POSTGRES_PORT POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD JWT_SECRET_KEY"

for var_name in $required_vars; do
  eval "var_value=\${$var_name}"
  if [ -z "$var_value" ]; then
    echo "Missing required environment variable: $var_name"
    exit 1
  fi
done

echo "Waiting for PostgreSQL at ${POSTGRES_HOST}:${POSTGRES_PORT}..."
python - <<'PY'
import os
import socket
import sys
import time

host = os.environ["POSTGRES_HOST"]
port = int(os.environ["POSTGRES_PORT"])
timeout_seconds = 30
deadline = time.time() + timeout_seconds

while time.time() < deadline:
    try:
        with socket.create_connection((host, port), timeout=2):
            print("PostgreSQL is reachable.")
            sys.exit(0)
    except OSError:
        time.sleep(1)

print(f"Could not connect to PostgreSQL at {host}:{port} within {timeout_seconds} seconds.")
sys.exit(1)
PY

echo "Launching FastAPI with uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
