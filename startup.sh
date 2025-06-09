#!/bin/bash
cd /home/site/wwwroot

echo "========== Installing dependencies =========="
python3.11 -m pip install -r requirements.txt

echo "========== Starting FastAPI =========="
python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug
