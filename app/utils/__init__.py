"""
Utility commands and helpers for the calculator application.

This module provides utility functionality that supports the calculator application:
1. Cross-platform screen clearing for a better user experience
2. System information retrieval for diagnostics
3. Utility command registration with the central command handler

These utilities demonstrate separation of concerns by isolating
support functionality from the core calculator operations.
"""
import logging
import os
import platform
import sys
from datetime import datetime
from typing import Dict, Any, Optional, List

from app.commands import Command, CommandHandler

class ClearScreenCommand(Command):
    """
    Command to clear the console/terminal screen.

    This command detects the operating system and uses the appropriate
    system command to clear the terminal output, providing a clean
    interface for the user regardless of their platform.

    The implementation demonstrates:
    1. Platform detection for cross-platform compatibility
    2. Appropriate error handling around system command execution
    3. Consistent logging for diagnostic purposes
    """

    def __init__(self):
        """
        Initialize the clear screen command.

        Sets up logging for the command to track usage and any potential issues.
        """
        self.logger = logging.getLogger(__name__)
        # Pre-determine the clear command based on the operating system
        self.clear_command = 'cls' if platform.system() == "Windows" else 'clear'

    def execute(self, *args, **kwargs) -> str:
        """
        Execute the command to clear the terminal screen.

        This method:
        1. Detects the user's operating system
        2. Executes the appropriate clear command
        3. Handles potential errors if the command fails
        4. Returns a success message to the user

        Args:
            *args: Not used by this command
            **kwargs: Not used by this command

        Returns:
            str: Success message or error information
        """
        self.logger.info("Executing clear screen command")

        try:
            # Execute the appropriate clear command for the OS
            os.system(self.clear_command)
            return "Screen cleared successfully."
        except Exception as e:
            error_msg = f"Failed to clear screen: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return error_msg

class SystemInfoCommand(Command):
    """
    Command to display system and calculator information.

    This command provides diagnostic information about the system
    running the calculator, including Python version, operating system,
    and runtime information.
    """

    def __init__(self):
        """Initialize the system info command."""
        self.logger = logging.getLogger(__name__)

    def execute(self, *args, **kwargs) -> str:
        """
        Execute the command to display system information.

        Args:
            *args: Not used by this command
            **kwargs: Not used by this command

        Returns:
            str: Formatted system information
        """
        self.logger.info("Executing system info command")

        # Collect system information
        info = {
            "Python Version": platform.python_version(),
            "Platform": platform.platform(),
            "Current Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Calculator Process ID": os.getpid(),
            "System Architecture": platform.architecture()[0]
        }

        # Format the information for display
        info_text = ["\n=== System Information ==="]
        for key, value in info.items():
            info_text.append(f"{key}: {value}")

        return "\n".join(info_text)

def register_utility_commands(command_handler: CommandHandler) -> None:
    """
    Register utility commands with the command handler.

    This function creates and registers utility command instances,
    making them available for use in the calculator.

    The function centralizes command registration to ensure:
    1. Consistent registration of all utility commands
    2. Well-defined command names and aliases
    3. Proper logging of registration events

    Args:
        command_handler: CommandHandler to register commands with
    """
    # Create command instances
    clear_screen_cmd = ClearScreenCommand()
    system_info_cmd = SystemInfoCommand()

    # Register commands with appropriate names and aliases
    registrations = [
        ("clear", clear_screen_cmd),
        ("cls", clear_screen_cmd),  # Common Windows alias
        ("system-info", system_info_cmd),
        ("sysinfo", system_info_cmd)  # Shorter alias
    ]

    # Register all commands
    for name, cmd in registrations:
        command_handler.register_command(name, cmd)
        
    logging.info("Registered %s utility commands", len(registrations))

def get_system_info() -> Dict[str, str]:
    """
    Get system information as a dictionary.

    This utility function provides access to system information
    for diagnostic purposes throughout the application.

    Returns:
        dict: Dictionary containing system information
    """
    return {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "system": platform.system(),
        "architecture": platform.architecture()[0],
        "processor": platform.processor(),
        "python_path": sys.executable
    }
