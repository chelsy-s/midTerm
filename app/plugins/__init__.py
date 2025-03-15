"""
Plugins package for the calculator application.
This directory contains plugin modules that extend the calculator functionality.

Plugins should be structured as packages with an __init__.py file that contains
Command subclasses. These commands will be automatically discovered and registered
with the application when it starts.

Example plugin structure:
- plugins/
  - add/
    - __init__.py  # Contains AddCommand class

The Command subclasses must implement the execute method.
"""
