"""
Utility commands for the calculator application.

This module contains utility commands for managing
the calculator application interface, such as clearing
the screen and other utility functions.
"""
import logging
import os
import platform
from app.commands import Command

class ClearScreenCommand(Command):
    """
    Command to clear the console/terminal screen.
    
    This command clears the screen output in the terminal,
    providing a clean interface for the user.
    """
    
    def __init__(self):
        """Initialize the clear screen command."""
        self.logger = logging.getLogger(__name__)
        
    def execute(self, *args, **kwargs):
        """
        Execute the command to clear the screen.
        
        Args:
            *args: Not used by this command
            **kwargs: Not used by this command
            
        Returns:
            str: Success message
        """
        self.logger.info("Executing clear screen command")
        
        # Determine the clear command based on operating system
        if platform.system() == "Windows":
            os.system('cls')
        else:  # Unix/Linux/MacOS
            os.system('clear')
            
        return "Screen cleared."

def register_utility_commands(command_handler):
    """
    Register utility commands with the command handler.
    
    This function creates instances of utility command classes
    and registers them with the provided command handler.
    
    Args:
        command_handler: CommandHandler to register commands with
    """
    # Create command instances
    clear_screen_cmd = ClearScreenCommand()
    
    # Register commands
    command_handler.register_command("clear", clear_screen_cmd)
    command_handler.register_command("cls", clear_screen_cmd)  # Common Windows alias
    
    logging.info("Utility commands registered") 