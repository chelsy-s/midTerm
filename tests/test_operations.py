"""
Tests for calculator operations.
"""
import pytest
import logging
from app.plugins.operations import OperationFactory, Operation
from app.plugins.operations.add import AddOperation
from app.plugins.operations.subtract import SubtractOperation
from app.plugins.operations.multiply import MultiplyOperation
from app.plugins.operations.divide import DivideOperation

# Test abstract class Operation
class TestOperation:
    """Tests for the Operation abstract base class."""

    class ConcreteOperation(Operation):
        """Concrete implementation of Operation for testing."""
        def validate_args(self, *args, **kwargs):
            return True, None

        def execute(self, *args, **kwargs):
            return "Executed"

    def test_operation_abstract_methods(self):
        """Test that concrete subclasses must implement abstract methods."""
        concrete_op = self.ConcreteOperation()
        assert concrete_op.execute() == "Executed"
        assert concrete_op.validate_args() == (True, None)

class TestOperationFactory:
    """Tests for the OperationFactory."""

    def test_register_and_create_operation(self):
        """Test registering and creating operations through the factory."""
        # Clear existing operations to ensure clean test
        OperationFactory._operations = {}

        # Register operations
        OperationFactory.register_operation("test_add", AddOperation)
        OperationFactory.register_operation("test_subtract", SubtractOperation)

        # Create operations
        add_op = OperationFactory.create_operation("test_add")
        subtract_op = OperationFactory.create_operation("test_subtract")

        # Verify operations were created and are of the correct type
        assert isinstance(add_op, AddOperation)
        assert isinstance(subtract_op, SubtractOperation)

        # Verify getting a non-existent operation returns None
        assert OperationFactory.create_operation("nonexistent") is None

    def test_get_available_operations(self):
        """Test getting available operations."""
        # Clear existing operations to ensure clean test
        OperationFactory._operations = {}

        # Register operations
        OperationFactory.register_operation("test_add", AddOperation)
        OperationFactory.register_operation("test_subtract", SubtractOperation)

        # Get available operations
        available_ops = OperationFactory.get_available_operations()

        # Verify available operations
        assert "test_add" in available_ops
        assert "test_subtract" in available_ops
        assert len(available_ops) == 2

class TestAddOperation:
    """Tests for the AddOperation."""

    def setup_method(self):
        """Set up for each test method."""
        self.operation = AddOperation()

    def test_validate_args_valid(self):
        """Test validation with valid arguments."""
        is_valid, _ = self.operation.validate_args("1", "2")
        assert is_valid is True

        is_valid, _ = self.operation.validate_args("1", "2", "3")
        assert is_valid is True

        is_valid, _ = self.operation.validate_args("1.5", "2.5")
        assert is_valid is True

    def test_validate_args_invalid(self):
        """Test validation with invalid arguments."""
        is_valid, _ = self.operation.validate_args("1")  # Not enough args
        assert is_valid is False

        is_valid, _ = self.operation.validate_args()  # No args
        assert is_valid is False

        is_valid, _ = self.operation.validate_args("1", "x")  # Non-numeric
        assert is_valid is False

        is_valid, _ = self.operation.validate_args("x", "2")  # Non-numeric
        assert is_valid is False

    def test_execute_success(self):
        """Test successful execution."""
        assert self.operation.execute("1", "2") == "3.0"
        assert self.operation.execute("1", "2", "3") == "6.0"
        assert self.operation.execute("-1", "2") == "1.0"
        assert self.operation.execute("1.5", "2.5") == "4.0"

    def test_execute_invalid_args(self):
        """Test execution with invalid arguments."""
        # With our improved code, invalid args now returns a clear error message
        result = self.operation.execute("1")  # Not enough args
        assert "requires at least two numbers" in result

        result = self.operation.execute()  # No args
        assert "requires at least two numbers" in result

        result = self.operation.execute("1", "x")  # Non-numeric
        assert "is not a valid number" in result

        result = self.operation.execute("x", "2")  # Non-numeric
        assert "is not a valid number" in result

    def test_execute_unexpected_error(self, monkeypatch):
        """Test execution with an unexpected error."""
        # Patch validate_args to return True, None but cause an error in execution
        monkeypatch.setattr(self.operation, 'validate_args', lambda *args, **kwargs: (True, None))

        # Create a function that will raise an exception when converting args to float
        original_float = float
        def mock_float(arg):
            if isinstance(arg, str) and arg.isdigit():
                # Raise an exception for numeric strings to simulate an error
                raise ValueError("Test error")
            return original_float(arg)

        with monkeypatch.context() as m:
            m.setattr('builtins.float', mock_float)
            result = self.operation.execute("1", "2")
            assert "Error" in result

class TestSubtractOperation:
    """Tests for the SubtractOperation."""

    def setup_method(self):
        """Set up for each test method."""
        self.operation = SubtractOperation()

    def test_validate_args_valid(self):
        """Test validation with valid arguments."""
        is_valid, _ = self.operation.validate_args("10", "2")
        assert is_valid is True

        is_valid, _ = self.operation.validate_args("10", "2", "3")
        assert is_valid is True

        is_valid, _ = self.operation.validate_args("10.5", "2.5")
        assert is_valid is True

    def test_validate_args_invalid(self):
        """Test validation with invalid arguments."""
        is_valid, _ = self.operation.validate_args("10")  # Not enough args
        assert is_valid is False

        is_valid, _ = self.operation.validate_args()  # No args
        assert is_valid is False

        is_valid, _ = self.operation.validate_args("10", "x")  # Non-numeric
        assert is_valid is False

        is_valid, _ = self.operation.validate_args("x", "2")  # Non-numeric
        assert is_valid is False

    def test_execute_success(self):
        """Test successful execution."""
        assert self.operation.execute("10", "2") == "8.0"
        assert self.operation.execute("10", "2", "3") == "5.0"
        assert self.operation.execute("10", "-2") == "12.0"
        assert self.operation.execute("10.5", "2.5") == "8.0"

    def test_execute_invalid_args(self):
        """Test execution with invalid arguments."""
        # With our improved code, invalid args now returns a clear error message
        result = self.operation.execute("10")  # Not enough args
        assert "requires at least two numbers" in result

        result = self.operation.execute()  # No args
        assert "requires at least two numbers" in result

        result = self.operation.execute("10", "x")  # Non-numeric
        assert "is not a valid number" in result

        result = self.operation.execute("x", "2")  # Non-numeric
        assert "is not a valid number" in result

    def test_execute_unexpected_error(self, monkeypatch):
        """Test execution with an unexpected error during subtraction."""
        # Patch validate_args to return True, None but cause an error in execution
        monkeypatch.setattr(self.operation, 'validate_args', lambda *args, **kwargs: (True, None))

        # Patch float to raise an exception for the second argument
        original_float = float
        call_count = 0

        def mock_float(value):
            nonlocal call_count
            call_count += 1
            if call_count == 2:  # The second float call (first subtraction)
                raise ValueError("Test error")
            return original_float(value)

        with monkeypatch.context() as m:
            m.setattr('builtins.float', mock_float)
            result = self.operation.execute("10", "2")
            assert "Error" in result

class TestMultiplyOperation:
    """Tests for the MultiplyOperation."""

    def setup_method(self):
        """Set up for each test method."""
        self.operation = MultiplyOperation()

    def test_validate_args_valid(self):
        """Test validation with valid arguments."""
        is_valid, _ = self.operation.validate_args("5", "2")
        assert is_valid is True

        is_valid, _ = self.operation.validate_args("5", "2", "3")
        assert is_valid is True

        is_valid, _ = self.operation.validate_args("5.5", "2.5")
        assert is_valid is True

    def test_validate_args_invalid(self):
        """Test validation with invalid arguments."""
        is_valid, _ = self.operation.validate_args("5")  # Not enough args
        assert is_valid is False

        is_valid, _ = self.operation.validate_args()  # No args
        assert is_valid is False

        is_valid, _ = self.operation.validate_args("5", "x")  # Non-numeric
        assert is_valid is False

        is_valid, _ = self.operation.validate_args("x", "2")  # Non-numeric
        assert is_valid is False

    def test_execute_success(self):
        """Test successful execution."""
        assert self.operation.execute("5", "2") == "10.0"
        assert self.operation.execute("5", "2", "3") == "30.0"
        assert self.operation.execute("5", "-2") == "-10.0"
        assert self.operation.execute("5.5", "2") == "11.0"
        assert self.operation.execute("5", "0") == "0.0"  # Multiply by zero

    def test_execute_invalid_args(self):
        """Test execution with invalid arguments."""
        # With our improved code, invalid args now returns a clear error message
        result = self.operation.execute("5")  # Not enough args
        assert "requires at least two numbers" in result

        result = self.operation.execute()  # No args
        assert "requires at least two numbers" in result

        result = self.operation.execute("5", "x")  # Non-numeric
        assert "is not a valid number" in result

        result = self.operation.execute("x", "2")  # Non-numeric
        assert "is not a valid number" in result

    def test_execute_unexpected_error(self, monkeypatch):
        """Test execution with an unexpected error during multiplication."""
        # Patch validate_args to return True, None but cause an error in execution
        monkeypatch.setattr(self.operation, 'validate_args', lambda *args, **kwargs: (True, None))

        # Create a function that will raise an exception when converting args to float
        original_float = float
        def mock_float(arg):
            if isinstance(arg, str) and arg.isdigit():
                # Raise an exception for numeric strings to simulate an error
                raise ValueError("Test error in multiplication")
            return original_float(arg)

        with monkeypatch.context() as m:
            m.setattr('builtins.float', mock_float)
            result = self.operation.execute("5", "2")
            assert "Error" in result

class TestDivideOperation:
    """Tests for the DivideOperation."""

    def setup_method(self):
        """Set up for each test method."""
        self.operation = DivideOperation()

    def test_validate_args_valid(self):
        """Test validation with valid arguments."""
        is_valid, _ = self.operation.validate_args("10", "2")
        assert is_valid is True

        is_valid, _ = self.operation.validate_args("10", "2", "5")
        assert is_valid is True

        is_valid, _ = self.operation.validate_args("10.5", "2.5")
        assert is_valid is True

    def test_validate_args_invalid(self):
        """Test validation with invalid arguments."""
        is_valid, _ = self.operation.validate_args("10")  # Not enough args
        assert is_valid is False

        is_valid, _ = self.operation.validate_args()  # No args
        assert is_valid is False

        is_valid, _ = self.operation.validate_args("10", "x")  # Non-numeric
        assert is_valid is False

        is_valid, _ = self.operation.validate_args("x", "2")  # Non-numeric
        assert is_valid is False

    def test_execute_success(self):
        """Test successful execution."""
        assert self.operation.execute("10", "2") == "5.0"
        assert self.operation.execute("10", "2", "5") == "1.0"
        assert self.operation.execute("10", "-2") == "-5.0"
        assert self.operation.execute("10.5", "3") == "3.5"

    def test_execute_division_by_zero(self):
        """Test execution with division by zero."""
        result = self.operation.execute("10", "0")  # Division by zero
        assert "division by zero" in result.lower()

        result = self.operation.execute("10", "2", "0")  # Division by zero
        assert "division by zero" in result.lower()

    def test_execute_invalid_args(self):
        """Test execution with invalid arguments."""
        # With our improved code, invalid args now returns a clear error message
        result = self.operation.execute("10")  # Not enough args
        assert "requires at least two numbers" in result

        result = self.operation.execute()  # No args
        assert "requires at least two numbers" in result

        result = self.operation.execute("10", "x")  # Non-numeric
        assert "is not a valid number" in result

        result = self.operation.execute("x", "2")  # Non-numeric
        assert "is not a valid number" in result

    def test_execute_zero_division_error(self):
        """Test execution with a ZeroDivisionError directly."""
        # We'll just verify the error message directly from division by zero
        result = self.operation.execute("10", "0")
        assert "division by zero" in result.lower()

    def test_execute_unexpected_error(self, monkeypatch):
        """Test execution with an unexpected error during division."""
        # Patch validate_args to return True, None but cause an error in execution
        monkeypatch.setattr(self.operation, 'validate_args', lambda *args, **kwargs: (True, None))

        # Patch float to raise an exception
        original_float = float
        call_count = 0

        def mock_float(value):
            nonlocal call_count
            call_count += 1
            if call_count > 1:  # After the first argument
                raise ValueError("Test error")
            return original_float(value)

        with monkeypatch.context() as m:
            m.setattr('builtins.float', mock_float)
            result = self.operation.execute("10", "2")
            assert "Error" in result

class TestMenuCommand:
    """Tests for the MenuCommand."""

    def test_menu_display(self, monkeypatch):
        """Test the menu command displays operations correctly."""
        from app.plugins.menu import MenuCommand

        # Create mock operations for display
        class MockAddOperation(Operation):
            """Mock addition operation for testing."""
            def validate_args(self, *args, **kwargs):
                return True, None

            def execute(self, *args, **kwargs):
                return "Added"

        # Mock the OperationFactory.get_available_operations method
        def mock_get_available_operations():
            return ["add", "divide", "multiply", "subtract"]

        # Mock the create_operation method to return our mock operations
        def mock_create_operation(name):
            return MockAddOperation()

        monkeypatch.setattr(OperationFactory, "get_available_operations", mock_get_available_operations)
        monkeypatch.setattr(OperationFactory, "create_operation", mock_create_operation)

        # Create menu command and execute
        menu_cmd = MenuCommand()
        result = menu_cmd.execute()

        # Verify result contains all operations and expected formatting
        assert "=== Available Calculator Operations ===" in result
        assert "add:" in result
        assert "divide:" in result
        assert "multiply:" in result
        assert "subtract:" in result
        assert "To use an operation" in result

    def test_menu_display_no_operations(self, monkeypatch):
        """Test the menu command handles no available operations."""
        from app.plugins.menu import MenuCommand

        # Mock empty operation list
        monkeypatch.setattr(
            OperationFactory,
            "get_available_operations",
            lambda: []
        )

        # Create menu command and execute
        menu_cmd = MenuCommand()
        result = menu_cmd.execute()

        # Verify result indicates no operations
        assert "No calculator operations are currently available" in result

    def test_menu_command_init(self):
        """Test the MenuCommand initialization."""
        from app.plugins.menu import MenuCommand
        menu_cmd = MenuCommand()
        assert hasattr(menu_cmd, 'logger')
