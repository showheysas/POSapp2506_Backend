#!/bin/bash
cd /home/site/wwwroot
python3.11 -m pip install -r requirements.txt
python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
