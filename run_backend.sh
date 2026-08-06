#!/bin/bash
PYTHON_EXEC="/Library/Frameworks/Python.framework/Versions/3.14/bin/python3"
exec $PYTHON_EXEC -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
