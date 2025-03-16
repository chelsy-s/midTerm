"""
Multiplication operation plugin for the calculator application.

This module defines the multiplication operation, which multiplies multiple numbers
together. It demonstrates:
1. Concrete implementation of the Operation abstract base class
2. Professional error handling and validation
3. Comprehensive logging for operation tracking
"""
import logging
from app.plugins.operations import Operation, OperationFactory

class MultiplyOperation(Operation):
    """
    Multiplication operation that calculates the product of multiple numbers.

    This operation takes two or more numeric arguments and multiplies them
    together to produce their product.
    """

    def __init__(self):
        """Initialize the multiplication operation."""
        self.logger = logging.getLogger(__name__)

    def validate_args(self, *args, **kwargs):
        """
        Validate that the provided arguments are valid for multiplication.

        This method checks that:
        1. At least two arguments are provided
        2. All arguments can be converted to floating point numbers

        Args:
            *args: The arguments to validate (should be numbers)
            **kwargs: Not used for this operation

        Returns:
            tuple: (is_valid, error_message)
                - is_valid (bool): True if arguments are valid, False otherwise
                - error_message (str): Error message if arguments are invalid, None otherwise
        """
        # Check if we have at least two numbers
        if len(args) < 2:
            error_msg = "Multiplication requires at least two numbers"
            self.logger.warning("Validation failed: %s", error_msg)
            return False, error_msg

        # Check if all arguments can be converted to floats
        for i, arg in enumerate(args):
            try:
                float(arg)
            except (ValueError, TypeError):
                error_msg = f"Invalid argument at position {i+1}: '{arg}' is not a valid number"
                self.logger.warning("Validation failed: %s", error_msg)
                return False, error_msg

        return True, None

    def execute(self, *args, **kwargs):
        """
        Perform the multiplication operation.

        This method multiplies all the provided numbers together.
        It first validates the arguments, then performs the multiplication.

        Args:
            *args: Numbers to multiply together
            **kwargs: Not used for this operation

        Returns:
            str: The result of the multiplication as a string, or an error message
        """
        self.logger.info("Executing multiplication operation with args: %s", args)

        # Validate arguments using LBYL (Look Before You Leap) approach
        is_valid, error_message = self.validate_args(*args)
        if not is_valid:
            return error_message

        try:
            # Convert all arguments to float and perform multiplication
            result = 1.0  # Identity element for multiplication
            for arg in args:
                result *= float(arg)

            self.logger.info("Multiplication result: %s", result)
            return str(result)
        except (ValueError, TypeError, AttributeError) as e:
            # This should never happen if validation passes, but defensive programming is good
            error_msg = f"Error during multiplication operation: {str(e)}"
            self.logger.error(error_msg)
            return error_msg

# Register the multiplication operation with the factory
OperationFactory.register_operation('multiply', MultiplyOperation)
