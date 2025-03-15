"""
Tests for the core App class and command functionality.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.commands import Command, CommandHandler
from app import App

class TestCommand(Command):
    """Test command implementation for testing."""
    def execute(self, *args, **kwargs):
        """Execute the test command."""
        return "TestCommand executed"

class TestCommandHandler:
    """Tests for the CommandHandler class."""
    
    def test_register_command(self):
        """Test registering a command."""
        handler = CommandHandler()
        cmd = TestCommand()
        handler.register_command("test", cmd)
        assert "test" in handler.commands
        assert handler.commands["test"] == cmd
        
    def test_execute_command_lbyl(self):
        """Test executing a command with LBYL approach."""
        handler = CommandHandler()
        cmd = TestCommand()
        handler.register_command("test", cmd)
        
        # Test existing command
        result = handler.execute_command("test")
        assert result == "TestCommand executed"
        
        # Test non-existent command
        result = handler.execute_command("nonexistent")
        assert "No such command" in result
        
    def test_execute_command_eafp(self):
        """Test executing a command with EAFP approach."""
        handler = CommandHandler()
        cmd = TestCommand()
        handler.register_command("test", cmd)
        
        # Test existing command
        result = handler.execute_command_eafp("test")
        assert result == "TestCommand executed"
        
        # Test non-existent command
        result = handler.execute_command_eafp("nonexistent")
        assert "No such command" in result

class TestApp:
    """Tests for the App class."""
    
    @patch('os.makedirs')
    @patch('logging.config.fileConfig')
    @patch('dotenv.load_dotenv')
    def test_init(self, mock_load_dotenv, mock_fileConfig, mock_makedirs):
        """Test App initialization."""
        app = App()
        mock_makedirs.assert_called_once_with('logs', exist_ok=True)
        mock_load_dotenv.assert_called_once()
        assert app.settings.get('ENVIRONMENT') == 'PRODUCTION'
        
    def test_get_environment_variable(self):
        """Test getting environment variables."""
        with patch.dict('os.environ', {'TEST_VAR': 'test_value'}):
            app = App()
            assert app.get_environment_variable('TEST_VAR') == 'test_value'
            assert app.get_environment_variable('NONEXISTENT') is None 