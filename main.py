#!/usr/bin/env python3
"""
Advanced Python Calculator
Main entry point for the calculator application.
"""
import sys
from app import App

def main():
    """
    Main function to start the calculator application.
    
    Returns:
        int: Exit code
    """
    app = App()
    return app.start()

if __name__ == "__main__":
    sys.exit(main())
