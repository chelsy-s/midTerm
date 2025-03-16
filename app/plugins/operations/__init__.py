"""
Operations plugin package for the calculator application.

This package implements a flexible plugin architecture for calculator operations,
providing the foundation components:

1. Operation (ABC) - The abstract base class that defines the interface for all operations
2. OperationFactory - A factory class that creates and manages operation instances
3. Dynamic registration system for operation plugins

The design follows several key architectural principles:
- Factory Method pattern for creating operation instances
- Strategy pattern for interchangeable operation implementations
- Open/Closed principle allowing extension without modification
- Dependency inversion through abstraction

Operations are implemented as concrete subclasses and are dynamically
discovered and registered at runtime, providing a truly extensible architecture.
"""
import logging
import sys
from abc import ABC, abstractmethod
from typing import Dict, Type, Optional, List, Tuple, Union, Any, Callable

# Configure logger for operations package
logger = logging.getLogger(__name__)

class Operation(ABC):
    """
    Abstract base class for calculator operations.

    This class forms the foundation of the calculator's operation system,
    implementing the Strategy pattern where different concrete implementations
    provide varying mathematical operations while sharing a common interface.

    The abstract methods establish a contract that all operation implementations
    must fulfill:
    1. validate_args - Validates operation inputs before execution
    2. execute - Performs the actual mathematical operation

    This design allows for seamless extension with new operations without
    modifying existing code, demonstrating the Open/Closed Principle of
    SOLID design.
    """

    @abstractmethod
    def validate_args(self, *args, **kwargs) -> Tuple[bool, Optional[str]]:
        """
        Validate arguments for the operation.

        This method verifies that the provided arguments are valid for this
        specific operation before attempting to execute it. It typically checks:
        - That a minimum number of arguments are provided
        - That all arguments can be converted to appropriate numeric types
        - That any operation-specific constraints are satisfied

        Args:
            *args: Positional arguments to validate (typically numbers as strings)
            **kwargs: Keyword arguments to validate (operation-specific)

        Returns:
            tuple: (is_valid, error_message)
                - is_valid (bool): True if arguments are valid, False otherwise
                - error_message (str): Descriptive error message if invalid, None if valid
        """
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> str:
        """
        Execute the operation with the provided arguments.

        This method performs the actual mathematical operation using the
        provided arguments after they have been validated. It should:
        1. Validate inputs (typically by calling validate_args)
        2. Perform the mathematical operation
        3. Handle any exceptions appropriately
        4. Return the result formatted as a string

        Args:
            *args: Positional arguments for the operation (typically numbers as strings)
            **kwargs: Keyword arguments for the operation (operation-specific)

        Returns:
            str: The result of the operation formatted as a string,
                 or an error message if the operation fails

        Raises:
            Should catch and handle most exceptions internally, returning error messages
            rather than propagating exceptions to maintain robustness
        """
        pass

class OperationFactory:
    """
    Factory for creating and managing operation instances.

    This class implements the Factory Method pattern, centralizing the
    creation and management of Operation objects. This decouples the
    clients (commands, REPL) from the concrete operation implementations,
    promoting loose coupling and maintainability.

    The factory maintains a registry of available operations and provides
    methods to:
    1. Register new operation types dynamically
    2. Create instances of registered operations on demand
    3. Discover available operations for runtime introspection

    As a static registry (class methods and class variables), it functions
    as a singleton without explicitly implementing the Singleton pattern.
    """
    # Registry of available operations - maps operation names to their classes
    _operations: Dict[str, Type[Operation]] = {}

    @classmethod
    def register_operation(cls, name: str, operation_class: Type[Operation]) -> bool:
        """
        Register an operation class with the factory.

        This method adds a new operation type to the registry, making it
        available for creation through the factory. It verifies that the
        provided class is a valid Operation subclass before registration.

        Args:
            name: Name to register the operation under (used as the key)
            operation_class: The Operation subclass to register

        Returns:
            bool: True if registration was successful, False otherwise
        """
        # Validate that the class is a subclass of Operation (LBYL approach)
        if not issubclass(operation_class, Operation):
            logger.error(f"Cannot register {name}: Class must be a subclass of Operation")
            return False

        # Check if operation is already registered
        if name in cls._operations:
            logger.warning(f"Operation '{name}' already registered, overwriting previous implementation")

        # Add to the operations registry
        cls._operations[name] = operation_class
        logger.info(f"Registered operation: '{name}' ({operation_class.__name__})")
        return True

    @classmethod
    def create_operation(cls, name: str) -> Optional[Operation]:
        """
        Create an instance of the specified operation.

        This method instantiates and returns an operation object based on
        the registered operation class. It demonstrates error handling using
        the EAFP approach (try/except) for robustness.

        Args:
            name: Name of the operation to create (must be registered)

        Returns:
            Operation: An instance of the requested Operation or None if not found
        """
        # Check if the operation exists in the registry (LBYL approach)
        if name not in cls._operations:
            logger.warning(f"Operation not found: '{name}'")
            return None

        # Create and return a new instance (EAFP approach for instantiation)
        try:
            operation_class = cls._operations[name]
            operation_instance = operation_class()
            logger.debug(f"Created operation instance: '{name}' ({operation_class.__name__})")
            return operation_instance
        except Exception as e:
            logger.error(f"Error creating operation '{name}': {str(e)}", exc_info=True)
            return None

    @classmethod
    def get_available_operations(cls) -> List[str]:
        """
        Get the names of all registered operations.

        This method provides runtime introspection of available operations,
        which is useful for implementing help commands, auto-completion,
        and dynamic user interfaces.

        Returns:
            list: Sorted list of operation names for consistent ordering
        """
        return sorted(cls._operations.keys())

    @classmethod
    def get_operation_info(cls, name: str) -> Dict[str, Any]:
        """
        Get detailed information about a registered operation.

        This method provides metadata about a specific operation,
        useful for generating help text and documentation.

        Args:
            name: Name of the operation to get information for

        Returns:
            dict: Dictionary containing operation metadata,
                 or empty dict if operation not found
        """
        if name not in cls._operations:
            return {}

        operation_class = cls._operations[name]
        return {
            'name': name,
            'class': operation_class.__name__,
            'docstring': operation_class.__doc__ or "No documentation available",
            'module': operation_class.__module__
        }