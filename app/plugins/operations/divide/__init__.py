"""
Division operation plugin for the calculator application.

This module defines the division operation, which divides the first number by
subsequent numbers. It demonstrates:
1. Concrete implementation of the Operation abstract base class
2. Professional error handling including division by zero
3. EAFP (Easier to Ask for Forgiveness than Permission) approach for errors
"""
import logging
from app.plugins.operations import Operation, OperationFactory

class DivideOperation(Operation):
    """
    Division operation that performs sequential division of numbers.
    
    This operation takes two or more numeric arguments and divides
    the first number by all subsequent numbers. It handles special
    cases like division by zero with appropriate error messages.
    """
    
    def __init__(self):
        """Initialize the division operation."""
        self.logger = logging.getLogger(__name__)
    
    def validate_args(self, *args, **kwargs):
        """
        Validate that the provided arguments are valid for division.
        
        This method checks that:
        1. At least two arguments are provided
        2. All arguments can be converted to floating point numbers
        
        Note: Zero division errors are handled in execute(), following
        the EAFP (Easier to Ask for Forgiveness than Permission) approach.
        
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
            error_msg = "Division requires at least two numbers"
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
        Perform the division operation.
        
        This method divides the first number by all subsequent numbers.
        It uses the EAFP approach for handling division by zero.
        
        Args:
            *args: Numbers to use in division
            **kwargs: Not used for this operation
            
        Returns:
            str: The result of the division as a string, or an error message
        """
        self.logger.info(f"Executing division operation with args: {args}")
        
        # Validate arguments
        is_valid, error_message = self.validate_args(*args)
        if not is_valid:
            return error_message
        
        try:
            # Convert all arguments to float
            numbers = [float(arg) for arg in args]
            result = numbers[0]  # Start with the first number
            
            # Divide by each subsequent number using EAFP approach
            for num in numbers[1:]:
                result /= num  # This will raise ZeroDivisionError if num is 0
                
            self.logger.info(f"Division result: {result}")
            return str(result)
            
        except ZeroDivisionError:
            # Handle division by zero specifically
            error_msg = "Error: Division by zero is not allowed"
            self.logger.warning(error_msg)
            return error_msg
            
        except Exception as e:
            # Handle other unexpected errors
            error_msg = f"Error during division operation: {str(e)}"
            self.logger.error(error_msg)
            return error_msg

# Register the division operation with the factory
OperationFactory.register_operation('divide', DivideOperation) 