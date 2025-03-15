"""
Addition operation plugin for the calculator application.

This module defines the addition operation, which adds multiple numbers together.
It demonstrates:
1. Concrete implementation of the Operation abstract base class
2. Automatic registration with the OperationFactory
3. Proper input validation and error handling
"""
import logging
from app.plugins.operations import Operation, OperationFactory

class AddOperation(Operation):
    """
    Addition operation that sums multiple numeric values.
    
    This operation takes two or more numeric arguments and returns their sum.
    It demonstrates proper argument validation, error handling, and logging.
    """
    
    def __init__(self):
        """Initialize the addition operation."""
        self.logger = logging.getLogger(__name__)
    
    def validate_args(self, *args, **kwargs):
        """
        Validate that the provided arguments are valid for addition.
        
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
        # Check if we have at least two numbers to add
        if len(args) < 2:
            error_msg = "Addition requires at least two numbers"
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
        Add the provided numbers together.
        
        This method first validates the arguments, then adds all numeric values.
        It handles potential errors and logs the operation details.
        
        Args:
            *args: Numbers to add together
            **kwargs: Not used for this operation
            
        Returns:
            str: The result of the addition as a string, or an error message
        """
        self.logger.info(f"Executing addition operation with args: {args}")
        
        # Validate arguments using LBYL (Look Before You Leap) approach
        is_valid, error_message = self.validate_args(*args)
        if not is_valid:
            return error_message
        
        try:
            # Convert all arguments to float and sum them
            result = sum(float(arg) for arg in args)
            self.logger.info(f"Addition result: {result}")
            return str(result)
        except Exception as e:
            # This should never happen if validation passes, but defensive programming is good
            error_msg = f"Error during addition operation: {str(e)}"
            self.logger.error(error_msg)
            return error_msg

# Register the addition operation with the factory
OperationFactory.register_operation('add', AddOperation) 