#!/usr/bin/env python3
"""
Advanced Python Calculator Application
Main entry point for the calculator application.

This application demonstrates:
1. Professional software development practices
2. Implementation of design patterns (Command, Factory Method)
3. Plugin architecture for extensibility
4. Comprehensive logging
5. Dynamic configuration via environment variables

The calculator provides a REPL (Read-Eval-Print Loop) interface
for interactive calculation operations and supports direct
mathematical expressions.
"""
import sys
from app import App

def main():
    """
    Main function that initializes and starts the calculator application.
    
    This function:
    1. Creates an instance of the App class
    2. Starts the application's REPL loop
    3. Returns the appropriate exit code
    
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    app = App()
    return app.start()

if __name__ == "__main__":
    sys.exit(main())
