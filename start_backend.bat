@echo off

py -3.11 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
