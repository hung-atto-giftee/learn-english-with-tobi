#!/bin/sh
set -e

echo "Starting frontend container..."
echo "Serving built React app on port 3000..."

exec serve -s dist -l 3000
