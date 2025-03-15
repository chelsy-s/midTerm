"""
Tests for the history management module.

This file contains tests for the HistoryManager class and history commands,
ensuring proper functionality for:
1. Adding, retrieving, and deleting history entries
2. Saving and loading history to/from CSV files
3. Searching and filtering history
4. Generating history statistics
5. Command execution for history operations
"""
import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock, mock_open
from app.history import history_manager, HistoryManager
from app.history.commands import (
    HistoryCommand, SaveHistoryCommand, LoadHistoryCommand, 
    ClearHistoryCommand, DeleteHistoryEntryCommand,
    HistoryStatsCommand, SearchHistoryCommand
)

class TestHistoryManager:
    """Tests for the HistoryManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a fresh history manager for each test
        self.history = HistoryManager(default_file_path="test_history.csv")
        
    def teardown_method(self):
        """Clean up after tests."""
        # Remove test file if it exists
        if os.path.exists("test_history.csv"):
            os.remove("test_history.csv")
    
    def test_init(self):
        """Test initialization of HistoryManager."""
        assert isinstance(self.history.history_df, pd.DataFrame)
        assert list(self.history.history_df.columns) == ['timestamp', 'operation', 'inputs', 'result']
        assert len(self.history.history_df) == 0
        
    def test_add_entry(self):
        """Test adding entries to history."""
        # Add an entry
        idx = self.history.add_entry("add", "5 10", "15.0")
        
        # Check the entry was added
        assert len(self.history.history_df) == 1
        assert idx == 0
        assert self.history.history_df.iloc[0]['operation'] == 'add'
        assert self.history.history_df.iloc[0]['inputs'] == '5 10'
        assert self.history.history_df.iloc[0]['result'] == '15.0'
        
        # Add another entry
        idx = self.history.add_entry("subtract", [20, 5], "15.0")
        
        # Check the second entry was added
        assert len(self.history.history_df) == 2
        assert idx == 1
        assert self.history.history_df.iloc[1]['operation'] == 'subtract'
        assert self.history.history_df.iloc[1]['inputs'] == '20 5'  # Should convert list to string
        
    def test_clear_history(self):
        """Test clearing history."""
        # Add a few entries
        self.history.add_entry("add", "5 10", "15.0")
        self.history.add_entry("subtract", "20 5", "15.0")
        
        # Verify entries were added
        assert len(self.history.history_df) == 2
        
        # Clear history
        result = self.history.clear_history()
        
        # Check the history was cleared
        assert result is True
        assert len(self.history.history_df) == 0
        
    def test_get_all_history(self):
        """Test getting all history entries."""
        # Add a few entries
        self.history.add_entry("add", "5 10", "15.0")
        self.history.add_entry("subtract", "20 5", "15.0")
        
        # Get all history
        history_df = self.history.get_all_history()
        
        # Check the returned DataFrame
        assert isinstance(history_df, pd.DataFrame)
        assert len(history_df) == 2
        assert list(history_df.columns) == ['timestamp', 'operation', 'inputs', 'result']
        
    def test_get_entry(self):
        """Test getting a specific history entry."""
        # Add a few entries
        self.history.add_entry("add", "5 10", "15.0")
        self.history.add_entry("subtract", "20 5", "15.0")
        
        # Get entry at index 1
        entry = self.history.get_entry(1)
        
        # Check the entry
        assert isinstance(entry, dict)
        assert entry['operation'] == 'subtract'
        assert entry['inputs'] == '20 5'
        assert entry['result'] == '15.0'
        
        # Try to get non-existent entry
        entry = self.history.get_entry(2)
        assert entry is None
        
    def test_get_last_entry(self):
        """Test getting the most recent history entry."""
        # Empty history
        entry = self.history.get_last_entry()
        assert entry is None
        
        # Add entries
        self.history.add_entry("add", "5 10", "15.0")
        self.history.add_entry("subtract", "20 5", "15.0")
        self.history.add_entry("multiply", "3 4", "12.0")
        
        # Get last entry
        entry = self.history.get_last_entry()
        
        # Check it's the most recent one
        assert entry['operation'] == 'multiply'
        assert entry['inputs'] == '3 4'
        assert entry['result'] == '12.0'
        
    @patch('pandas.DataFrame.to_csv')
    def test_save_history(self, mock_to_csv):
        """Test saving history to a CSV file."""
        # Add entries
        self.history.add_entry("add", "5 10", "15.0")
        
        # Save to default path
        result = self.history.save_history()
        assert result is True
        mock_to_csv.assert_called_once_with(self.history.default_file_path, index=False)
        
        # Save to custom path
        mock_to_csv.reset_mock()
        result = self.history.save_history("custom_path.csv")
        assert result is True
        mock_to_csv.assert_called_once_with("custom_path.csv", index=False)
        
        # Test saving when there's an error
        mock_to_csv.side_effect = Exception("Test error")
        result = self.history.save_history()
        assert result is False
        
    @patch('pandas.read_csv')
    @patch('os.path.exists')
    def test_load_history(self, mock_exists, mock_read_csv):
        """Test loading history from a CSV file."""
        # Set up mocks
        mock_exists.return_value = True
        mock_df = pd.DataFrame({
            'timestamp': ['2023-01-01 12:00:00'],
            'operation': ['add'],
            'inputs': ['5 10'],
            'result': ['15.0']
        })
        mock_read_csv.return_value = mock_df
        
        # Load from default path
        result = self.history.load_history()
        assert result is True
        mock_read_csv.assert_called_once_with(self.history.default_file_path)
        assert len(self.history.history_df) == 1
        
        # File doesn't exist
        mock_exists.return_value = False
        mock_read_csv.reset_mock()
        result = self.history.load_history("nonexistent.csv")
        assert result is False
        mock_read_csv.assert_not_called()
        
        # Error during loading
        mock_exists.return_value = True
        mock_read_csv.side_effect = Exception("Test error")
        result = self.history.load_history()
        assert result is False
        
    def test_delete_entry(self):
        """Test deleting a specific history entry."""
        # Add entries
        self.history.add_entry("add", "5 10", "15.0")
        self.history.add_entry("subtract", "20 5", "15.0")
        self.history.add_entry("multiply", "3 4", "12.0")
        
        # Delete middle entry
        result = self.history.delete_entry(1)
        assert result is True
        assert len(self.history.history_df) == 2
        
        # Check the remaining entries
        assert self.history.history_df.iloc[0]['operation'] == 'add'
        assert self.history.history_df.iloc[1]['operation'] == 'multiply'
        
        # Try to delete non-existent entry
        result = self.history.delete_entry(5)
        assert result is False
        assert len(self.history.history_df) == 2
        
    def test_filter_by_operation(self):
        """Test filtering history by operation type."""
        # Add entries with different operations
        self.history.add_entry("add", "5 10", "15.0")
        self.history.add_entry("add", "1 2", "3.0")
        self.history.add_entry("subtract", "20 5", "15.0")
        self.history.add_entry("multiply", "3 4", "12.0")
        
        # Filter by 'add' operation
        filtered = self.history.filter_by_operation("add")
        assert len(filtered) == 2
        assert all(filtered['operation'] == 'add')
        
        # Filter by operation with no matches
        filtered = self.history.filter_by_operation("nonexistent")
        assert len(filtered) == 0
        
    def test_search_history(self):
        """Test searching history for specific terms."""
        # Add varied entries
        self.history.add_entry("add", "5 10", "15.0")
        self.history.add_entry("add", "1 2", "3.0")
        self.history.add_entry("subtract", "20 5", "15.0")
        self.history.add_entry("multiply", "3 4", "12.0")
        
        # Search by operation
        results = self.history.search_history("add")
        assert len(results) == 2
        
        # Search by input
        results = self.history.search_history("5")
        assert len(results) == 2  # Should match "5 10" and "20 5"
        
        # Search by result
        results = self.history.search_history("15")
        assert len(results) == 2
        
        # Search with no matches
        results = self.history.search_history("xyz")
        assert len(results) == 0
        
    def test_get_stats(self):
        """Test generating statistics about the calculation history."""
        # Empty history
        stats = self.history.get_stats()
        assert stats["total_entries"] == 0
        assert stats["operations"] == {}
        
        # Add entries
        self.history.add_entry("add", "5 10", "15.0")
        self.history.add_entry("add", "1 2", "3.0")
        self.history.add_entry("subtract", "20 5", "15.0")
        self.history.add_entry("multiply", "3 4", "12.0")
        
        # Get stats
        stats = self.history.get_stats()
        
        # Check stats content
        assert stats["total_entries"] == 4
        assert stats["operations"]["add"] == 2
        assert stats["operations"]["subtract"] == 1
        assert stats["operations"]["multiply"] == 1
        assert "first_entry_time" in stats
        assert "last_entry_time" in stats

class TestHistoryCommands:
    """Tests for the history command classes."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a fresh history manager with some test data
        self.original_manager = history_manager
        
        # Add some entries to the manager for testing
        history_manager.clear_history()
        history_manager.add_entry("add", "5 10", "15.0")
        history_manager.add_entry("subtract", "20 5", "15.0")
        
    def teardown_method(self):
        """Clean up after tests."""
        # Restore original history manager
        history_manager.clear_history()
    
    def test_history_command(self):
        """Test the history command."""
        cmd = HistoryCommand()
        
        # Execute with no args (should show all entries)
        result = cmd.execute()
        assert "=== Calculation History ===" in result
        assert "add 5 10 = 15.0" in result
        assert "subtract 20 5 = 15.0" in result
        
        # Execute with limit
        result = cmd.execute("1")
        assert "subtract 20 5 = 15.0" in result  # Should show only the last entry
        assert "add 5 10 = 15.0" not in result
        assert "Showing 1 of 2 entries" in result
        
        # Execute with invalid limit
        result = cmd.execute("invalid")
        assert "Invalid argument" in result
        
        # Execute with empty history
        history_manager.clear_history()
        result = cmd.execute()
        assert "No calculation history available" in result
        
    def test_save_history_command(self):
        """Test the save history command."""
        cmd = SaveHistoryCommand()
        
        # Execute with no args (should use default path)
        with patch.object(history_manager, 'save_history', return_value=True) as mock_save:
            result = cmd.execute()
            assert "History saved to" in result
            mock_save.assert_called_once_with(None)
            
        # Execute with custom path
        with patch.object(history_manager, 'save_history', return_value=True) as mock_save:
            result = cmd.execute("custom_path")
            assert "History saved to custom_path.csv" in result
            mock_save.assert_called_once_with("custom_path.csv")
            
        # Execute with save error
        with patch.object(history_manager, 'save_history', return_value=False) as mock_save:
            result = cmd.execute()
            assert "Error saving history" in result
            
        # Execute with empty history
        history_manager.clear_history()
        result = cmd.execute()
        assert "No history to save" in result
        
    def test_load_history_command(self):
        """Test the load history command."""
        cmd = LoadHistoryCommand()
        
        # Execute with no args (should use default path)
        with patch.object(history_manager, 'load_history', return_value=True) as mock_load:
            with patch('os.path.exists', return_value=True):
                result = cmd.execute()
                assert "Loaded" in result
                mock_load.assert_called_once_with(None)
            
        # Execute with custom path
        with patch.object(history_manager, 'load_history', return_value=True) as mock_load:
            with patch('os.path.exists', return_value=True):
                result = cmd.execute("custom_path")
                assert "Loaded" in result
                mock_load.assert_called_once_with("custom_path.csv")
            
        # Execute with file not found
        with patch('os.path.exists', return_value=False):
            result = cmd.execute("nonexistent")
            assert "File not found" in result
            
        # Execute with load error
        with patch.object(history_manager, 'load_history', return_value=False) as mock_load:
            with patch('os.path.exists', return_value=True):
                result = cmd.execute()
                assert "Error loading history" in result
        
    def test_clear_history_command(self):
        """Test the clear history command."""
        cmd = ClearHistoryCommand()
        
        # Execute (should clear history)
        result = cmd.execute()
        assert "History cleared" in result
        assert len(history_manager.get_all_history()) == 0
        
        # Execute with already empty history
        result = cmd.execute()
        assert "History is already empty" in result
        
    def test_delete_history_entry_command(self):
        """Test the delete history entry command."""
        cmd = DeleteHistoryEntryCommand()
        
        # Re-add entries for testing
        history_manager.clear_history()
        history_manager.add_entry("add", "5 10", "15.0")
        history_manager.add_entry("subtract", "20 5", "15.0")
        
        # Execute without index
        result = cmd.execute()
        assert "Please specify an entry index" in result
        
        # Execute with invalid index
        result = cmd.execute("invalid")
        assert "Invalid index" in result
        
        # Execute with valid index
        result = cmd.execute("0")
        assert "Deleted history entry" in result
        assert len(history_manager.get_all_history()) == 1
        
        # Execute with non-existent index
        result = cmd.execute("5")
        assert "Entry 5 not found" in result
        
    def test_history_stats_command(self):
        """Test the history stats command."""
        cmd = HistoryStatsCommand()
        
        # Execute with history
        result = cmd.execute()
        assert "=== History Statistics ===" in result
        assert "Total entries: 2" in result
        assert "add: 1" in result
        assert "subtract: 1" in result
        
        # Execute with empty history
        history_manager.clear_history()
        result = cmd.execute()
        assert "No history entries available" in result
        
    def test_search_history_command(self):
        """Test the search history command."""
        cmd = SearchHistoryCommand()
        
        # Execute without search term
        result = cmd.execute()
        assert "Please provide a search term" in result
        
        # Execute with term that has matches
        result = cmd.execute("add")
        assert "=== Search Results for 'add' ===" in result
        assert "add 5 10 = 15.0" in result
        assert "Found 1 matching entries" in result
        
        # Execute with term that has no matches
        result = cmd.execute("nonexistent")
        assert "No history entries found matching" in result
        
        # Execute with multiple word search term
        result = cmd.execute("5", "10")
        assert "=== Search Results for '5 10' ===" in result
        assert "add 5 10 = 15.0" in result 