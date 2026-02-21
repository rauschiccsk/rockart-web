#!/bin/sh
# Startup script — spusti Python contact API na pozadi a potom Nginx na popredi
echo "[start.sh] Starting contact_api.py on port 8080..."
python3 /app/contact_api.py &

echo "[start.sh] Starting Nginx..."
nginx -g "daemon off;"
