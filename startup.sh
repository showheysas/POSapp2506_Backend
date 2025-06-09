#!/bin/bash
cd /home/site/wwwroot

# Python 実行ファイルのフルパスで pip を使う（App Service対応）
python3.11 -m pip install -r requirements.txt

# FastAPI アプリを起動
python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
