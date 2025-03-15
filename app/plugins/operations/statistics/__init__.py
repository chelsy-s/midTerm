"""
Statistical operations plugins for the calculator application.

This module defines statistical operations like mean, median, and standard deviation.
It demonstrates:
1. Extending the calculator with new operation types
2. Implementation of statistical calculations
3. Proper input validation and error handling
"""
import logging
import statistics
from app.plugins.operations import Operation, OperationFactory

class MeanOperation(Operation):
    """
    Mean operation that calculates the arithmetic mean (average) of multiple numbers.
    
    This operation takes two or more numeric arguments and returns their arithmetic mean.
    It demonstrates proper argument validation, error handling, and logging.
    """
    
    def __init__(self):
        """Initialize the mean operation."""
        self.logger = logging.getLogger(__name__)
    
    def validate_args(self, *args, **kwargs):
        """
        Validate that the provided arguments are valid for calculating the mean.
        
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
            error_msg = "Mean calculation requires at least two numbers"
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
        Calculate the mean of the provided numbers.
        
        This method first validates the arguments, then calculates their mean.
        It handles potential errors and logs the operation details.
        
        Args:
            *args: Numbers to calculate the mean of
            **kwargs: Not used for this operation
            
        Returns:
            str: The result of the mean calculation as a string, or an error message
        """
        self.logger.info(f"Executing mean operation with args: {args}")
        
        # Validate arguments
        is_valid, error_message = self.validate_args(*args)
        if not is_valid:
            return error_message
        
        try:
            # Convert all arguments to float and calculate mean
            numbers = [float(arg) for arg in args]
            result = statistics.mean(numbers)
            self.logger.info(f"Mean calculation result: {result}")
            return str(result)
        except Exception as e:
            # This should never happen if validation passes, but defensive programming is good
            error_msg = f"Error during mean calculation: {str(e)}"
            self.logger.error(error_msg)
            return error_msg

class MedianOperation(Operation):
    """
    Median operation that calculates the median value of multiple numbers.
    
    This operation takes an odd or even number of numeric arguments and returns their median value.
    For an even number of arguments, it returns the average of the two middle values.
    """
    
    def __init__(self):
        """Initialize the median operation."""
        self.logger = logging.getLogger(__name__)
    
    def validate_args(self, *args, **kwargs):
        """
        Validate that the provided arguments are valid for calculating the median.
        
        This method checks that:
        1. At least three arguments are provided (for a meaningful median)
        2. All arguments can be converted to floating point numbers
        
        Args:
            *args: The arguments to validate (should be numbers)
            **kwargs: Not used for this operation
            
        Returns:
            tuple: (is_valid, error_message)
                - is_valid (bool): True if arguments are valid, False otherwise
                - error_message (str): Error message if arguments are invalid, None otherwise
        """
        # Check if we have at least three numbers for a meaningful median
        if len(args) < 3:
            error_msg = "Median calculation requires at least three numbers for meaningful results"
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
        Calculate the median of the provided numbers.
        
        This method first validates the arguments, then calculates their median.
        It handles potential errors and logs the operation details.
        
        Args:
            *args: Numbers to calculate the median of
            **kwargs: Not used for this operation
            
        Returns:
            str: The result of the median calculation as a string, or an error message
        """
        self.logger.info(f"Executing median operation with args: {args}")
        
        # Validate arguments
        is_valid, error_message = self.validate_args(*args)
        if not is_valid:
            return error_message
        
        try:
            # Convert all arguments to float and calculate median
            numbers = [float(arg) for arg in args]
            result = statistics.median(numbers)
            self.logger.info(f"Median calculation result: {result}")
            return str(result)
        except Exception as e:
            error_msg = f"Error during median calculation: {str(e)}"
            self.logger.error(error_msg)
            return error_msg

class StddevOperation(Operation):
    """
    Standard Deviation operation that calculates the standard deviation of multiple numbers.
    
    This operation takes two or more numeric arguments and returns their sample standard deviation.
    """
    
    def __init__(self):
        """Initialize the standard deviation operation."""
        self.logger = logging.getLogger(__name__)
    
    def validate_args(self, *args, **kwargs):
        """
        Validate that the provided arguments are valid for calculating the standard deviation.
        
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
            error_msg = "Standard deviation calculation requires at least two numbers"
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
        Calculate the standard deviation of the provided numbers.
        
        This method first validates the arguments, then calculates their standard deviation.
        It handles potential errors and logs the operation details.
        
        Args:
            *args: Numbers to calculate the standard deviation of
            **kwargs: Not used for this operation
            
        Returns:
            str: The result of the standard deviation calculation as a string, or an error message
        """
        self.logger.info(f"Executing standard deviation operation with args: {args}")
        
        # Validate arguments
        is_valid, error_message = self.validate_args(*args)
        if not is_valid:
            return error_message
        
        try:
            # Convert all arguments to float and calculate standard deviation
            numbers = [float(arg) for arg in args]
            # Calculate sample standard deviation (n-1 denominator)
            result = statistics.stdev(numbers)
            self.logger.info(f"Standard deviation calculation result: {result}")
            return str(result)
        except Exception as e:
            error_msg = f"Error during standard deviation calculation: {str(e)}"
            self.logger.error(error_msg)
            return error_msg

# Register the statistical operations with the factory
OperationFactory.register_operation('mean', MeanOperation)
OperationFactory.register_operation('median', MedianOperation)
OperationFactory.register_operation('stddev', StddevOperation) 