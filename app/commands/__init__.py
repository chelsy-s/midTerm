"""
Command handling module for the calculator application.

This module implements the Command pattern, providing a framework for:
1. Defining commands as classes with a consistent interface
2. Registering commands with a central handler
3. Executing commands by name with consistent error handling

The module demonstrates both LBYL (Look Before You Leap) and
EAFP (Easier to Ask for Forgiveness than Permission) error handling
approaches.
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class Command(ABC):
    """
    Abstract base class for all calculator commands.
    
    This class implements the Command design pattern, providing a uniform
    interface for executing different actions in the calculator.
    
    All commands must implement the execute method, which performs
    the command's specific functionality.
    """
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute the command with the given arguments.
        
        Args:
            *args: Positional arguments for the command
            **kwargs: Keyword arguments for the command
            
        Returns:
            The result of executing the command
        """
        pass

class CommandHandler:
    """
    Manages command registration and execution.
    
    This class acts as an invoker in the Command pattern. It maintains
    a registry of command objects and provides methods to:
    1. Register commands
    2. Execute commands by name
    3. Handle command execution errors
    
    The handler implements both LBYL and EAFP approaches for error handling.
    """
    
    def __init__(self):
        """Initialize the command handler with an empty command registry."""
        self.commands: Dict[str, Command] = {}
        self.logger = logging.getLogger(__name__)
        self.logger.info("CommandHandler initialized")
        
    def register_command(self, name: str, command: Command) -> bool:
        """
        Register a command with the handler.
        
        Args:
            name: Name to register the command under
            command: Command object to register
            
        Returns:
            bool: True if registration was successful, False otherwise
        """
        if not isinstance(command, Command):
            self.logger.error(f"Cannot register {name}: Object must be a Command instance")
            return False
            
        # Check if command is already registered
        if name in self.commands:
            self.logger.warning(f"Command '{name}' already registered, overwriting")
            
        self.commands[name] = command
        self.logger.info(f"Command '{name}' registered")
        return True
        
    def get_available_commands(self) -> List[str]:
        """
        Get a list of all registered command names.
        
        Returns:
            List of available command names
        """
        return list(self.commands.keys())
        
    def execute_command_lbyl(self, command_name: str, *args, **kwargs) -> Optional[Any]:
        """
        Execute a command using the LBYL (Look Before You Leap) approach.
        
        This method checks for command existence before attempting execution,
        demonstrating the LBYL error handling approach.
        
        Args:
            command_name: Name of the command to execute
            *args: Arguments to pass to the command
            **kwargs: Keyword arguments to pass to the command
            
        Returns:
            The result of the command execution or an error message
        """
        self.logger.info(f"LBYL: Executing command '{command_name}'")
        
        # Check if the command exists (Looking before leaping)
        if command_name not in self.commands:
            error_msg = f"Unknown command: '{command_name}'"
            self.logger.warning(error_msg)
            return error_msg
            
        try:
            command = self.commands[command_name]
            result = command.execute(*args, **kwargs)
            return result
        except Exception as e:
            error_msg = f"Error executing command '{command_name}': {str(e)}"
            self.logger.error(error_msg)
            return error_msg
            
    def execute_command_eafp(self, command_name: str, *args, **kwargs) -> Optional[Any]:
        """
        Execute a command using the EAFP (Easier to Ask for Forgiveness than Permission) approach.
        
        This method attempts to execute the command directly and handles exceptions
        if they occur, demonstrating the EAFP error handling approach.
        
        Args:
            command_name: Name of the command to execute
            *args: Arguments to pass to the command
            **kwargs: Keyword arguments to pass to the command
            
        Returns:
            The result of the command execution or an error message
        """
        self.logger.info(f"EAFP: Executing command '{command_name}'")
        
        try:
            # Try to execute the command (Easier to Ask for Forgiveness)
            command = self.commands[command_name]
            result = command.execute(*args, **kwargs)
            return result
        except KeyError:
            # Command not found
            error_msg = f"Unknown command: '{command_name}'. Type 'help' for available commands."
            self.logger.warning(error_msg)
            return error_msg
        except Exception as e:
            # Other execution errors
            error_msg = f"Error executing command '{command_name}': {str(e)}"
            self.logger.error(error_msg)
            return error_msg
