#!/usr/bin/env python3
"""
Advanced Python Calculator Application - Main Entry Point

This module serves as the entry point for the calculator application,
demonstrating professional software engineering practices including:

1. Modular architecture with clear separation of concerns
2. Implementation of multiple design patterns:
   - Command Pattern: Encapsulating operations as objects
   - Factory Method: Creating operations without specifying concrete classes
   - Strategy Pattern: Interchangeable algorithm implementations
   - Facade Pattern: Simplified interface to complex subsystems

3. Plugin-based extensibility allowing dynamic functionality loading
4. Comprehensive logging with configurable levels
5. Environment-based configuration for deployment flexibility
6. Robust error handling with both LBYL and EAFP approaches

The calculator provides an intuitive REPL (Read-Eval-Print Loop) interface
for interactive calculation operations with history tracking and supports
direct mathematical expressions for rapid calculations.
"""
import sys
import logging
import traceback
from typing import Optional, Dict, Any

from app import App

def main() -> int:
    """
    Main function that initializes and starts the calculator application.

    This function acts as the entry point for the application, performing:
    1. Application instance creation
    2. Application startup with exception handling
    3. Clean shutdown with appropriate exit codes

    The implementation demonstrates professional error handling to ensure
    the application behaves gracefully even when unexpected errors occur.

    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    try:
        # Create and start the application
        app = App()
        return app.start()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nApplication terminated by user")
        return 0
    except Exception as e:
        # Handle unexpected errors with detailed logging
        logging.critical(f"Fatal error in main: {str(e)}", exc_info=True)
        print(f"\nFatal error: {str(e)}")
        print("See logs for details.")
        return 1

if __name__ == "__main__":
    # Run the application and pass its exit code to the system
    exit_code = main()
    sys.exit(exit_code)
