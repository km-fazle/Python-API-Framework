#!/usr/bin/env python3
"""
Command-line interface for KM PyAPI Framework.
"""

import sys
import uvicorn
from .main import app

def main():
    """Run the FastAPI application."""
    uvicorn.run(
        "py_api_framework.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main() 