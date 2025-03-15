"""
Tests for the operation command mapper.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.plugins.operations.command_mapper import OperationCommand, register_operation_commands
from app.plugins.operations import OperationFactory

class TestOperationCommand:
    """Tests for the OperationCommand class."""
    
    def setup_method(self):
        """Set up for each test method."""
        # Create a mock operation that can be configured for different tests
        self.mock_operation = MagicMock()
        self.mock_operation.validate_args.return_value = (True, None)
        self.mock_operation.execute.return_value = "10"
        
        # Create the patcher for OperationFactory.create_operation
        self.patcher = patch('app.plugins.operations.OperationFactory.create_operation', 
                             return_value=self.mock_operation)
        self.mock_create_operation = self.patcher.start()
        
        # Create an operation command
        self.cmd = OperationCommand("add")
        
    def teardown_method(self):
        """Clean up after each test method."""
        self.patcher.stop()
    
    def test_init(self):
        """Test initialization of OperationCommand."""
        assert self.cmd.operation_name == "add"
    
    def test_execute_success(self):
        """Test successful execution of an operation command."""
        # Call the method
        result = self.cmd.execute("1", "2", "3")
        
        # Verify the result
        assert result == "10"
        
        # Verify the correct calls were made
        self.mock_create_operation.assert_called_once_with("add")
        self.mock_operation.execute.assert_called_once_with("1", "2", "3")
    
    def test_execute_operation_not_found(self):
        """Test execution when the operation is not found."""
        # Set up the mock to return None
        self.mock_create_operation.return_value = None
        
        # Call the method
        result = self.cmd.execute("1", "2", "3")
        
        # Verify the result
        assert "Error: No such operation" in result
        assert "add" in result
        
        # Verify the correct calls were made
        self.mock_create_operation.assert_called_once_with("add")
    
    def test_execute_validate_args_error(self):
        """Test execution when validate_args returns an error."""
        # Skip this test as the command_mapper doesn't use validate_args
        # The validate_args logic is now handled within the Operation classes
        pytest.skip("Command mapper doesn't use validate_args directly")
    
    def test_execute_operation_error(self):
        """Test execution when the operation raises an exception."""
        # Set up the mock
        self.mock_operation.execute.side_effect = Exception("Test error")
        
        # Call the method
        result = self.cmd.execute("1", "2", "3")
        
        # Verify the result - will return the exception as string
        assert isinstance(result, Exception) or "Test error" in str(result)
        
        # Verify the correct calls were made
        self.mock_create_operation.assert_called_once_with("add")
        self.mock_operation.execute.assert_called_once_with("1", "2", "3")

class TestRegisterOperationCommands:
    """Tests for the register_operation_commands function."""
    
    def test_register_operation_commands(self):
        """Test registering operation commands."""
        # Create mock command handler
        mock_handler = MagicMock()
        
        # Setup the patcher
        with patch('app.plugins.operations.OperationFactory.get_available_operations', 
                  return_value=["add", "subtract", "multiply", "divide"]) as mock_get_ops:
            # Call the function
            register_operation_commands(mock_handler)
            
            # Verify the correct calls were made
            mock_get_ops.assert_called_once()
        
            # verify register_command called for each operation
            assert mock_handler.register_command.call_count == 4
        
            # Check the arguments for each call
            for op_name in ["add", "subtract", "multiply", "divide"]:
                # Check if register_command was called with the operation name
                any_call_with_op = any(args[0] == op_name for args, _ in mock_handler.register_command.call_args_list)
                assert any_call_with_op, f"register_command not called with {op_name}"
    
    def test_register_operation_commands_no_operations(self):
        """Test registering operation commands when no operations are available."""
        # Create mock command handler
        mock_handler = MagicMock()
        
        # Setup the patcher
        with patch('app.plugins.operations.OperationFactory.get_available_operations', 
                  return_value=[]) as mock_get_ops:
            # Call the function
            register_operation_commands(mock_handler)
        
            # Verify the correct calls were made
            mock_get_ops.assert_called_once()
        
            # verify register_command was not called
            mock_handler.register_command.assert_not_called() 