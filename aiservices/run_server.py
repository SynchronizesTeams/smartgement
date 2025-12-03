#!/usr/bin/env python
"""Minimal server test"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
