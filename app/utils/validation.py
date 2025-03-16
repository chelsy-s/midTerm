"""
Validation utilities for the calculator application.

This module provides common validation functions that can be used
across different parts of the application to ensure consistent
validation behavior.
"""
from typing import Tuple, Optional, List, Any

def validate_numeric_args(args: List[Any], min_args: int = 1) -> Tuple[bool, Optional[str]]:
    """
    Validate that arguments are numeric and meet minimum count requirements.
    
    This utility function centralizes the common validation logic used
    across different calculator operations.
    
    Args:
        args: List of arguments to validate
        min_args: Minimum number of arguments required
        
    Returns:
        tuple: (is_valid, error_message)
            - is_valid (bool): True if arguments are valid, False otherwise
            - error_message (str): Error message if invalid, None if valid
    """
    # Check if we have enough arguments
    if len(args) < min_args:
        error_msg = f"Operation requires at least {min_args} numbers"
        return False, error_msg
        
    # Check if all arguments can be converted to floats
    for i, arg in enumerate(args):
        try:
            float(arg)
        except (ValueError, TypeError):
            error_msg = f"Invalid argument at position {i+1}: '{arg}' is not a valid number"
            return False, error_msg
            
    return True, None 