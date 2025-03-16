"""
Command handling module for the calculator application.

This module implements the Command pattern, a behavioral design pattern
where requests are encapsulated as objects. This allows for:

1. Parameterization of clients with different requests
2. Queuing or logging of requests
3. Support for undoable operations
4. Separation of concerns between invoker and receiver

The implementation provides both LBYL (Look Before You Leap) and
EAFP (Easier to Ask for Forgiveness than Permission) error handling
approaches, demonstrating both Python idioms.
"""
import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Tuple, Union, Callable

class Command(ABC):
    """
    Abstract base class for all calculator commands.

    This class serves as the foundation of the Command design pattern,
    providing a uniform interface for executing different actions in
    the calculator. By encapsulating commands as objects, we achieve:

    1. Decoupling between the invoker (CommandHandler) and receivers
    2. Extensibility through new command implementations
    3. Composability of complex commands from simple ones
    4. Consistent error handling across all commands

    All concrete command classes must implement the execute method.
    """

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the command with the given arguments.

        This abstract method must be implemented by all concrete command
        classes to perform their specific functionality.

        Args:
            *args: Positional arguments for the command
            **kwargs: Keyword arguments for the command

        Returns:
            The result of executing the command, typically a string
            or a numeric value depending on the command type
        """
        pass

class CommandHandler:
    """
    Manages command registration and execution.

    This class serves as the invoker in the Command pattern, maintaining
    a registry of command objects and coordinating their execution. It:

    1. Provides a centralized registry for all available commands
    2. Implements uniform command execution with comprehensive error handling
    3. Demonstrates both LBYL and EAFP Python error handling approaches
    4. Supports runtime discovery of commands through registration

    The handler acts as a facade to the underlying command objects,
    simplifying the client interface to the command subsystem.
    """

    def __init__(self):
        """
        Initialize the command handler with an empty command registry.

        Sets up the command registry dictionary and configures logging
        for command execution tracking.
        """
        self.commands: Dict[str, Command] = {}
        self.logger = logging.getLogger(__name__)
        self.execution_stats: Dict[str, Dict[str, Union[int, float]]] = {}
        self.logger.info("CommandHandler initialized")

    def register_command(self, name: str, command: Command) -> bool:
        """
        Register a command with the handler.

        This method adds a command to the registry under the specified name,
        performing validation to ensure command integrity. It follows the
        LBYL approach by checking preconditions before taking action.

        Args:
            name: Name to register the command under (used as the key)
            command: Command object to register (must implement Command ABC)

        Returns:
            bool: True if registration was successful, False otherwise
        """
        # Validate command is a proper Command instance (LBYL approach)
        if not isinstance(command, Command):
            self.logger.error("Cannot register %s: Object must be a Command instance", name)
            return False

        # Check if command is already registered and log appropriately
        if name in self.commands:
            self.logger.warning(f"Command '{name}' already registered, overwriting previous implementation")

        # Store the command and initialize its execution statistics
        self.commands[name] = command
        self.execution_stats[name] = {"count": 0, "total_time": 0.0, "last_executed": 0.0}

        self.logger.info(f"Command '{name}' registered successfully")
        return True

    def get_available_commands(self) -> List[str]:
        """
        Get a list of all registered command names.

        This convenience method provides clients with a way to discover
        available commands at runtime.

        Returns:
            List[str]: Sorted list of available command names for predictable output
        """
        return sorted(self.commands.keys())

    def execute_command_lbyl(self, command_name: str, *args, **kwargs) -> Optional[Any]:
        """
        Execute a command using the LBYL (Look Before You Leap) approach.

        This method demonstrates the LBYL error handling style by checking
        conditions before proceeding with execution. It:

        1. Verifies the command exists before attempting to execute it
        2. Handles execution errors with structured error messages
        3. Logs command execution for debugging and monitoring
        4. Tracks execution statistics for performance analysis

        Args:
            command_name: Name of the command to execute
            *args: Positional arguments to pass to the command
            **kwargs: Keyword arguments to pass to the command

        Returns:
            The result of the command execution or an error message
        """
        self.logger.info(f"LBYL: Executing command '{command_name}'")

        # Check if the command exists before attempting execution (LBYL principle)
        if command_name not in self.commands:
            error_msg = f"Unknown command: '{command_name}'"
            self.logger.warning(error_msg)
            return error_msg

        try:
            # Measure execution time for performance tracking
            start_time = time.time()

            command = self.commands[command_name]
            result = command.execute(*args, **kwargs)

            # Update execution statistics
            execution_time = time.time() - start_time
            self._update_execution_stats(command_name, execution_time)

            return result
        except (ValueError, TypeError, AttributeError) as e:
            error_msg = f"Error executing command '{command_name}': {str(e)}"
            self.logger.error(error_msg)
            return error_msg
        except Exception as e:
            # Catch-all for unexpected errors to prevent application crashes
            error_msg = f"Unexpected error in command '{command_name}': {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return error_msg

    def execute_command_eafp(self, command_name: str, *args, **kwargs) -> Optional[Any]:
        """
        Execute a command using the EAFP (Easier to Ask for Forgiveness than Permission) approach.

        This method demonstrates the EAFP error handling style by attempting
        the operation and catching exceptions if they occur. It:

        1. Attempts to execute the command directly without preliminary checks
        2. Handles expected exceptions with appropriate error messages
        3. Categorizes errors for better diagnostics and troubleshooting
        4. Tracks execution statistics for performance analysis

        Args:
            command_name: Name of the command to execute
            *args: Positional arguments to pass to the command
            **kwargs: Keyword arguments to pass to the command

        Returns:
            The result of the command execution or an error message
        """
        self.logger.info(f"EAFP: Executing command '{command_name}'")

        try:
            # Measure execution time for performance tracking
            start_time = time.time()

            # Try to execute the command directly (EAFP principle)
            command = self.commands[command_name]
            result = command.execute(*args, **kwargs)

            # Update execution statistics
            execution_time = time.time() - start_time
            self._update_execution_stats(command_name, execution_time)

            return result
        except KeyError:
            # Command not found in registry
            error_msg = f"Unknown command: '{command_name}'. Type 'help' for available commands."
            self.logger.warning(error_msg)
            return error_msg
        except (ValueError, TypeError) as e:
            # For test compatibility, use a more general error message format
            error_msg = f"Error executing command '{command_name}': {str(e)}"
            self.logger.error(error_msg)
            return error_msg
        except AttributeError as e:
            # Command implementation errors (for backward compatibility with tests)
            error_msg = f"Error executing command '{command_name}': {str(e)}"
            self.logger.error(error_msg)
            return error_msg
        except Exception as e:
            # Catch-all for unexpected errors to prevent application crashes
            error_msg = f"Error executing command '{command_name}': {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return error_msg

    def _update_execution_stats(self, command_name: str, execution_time: float) -> None:
        """
        Update execution statistics for a command.

        This private helper method tracks command usage metrics for
        performance monitoring and optimization opportunities.

        Args:
            command_name: Name of the executed command
            execution_time: Time taken to execute the command in seconds
        """
        stats = self.execution_stats.setdefault(command_name, {
            "count": 0,
            "total_time": 0.0,
            "last_executed": 0.0
        })

        stats["count"] += 1
        stats["total_time"] += execution_time
        stats["last_executed"] = time.time()

    def get_command_stats(self, command_name: Optional[str] = None) -> Dict:
        """
        Get execution statistics for commands.

        Args:
            command_name: Optional name of specific command to get stats for
                         If None, returns stats for all commands

        Returns:
            Dictionary of command execution statistics
        """
        if command_name:
            return self.execution_stats.get(command_name, {})
        return self.execution_stats
