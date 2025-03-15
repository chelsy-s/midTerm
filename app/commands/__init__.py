from abc import ABC, abstractmethod
import logging

class Command(ABC):
    """
    Command Pattern: Abstract base class for all commands.
    This implements the Command Pattern, which encapsulates a request as an object,
    allowing for parameterization of clients with different requests.
    """
    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute the command with the provided arguments.
        
        Args:
            *args: Variable length argument list
            **kwargs: Variable length keyword arguments
        
        Returns:
            The result of the command execution
        """
        pass

class CommandHandler:
    """
    CommandHandler manages and executes commands.
    This is part of the Command Pattern implementation.
    """
    def __init__(self):
        self.commands = {}
        self.logger = logging.getLogger(__name__)

    def register_command(self, command_name: str, command: Command):
        """
        Register a command with the handler.
        
        Args:
            command_name: Name to register the command under
            command: Command object to register
        """
        self.logger.info(f"Registering command: {command_name}")
        self.commands[command_name] = command

    def execute_command(self, command_name: str, *args, **kwargs):
        """
        Execute a command by name using the "Look Before You Leap" (LBYL) approach.
        This approach checks for conditions before attempting to execute.
        
        Args:
            command_name: Name of the command to execute
            *args: Arguments to pass to the command
            **kwargs: Keyword arguments to pass to the command
            
        Returns:
            Result of the command execution or None if command not found
        """
        self.logger.debug(f"Attempting to execute command: {command_name}")
        
        # LBYL approach - Look Before You Leap
        if command_name in self.commands:
            self.logger.info(f"Executing command: {command_name}")
            return self.commands[command_name].execute(*args, **kwargs)
        else:
            self.logger.warning(f"No such command: {command_name}")
            return f"No such command: {command_name}"

    def execute_command_eafp(self, command_name: str, *args, **kwargs):
        """
        Execute a command by name using the "Easier to Ask for Forgiveness than Permission" (EAFP) approach.
        This approach attempts to execute and catches exceptions if they occur.
        
        Args:
            command_name: Name of the command to execute
            *args: Arguments to pass to the command
            **kwargs: Keyword arguments to pass to the command
            
        Returns:
            Result of the command execution or error message if command fails
        """
        self.logger.debug(f"Attempting to execute command (EAFP): {command_name}")
        
        # EAFP approach - Easier to Ask for Forgiveness than Permission
        try:
            self.logger.info(f"Executing command: {command_name}")
            return self.commands[command_name].execute(*args, **kwargs)
        except KeyError:
            self.logger.warning(f"No such command: {command_name}")
            return f"No such command: {command_name}"
        except Exception as e:
            self.logger.error(f"Error executing command {command_name}: {str(e)}")
            return f"Error executing command {command_name}: {str(e)}"
