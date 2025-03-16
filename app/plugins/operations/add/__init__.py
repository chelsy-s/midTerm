"""
Addition operation plugin for the calculator application.

This module implements the addition operation for the calculator, showcasing:
1. Concrete implementation of the Operation abstract base class
2. Clean separation between argument validation and execution
3. Comprehensive error handling and logging
4. Automatic registration with the operation factory

The addition operation represents one of the foundational mathematical
operations that demonstrates the plugin architecture of the calculator.
"""
import logging
from typing import Tuple, Optional, List, Union
from app.plugins.operations import Operation, OperationFactory

class AddOperation(Operation):
    """
    Addition operation that computes the sum of multiple numeric values.

    This operation follows the mathematical principle of addition by:
    1. Converting all input arguments to floating-point numbers
    2. Computing their sum using Python's built-in sum function
    3. Handling edge cases and errors with appropriate messages

    The implementation validates inputs thoroughly before performing
    the calculation, demonstrating the LBYL (Look Before You Leap)
    approach to error handling.
    """

    def __init__(self):
        """
        Initialize the addition operation.

        Sets up the logger for operation-specific logging, allowing
        for detailed troubleshooting if issues occur.
        """
        self.logger = logging.getLogger(__name__)

    def validate_args(self, *args, **kwargs) -> Tuple[bool, Optional[str]]:
        """
        Validate that the provided arguments are valid for addition.

        This method performs thorough input validation by checking that:
        1. At least two arguments are provided (addition requires 2+ operands)
        2. All arguments can be converted to floating-point numbers

        Args:
            *args: The arguments to validate as strings or numeric values
            **kwargs: Not used for the addition operation

        Returns:
            tuple: (is_valid, error_message)
                - is_valid (bool): True if arguments are valid, False otherwise
                - error_message (str): Detailed error message if invalid, None otherwise
        """
        # Check argument count - addition needs at least two numbers
        if len(args) < 2:
            error_msg = "Addition requires at least two numbers"
            self.logger.warning("Validation failed: %s", error_msg)
            return False, error_msg

        # Validate each argument can be converted to a float
        for i, arg in enumerate(args):
            try:
                float(arg)
            except (ValueError, TypeError):
                error_msg = f"Invalid argument at position {i+1}: '{arg}' is not a valid number"
                self.logger.warning("Validation failed: %s", error_msg)
                return False, error_msg

        # All validations passed
        return True, None

    def execute(self, *args, **kwargs) -> str:
        """
        Add the provided numbers together and return their sum.

        This method implements the addition operation by:
        1. First validating the input arguments
        2. Converting all validated arguments to floating-point numbers
        3. Computing their sum and returning the result as a string

        The implementation handles potential errors through appropriate
        exception handling, ensuring robust behavior even with unexpected inputs.

        Args:
            *args: Numbers to add together (as strings or numeric values)
            **kwargs: Not used for the addition operation

        Returns:
            str: The sum of the numbers formatted as a string,
                 or an error message if the operation fails
        """
        self.logger.info("Executing addition operation with args: %s", args)

        # Validate arguments using LBYL approach
        is_valid, error_message = self.validate_args(*args)
        if not is_valid:
            return error_message

        try:
            # Convert all arguments to float and compute their sum
            # Using a list comprehension for clarity and performance
            numbers = [float(arg) for arg in args]
            result = sum(numbers)

            # Handle potential edge cases
            if result == float('inf') or result == float('-inf'):
                error_msg = "Result is too large (infinity)"
                self.logger.warning(error_msg)
                return error_msg

            self.logger.info(f"Addition result: {result}")
            return str(result)
        except (ValueError, TypeError) as e:
            # This should not happen if validation passes, but defensive programming is good
            error_msg = f"Error during numeric conversion: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
        except OverflowError as e:
            # Handle numeric overflow
            error_msg = f"Numeric overflow during addition: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
        except Exception as e:
            # Catch-all for any unexpected errors
            error_msg = f"Unexpected error during addition: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return error_msg

# Register the addition operation with the factory
# This automatic registration enables the operation to be discovered
# and used without modifying any other part of the application
OperationFactory.register_operation('add', AddOperation)
