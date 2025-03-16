"""
Menu plugin for the calculator application.

This plugin provides a menu command that lists all available
calculator operations to the user, enhancing discoverability
and usability of the calculator functionality.
"""
import logging
from app.commands import Command
from app.plugins.operations import OperationFactory

class MenuCommand(Command):
    """
    Command that displays available operations in the calculator.

    This command implements the Command pattern and provides users
    with information about what operations are available in the
    calculator and how to use them.
    """
    def __init__(self):
        """Initialize the menu command."""
        self.logger = logging.getLogger(__name__)

    def execute(self, *args, **kwargs):
        """
        Execute the menu command, displaying available operations.

        This method queries the OperationFactory for all registered
        operations and formats them into a user-friendly menu display.

        Args:
            *args: Not used by this command
            **kwargs: Not used by this command

        Returns:
            str: Formatted string containing the menu of available operations
        """
        self.logger.info("Executing menu command")

        operations = OperationFactory.get_available_operations()

        if not operations:
            self.logger.warning("No operations available to display in menu")
            return "No calculator operations are currently available."

        # Format the menu in a user-friendly way
        menu_text = [
            "\n=== Available Calculator Operations ===",
            ""
        ]

        for op in sorted(operations):
            operation = OperationFactory.create_operation(op)
            if operation:
                description = operation.__doc__ or "No description available"
                # Clean up the docstring
                description = description.strip().split('\n')[0]
                menu_text.append(f"{op}: {description}")

        menu_text.extend([
            "",
            "To use an operation, type its name followed by the numbers to operate on.",
            "Example: 'add 5 10 15' to add the numbers 5, 10, and 15.",
            "",
            "Type 'help' for more information on using the calculator."
        ])

        self.logger.info("Menu command displayed %s operations", len(operations))
        return "\n".join(menu_text)
