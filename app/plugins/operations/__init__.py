"""
Operations plugin package for the calculator application.

This package defines:
1. The Operation abstract base class that all calculator operations must implement
2. The OperationFactory for creating operation instances (Factory Method pattern)
3. Registration system for operation plugins

Operations implemented as concrete subclasses are dynamically loaded and registered
with the OperationFactory at runtime, demonstrating the plugin architecture and
Open/Closed principle of SOLID design.
"""
import logging
from abc import ABC, abstractmethod
import sys

# Configure logger for operations package
logger = logging.getLogger(__name__)

class Operation(ABC):
    """
    Abstract base class for calculator operations.
    
    This class forms the foundation of the calculator's operation system,
    implementing the Strategy pattern. Each concrete subclass represents
    a different mathematical operation strategy.
    
    All operations must implement:
    1. validate_args - to check if the provided arguments are valid
    2. execute - to perform the actual mathematical operation
    
    This design allows for easy extension with new operations without
    modifying existing code (Open/Closed Principle).
    """
    
    @abstractmethod
    def validate_args(self, *args, **kwargs):
        """
        Validate arguments for the operation.
        
        This method checks if the provided arguments are valid for this
        particular operation before attempting to execute it.
        
        Args:
            *args: Arguments to validate
            **kwargs: Keyword arguments to validate
            
        Returns:
            tuple: (is_valid, error_message)
                - is_valid (bool): True if arguments are valid, False otherwise
                - error_message (str): Error message if arguments are invalid, None otherwise
        """
        pass
        
    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute the operation with the provided arguments.
        
        This method performs the actual mathematical operation using the
        provided arguments after they have been validated.
        
        Args:
            *args: Arguments for the operation
            **kwargs: Keyword arguments for the operation
            
        Returns:
            The result of the operation
        
        Raises:
            Various exceptions depending on the specific operation
        """
        pass

class OperationFactory:
    """
    Factory for creating operation instances.
    
    This class implements the Factory Method pattern, centralizing
    the creation and management of Operation objects. This decouples
    the clients (commands, REPL) from the concrete operation classes.
    
    The factory maintains a registry of available operations and
    provides methods to:
    1. Register new operation types
    2. Create instances of registered operations
    3. Retrieve a list of available operations
    """
    # Registry of available operations
    _operations = {}
    
    @classmethod
    def register_operation(cls, name, operation_class):
        """
        Register an operation class with the factory.
        
        Args:
            name: Name to register the operation under
            operation_class: The Operation subclass to register
            
        Returns:
            bool: True if registration was successful, False otherwise
        """
        # Validate that the class is a subclass of Operation
        if not issubclass(operation_class, Operation):
            logger.error(f"Cannot register {name}: Class must be a subclass of Operation")
            return False
            
        # Add to the operations registry
        cls._operations[name] = operation_class
        logger.info(f"Registered operation: {name}")
        return True
        
    @classmethod
    def create_operation(cls, name):
        """
        Create an instance of the specified operation.
        
        Args:
            name: Name of the operation to create
            
        Returns:
            An instance of the requested Operation or None if not found
        """
        # Check if the operation exists in the registry
        if name not in cls._operations:
            logger.warning(f"Operation not found: {name}")
            return None
            
        # Create and return a new instance
        try:
            operation_instance = cls._operations[name]()
            logger.debug(f"Created operation instance: {name}")
            return operation_instance
        except Exception as e:
            logger.error(f"Error creating operation {name}: {str(e)}")
            return None
    
    @classmethod
    def get_available_operations(cls):
        """
        Get the names of all registered operations.
        
        Returns:
            list: List of operation names
        """
        return list(cls._operations.keys()) 