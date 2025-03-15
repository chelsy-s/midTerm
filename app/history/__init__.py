"""
Calculation history management module for the calculator application.

This module implements a HistoryManager class using the Pandas library to:
1. Track calculator operations and their results
2. Save history to CSV files
3. Load history from CSV files
4. Provide query and filtering capabilities
5. Maintain a calculation history log

It demonstrates the Facade pattern by providing a simplified interface
to complex Pandas operations.
"""
import os
import logging
from datetime import datetime
import pandas as pd

class HistoryManager:
    """
    Manages calculator operation history using Pandas.
    
    This class implements the Facade pattern by providing a simplified interface
    to complex Pandas data operations. It handles the creation, storage, retrieval,
    and management of calculation history records.
    
    Attributes:
        history_df (pd.DataFrame): DataFrame storing operation history
        default_file_path (str): Default path for saving/loading history CSV files
    """
    
    def __init__(self, default_file_path="data/history.csv"):
        """
        Initialize the history manager with an empty history.
        
        Args:
            default_file_path: Default path for saving/loading history
        """
        self.logger = logging.getLogger(__name__)
        self.history_df = pd.DataFrame(columns=[
            'timestamp', 
            'operation', 
            'inputs', 
            'result'
        ])
        self.default_file_path = default_file_path
        
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(default_file_path), exist_ok=True)
        
        self.logger.info("History manager initialized")
        
    def add_entry(self, operation, inputs, result):
        """
        Add a new entry to the calculation history.
        
        Args:
            operation: The operation performed (e.g., 'add', 'subtract')
            inputs: The inputs to the operation (as a string or list)
            result: The result of the operation
            
        Returns:
            int: The index of the new entry
        """
        # Convert inputs to string if they're not already
        if isinstance(inputs, list):
            inputs = ' '.join(map(str, inputs))
            
        # Create a new entry as a DataFrame
        new_entry = pd.DataFrame([{
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operation': operation,
            'inputs': inputs,
            'result': result
        }])
        
        # Append to the history DataFrame
        self.history_df = pd.concat([self.history_df, new_entry], ignore_index=True)
        
        self.logger.info(f"Added history entry: {operation} {inputs} = {result}")
        return len(self.history_df) - 1
        
    def clear_history(self):
        """
        Clear all entries from the history.
        
        Returns:
            bool: True if history was cleared successfully
        """
        self.history_df = pd.DataFrame(columns=[
            'timestamp', 
            'operation', 
            'inputs', 
            'result'
        ])
        self.logger.info("History cleared")
        return True
        
    def get_all_history(self):
        """
        Get all history entries.
        
        Returns:
            pd.DataFrame: All history entries
        """
        return self.history_df
        
    def get_entry(self, index):
        """
        Get a specific history entry by index.
        
        Args:
            index: Index of the entry to retrieve
            
        Returns:
            dict: The history entry or None if not found
        """
        if 0 <= index < len(self.history_df):
            entry = self.history_df.iloc[index].to_dict()
            return entry
        self.logger.warning(f"History entry {index} not found")
        return None
        
    def get_last_entry(self):
        """
        Get the most recent history entry.
        
        Returns:
            dict: The most recent history entry or None if history is empty
        """
        if len(self.history_df) > 0:
            entry = self.history_df.iloc[-1].to_dict()
            return entry
        self.logger.warning("No history entries found")
        return None
        
    def save_history(self, file_path=None):
        """
        Save the history to a CSV file.
        
        This method demonstrates using Pandas to write data to CSV files,
        with error handling using the EAFP approach.
        
        Args:
            file_path: Path to save the history to (uses default_file_path if None)
            
        Returns:
            bool: True if history was saved successfully, False otherwise
        """
        if file_path is None:
            file_path = self.default_file_path
            
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save the DataFrame to CSV
            self.history_df.to_csv(file_path, index=False)
            self.logger.info(f"History saved to {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving history to {file_path}: {str(e)}")
            return False
            
    def load_history(self, file_path=None):
        """
        Load history from a CSV file.
        
        This method demonstrates using Pandas to read data from CSV files,
        with error handling using the EAFP approach.
        
        Args:
            file_path: Path to load the history from (uses default_file_path if None)
            
        Returns:
            bool: True if history was loaded successfully, False otherwise
        """
        if file_path is None:
            file_path = self.default_file_path
            
        # EAFP approach for file operations
        try:
            if os.path.exists(file_path):
                self.history_df = pd.read_csv(file_path)
                self.logger.info(f"History loaded from {file_path}")
                return True
            else:
                self.logger.warning(f"History file {file_path} not found")
                return False
        except Exception as e:
            self.logger.error(f"Error loading history from {file_path}: {str(e)}")
            return False
            
    def delete_entry(self, index):
        """
        Delete a specific history entry by index.
        
        Args:
            index: Index of the entry to delete
            
        Returns:
            bool: True if entry was deleted successfully, False otherwise
        """
        # LBYL approach for index validation
        if 0 <= index < len(self.history_df):
            # Drop the row at the specified index
            self.history_df = self.history_df.drop(index).reset_index(drop=True)
            self.logger.info(f"Deleted history entry at index {index}")
            return True
        else:
            self.logger.warning(f"Cannot delete: History entry {index} not found")
            return False
            
    def filter_by_operation(self, operation):
        """
        Filter history entries by operation type.
        
        Args:
            operation: Operation name to filter by
            
        Returns:
            pd.DataFrame: Filtered history entries
        """
        filtered = self.history_df[self.history_df['operation'] == operation]
        self.logger.info(f"Filtered history by operation '{operation}': {len(filtered)} entries")
        return filtered
        
    def search_history(self, search_term):
        """
        Search history entries for a specific term across all fields.
        
        Args:
            search_term: Term to search for
            
        Returns:
            pd.DataFrame: Matching history entries
        """
        # Convert search term to string for comparison
        search_term = str(search_term)
        
        # Search across all columns using string representations
        result = self.history_df[
            self.history_df.astype(str).apply(
                lambda row: row.str.contains(search_term, case=False).any(), 
                axis=1
            )
        ]
        
        self.logger.info(f"Searched history for '{search_term}': {len(result)} entries found")
        return result
        
    def get_stats(self):
        """
        Get statistics about the calculation history.
        
        Returns:
            dict: Statistics including total entries, operations count, etc.
        """
        if len(self.history_df) == 0:
            return {"total_entries": 0, "operations": {}}
            
        # Count operations
        operation_counts = self.history_df['operation'].value_counts().to_dict()
        
        # Basic statistics
        stats = {
            "total_entries": len(self.history_df),
            "operations": operation_counts,
            "first_entry_time": self.history_df['timestamp'].min(),
            "last_entry_time": self.history_df['timestamp'].max()
        }
        
        self.logger.info(f"Generated history statistics: {len(self.history_df)} total entries")
        return stats

# Singleton instance for global access to history
history_manager = HistoryManager() 