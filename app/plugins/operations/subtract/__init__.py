"""
Subtraction operation plugin for the calculator application.

This module defines the subtraction operation, which subtracts subsequent numbers
from the first number. It demonstrates:
1. Concrete implementation of the Operation abstract base class
2. Professional error handling and validation
3. Comprehensive logging for operation tracking
"""
import logging
from app.plugins.operations import Operation, OperationFactory

class SubtractOperation(Operation):
    """
    Subtraction operation that calculates the difference between numbers.
    
    This operation takes two or more numeric arguments and subtracts
    all subsequent values from the first value.
    """
    
    def __init__(self):
        """Initialize the subtraction operation."""
        self.logger = logging.getLogger(__name__)
    
    def validate_args(self, *args, **kwargs):
        """
        Validate that the provided arguments are valid for subtraction.
        
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
            error_msg = "Subtraction requires at least two numbers"
            self.logger.warning(f"Validation failed: {error_msg}")
            return False, error_msg
            
        # Check if all arguments can be converted to floats
        for i, arg in enumerate(args):
            try:
                float(arg)
            except (ValueError, TypeError):
                error_msg = f"Invalid argument at position {i+1}: '{arg}' is not a valid number"
                self.logger.warning(f"Validation failed: {error_msg}")
                return False, error_msg
                
        return True, None
        
    def execute(self, *args, **kwargs):
        """
        Perform the subtraction operation.
        
        This method subtracts all subsequent numbers from the first number.
        It first validates the arguments, then performs the subtraction.
        
        Args:
            *args: Numbers to use in subtraction
            **kwargs: Not used for this operation
            
        Returns:
            str: The result of the subtraction as a string, or an error message
        """
        self.logger.info(f"Executing subtraction operation with args: {args}")
        
        # Validate arguments
        is_valid, error_message = self.validate_args(*args)
        if not is_valid:
            return error_message
        
        try:
            # Convert all arguments to float and perform subtraction
            numbers = [float(arg) for arg in args]
            result = numbers[0]  # Start with the first number
            
            # Subtract all subsequent numbers
            for num in numbers[1:]:
                result -= num
                
            self.logger.info(f"Subtraction result: {result}")
            return str(result)
        except Exception as e:
            # This should never happen if validation passes, but defensive programming is good
            error_msg = f"Error during subtraction operation: {str(e)}"
            self.logger.error(error_msg)
            return error_msg

# Register the subtraction operation with the factory
OperationFactory.register_operation('subtract', SubtractOperation) 