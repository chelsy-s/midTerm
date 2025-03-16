"""
Command mapper for calculator operations.

This module creates command handlers that map to operation plugins, allowing users
to directly invoke mathematical operations like 'add 1 2 3' as commands.

The mapper automatically registers all operations from the OperationFactory
as individual commands that can be executed within the REPL interface.
"""
import logging
from app.commands import Command
from app.plugins.operations import OperationFactory

class OperationCommand(Command):
    """
    Command that maps to a calculator operation.

    This class bridges the Command pattern and the Factory Method pattern.
    It allows users to directly call operations like 'add 1 2 3' in the REPL
    instead of needing to go through a more complex interface.

    Each OperationCommand instance is linked to a specific operation type
    (add, subtract, etc.) and delegates execution to the corresponding
    Operation instance created by the OperationFactory.
    """
    def __init__(self, operation_name):
        """
        Initialize the operation command.

        Args:
            operation_name: Name of the operation to map to (e.g., 'add', 'subtract')
        """
        self.operation_name = operation_name
        self.logger = logging.getLogger(__name__)

    def execute(self, *args, **kwargs):
        """
        Execute the mapped operation.

        This method retrieves the appropriate Operation instance from the
        OperationFactory and delegates execution to it, passing along any
        provided arguments.

        Args:
            *args: Arguments to pass to the operation (typically numeric values)
            **kwargs: Keyword arguments to pass to the operation

        Returns:
            Result of the operation or error message if execution fails
        """
        self.logger.info("Executing operation command: %s with args: %s", self.operation_name, args)

        # Get the operation from the factory
        operation = OperationFactory.create_operation(self.operation_name)

        if operation is None:
            error_msg = f"Error: No such operation: {self.operation_name}"
            self.logger.warning(error_msg)
            return error_msg

        # Execute the operation with the provided arguments
        try:
            result = operation.execute(*args, **kwargs)
            self.logger.info("Operation %s result: %s", self.operation_name, result)
            return result
        except Exception as e:
            # Properly handle any exceptions during execution
            error_msg = f"Error during operation {self.operation_name}: {str(e)}"
            self.logger.error(error_msg)
            return error_msg

def register_operation_commands(command_handler):
    """
    Register commands for all available operations.

    This function automatically discovers all operations registered with
    the OperationFactory and creates corresponding command handlers for each.
    This enables direct execution of operations from the REPL.

    Args:
        command_handler: CommandHandler to register commands with
    """
    # Get all available operations
    operations = OperationFactory.get_available_operations()

    if not operations:
        logging.warning("No operations available to register as commands")
        return

    # Register a command for each operation
    for op_name in operations:
        command = OperationCommand(op_name)
        command_handler.register_command(op_name, command)
        logging.info("Registered command for operation: %s", op_name)

    logging.info("Successfully registered %s operation commands", len(operations))
