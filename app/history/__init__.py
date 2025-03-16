"""
Calculation history management module for the calculator application.

This module implements the HistoryManager class that provides a robust solution for:
1. Tracking calculator operations with timestamps, inputs, and results
2. Persisting calculation history to CSV files for long-term storage
3. Loading previous calculation sessions from CSV files
4. Querying history with filtering and search capabilities
5. Generating statistics on calculation patterns

The implementation demonstrates the Facade design pattern by providing a clean,
unified interface that encapsulates the complexity of the underlying pandas
DataFrame operations. This promotes loose coupling between the calculator core
and its history management functionality.
"""
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union, Any, Tuple
import pandas as pd

class HistoryManager:
    """
    Manages calculator operation history using pandas DataFrame.

    This class implements the Facade pattern by providing a simplified interface
    to complex pandas data manipulation operations. It encapsulates the details
    of data storage, retrieval, and querying behind intuitive methods that
    other parts of the application can easily use.

    The implementation prioritizes:
    - Data integrity through consistent validation
    - Performance through appropriate pandas optimizations
    - Robustness through comprehensive error handling
    - Maintainability through clear organization and documentation

    Attributes:
        history_df (pd.DataFrame): DataFrame storing operation history with columns:
            - timestamp: When the operation was performed
            - operation: The type of operation (add, subtract, etc.)
            - inputs: The inputs to the operation
            - result: The result of the operation
        default_file_path (str): Default path for saving/loading history CSV files
    """

    # Define column names as constants for consistency and maintainability
    TIMESTAMP_COL = 'timestamp'
    OPERATION_COL = 'operation'
    INPUTS_COL = 'inputs'
    RESULT_COL = 'result'

    # Define the schema as a class attribute for reuse
    SCHEMA = [TIMESTAMP_COL, OPERATION_COL, INPUTS_COL, RESULT_COL]

    def __init__(self, default_file_path: str = "data/history.csv"):
        """
        Initialize the history manager with an empty history DataFrame.

        Args:
            default_file_path: Default path for saving/loading history
        """
        self.logger = logging.getLogger(__name__)

        # Initialize empty DataFrame with predefined schema
        self.history_df = pd.DataFrame(columns=self.SCHEMA)

        # Store the default file path
        self.default_file_path = default_file_path

        # Ensure the data directory exists to prevent future I/O errors
        self._ensure_directory_exists(default_file_path)

        self.logger.info("History manager initialized with default path: %s", default_file_path)

    def add_entry(self, operation: str, inputs: Union[str, List], result: str) -> int:
        """
        Add a new entry to the calculation history.

        This method records a calculation with its operation type, inputs,
        and result, along with a timestamp for chronological tracking.
        It handles both string and list inputs for flexibility.

        Args:
            operation: The operation performed (e.g., 'add', 'subtract')
            inputs: The inputs to the operation (as a string or list)
            result: The result of the operation

        Returns:
            int: The index of the new entry in the history DataFrame
        """
        # Convert inputs to string if they're a list
        if isinstance(inputs, list):
            inputs = ' '.join(map(str, inputs))

        # Get current timestamp in consistent format
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create a new entry as a single-row DataFrame for efficient appending
        new_entry = pd.DataFrame([{
            self.TIMESTAMP_COL: timestamp,
            self.OPERATION_COL: operation,
            self.INPUTS_COL: inputs,
            self.RESULT_COL: result
        }])

        # Append to the history DataFrame using concat for better performance
        # than .append() method which is deprecated in newer pandas versions
        self.history_df = pd.concat([self.history_df, new_entry], ignore_index=True)

        # Get the index of the newly added entry
        new_index = len(self.history_df) - 1

        self.logger.info(f"Added history entry {new_index}: {operation} {inputs} = {result}")
        return new_index

    def clear_history(self) -> bool:
        """
        Clear all entries from the history.

        This method resets the history to an empty DataFrame while preserving
        the schema, effectively removing all calculation records.

        Returns:
            bool: True if history was cleared successfully
        """
        # Reset to a new empty DataFrame with the same schema
        self.history_df = pd.DataFrame(columns=self.SCHEMA)
        self.logger.info("History cleared - all entries removed")
        return True

    def get_all_history(self) -> pd.DataFrame:
        """
        Get all history entries.

        Returns a copy of the history DataFrame to prevent accidental
        modifications to the internal data structure.

        Returns:
            pd.DataFrame: Copy of all history entries
        """
        return self.history_df.copy()

    def get_entry(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific history entry by index.

        Retrieves a single history entry by its index position, with bounds
        checking to prevent index errors.

        Args:
            index: Index of the entry to retrieve (zero-based)

        Returns:
            dict: The history entry as a dictionary, or None if not found
        """
        # Check if index is valid using LBYL approach
        if 0 <= index < len(self.history_df):
            entry = self.history_df.iloc[index].to_dict()
            return entry

        self.logger.warning(f"History entry {index} not found (valid range: 0-{len(self.history_df)-1 if len(self.history_df) > 0 else 0})")
        return None

    def get_last_entry(self) -> Optional[Dict[str, Any]]:
        """
        Get the most recent history entry.

        A convenience method that returns the last entry added to the
        history, which is useful for retrieving the result of the most
        recent calculation.

        Returns:
            dict: The most recent history entry as a dictionary, or None if history is empty
        """
        # Check if history is empty using LBYL approach
        if len(self.history_df) > 0:
            entry = self.history_df.iloc[-1].to_dict()
            return entry

        self.logger.warning("No history entries found - history is empty")
        return None

    def save_history(self, file_path: Optional[str] = None) -> bool:
        """
        Save the history to a CSV file.

        This method persists the calculation history to a CSV file for
        later retrieval. It demonstrates the EAFP approach to error handling
        by attempting the operation and handling exceptions if they occur.

        Args:
            file_path: Path to save the history to (uses default_file_path if None)

        Returns:
            bool: True if history was saved successfully, False otherwise
        """
        # Use default path if none provided
        if file_path is None:
            file_path = self.default_file_path

        try:
            # Ensure the directory exists by calling os.makedirs directly
            # This maintains compatibility with test mocks
            directory = os.path.dirname(file_path)
            if directory:  # Only create if there's actually a directory part
                os.makedirs(directory, exist_ok=True)

            # Save the DataFrame to CSV
            self.history_df.to_csv(file_path, index=False)
            self.logger.info(f"History saved to {file_path} ({len(self.history_df)} entries)")
            return True
        except PermissionError as e:
            self.logger.error(f"Permission denied when saving history to {file_path}: {str(e)}")
            return False
        except OSError as e:
            self.logger.error(f"OS error when saving history to {file_path}: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error saving history to {file_path}: {str(e)}", exc_info=True)
            return False

    def load_history(self, file_path: Optional[str] = None) -> bool:
        """
        Load history from a CSV file.

        This method retrieves previously saved calculation history from a
        CSV file. It demonstrates the EAFP approach to error handling and
        provides detailed error messages for troubleshooting.

        Args:
            file_path: Path to load the history from (uses default_file_path if None)

        Returns:
            bool: True if history was loaded successfully, False otherwise
        """
        # Use default path if none provided
        if file_path is None:
            file_path = self.default_file_path

        # EAFP approach for file operations
        try:
            if os.path.exists(file_path):
                # Load the DataFrame from CSV
                loaded_df = pd.read_csv(file_path)

                # Validate the loaded DataFrame schema
                if set(self.SCHEMA).issubset(set(loaded_df.columns)):
                    self.history_df = loaded_df
                    self.logger.info(f"History loaded from {file_path} ({len(self.history_df)} entries)")
                    return True
                else:
                    self.logger.error(f"Invalid schema in history file {file_path}")
                    return False
            else:
                self.logger.warning(f"History file {file_path} not found")
                return False
        except pd.errors.EmptyDataError:
            # Handle empty file
            self.logger.warning(f"History file {file_path} is empty")
            self.history_df = pd.DataFrame(columns=self.SCHEMA)
            return True
        except pd.errors.ParserError as e:
            self.logger.error(f"Error parsing history file {file_path}: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error loading history from {file_path}: {str(e)}", exc_info=True)
            return False

    def delete_entry(self, index: int) -> bool:
        """
        Delete a specific history entry by index.

        Removes a single entry from the history by its index position,
        with bounds checking to prevent index errors.

        Args:
            index: Index of the entry to delete (zero-based)

        Returns:
            bool: True if entry was deleted successfully, False otherwise
        """
        # LBYL approach for index validation
        if 0 <= index < len(self.history_df):
            # Store entry details for logging
            entry = self.history_df.iloc[index]

            # Drop the row at the specified index and reset index to maintain continuity
            self.history_df = self.history_df.drop(index).reset_index(drop=True)

            self.logger.info(f"Deleted history entry at index {index}: {entry[self.OPERATION_COL]} {entry[self.INPUTS_COL]} = {entry[self.RESULT_COL]}")
            return True
        else:
            self.logger.warning(f"Cannot delete: History entry {index} not found (valid range: 0-{len(self.history_df)-1 if len(self.history_df) > 0 else 0})")
            return False

    def filter_by_operation(self, operation: str) -> pd.DataFrame:
        """
        Filter history entries by operation type.

        This method leverages pandas' efficient filtering capabilities to
        retrieve all entries matching a specific operation type.

        Args:
            operation: Operation name to filter by (e.g., 'add', 'subtract')

        Returns:
            pd.DataFrame: Filtered history entries (may be empty if no matches)
        """
        # Use pandas boolean indexing for efficient filtering
        filtered = self.history_df[self.history_df[self.OPERATION_COL] == operation]

        self.logger.info(f"Filtered history by operation '{operation}': found {len(filtered)} entries")
        return filtered

    def search_history(self, search_term: str) -> pd.DataFrame:
        """
        Search history entries for a specific term across all fields.

        This method performs a case-insensitive search across all columns
        in the history to find entries containing the specified term.

        Args:
            search_term: Term to search for

        Returns:
            pd.DataFrame: Matching history entries (may be empty if no matches)
        """
        # Convert search term to string for comparison
        search_term = str(search_term)

        # Search across all columns using efficient pandas vectorized operations
        result = self.history_df[
            self.history_df.astype(str).apply(
                lambda row: row.str.contains(search_term, case=False, na=False).any(),
                axis=1
            )
        ]

        self.logger.info(f"Searched history for '{search_term}': found {len(result)} entries")
        return result

    def get_stats(self) -> Dict[str, Any]:
        """
        Generate statistics from the calculation history.

        This method analyzes the history data to provide insights such as:
        - Most used operations
        - Total number of calculations
        - Distribution of operation types
        - Time period covered by the history

        Returns:
            dict: Dictionary of statistics about the calculation history
        """
        stats = {
            'total_entries': len(self.history_df),
            'unique_operations': 0,
            'operation_counts': {},
            'time_period': {'first': None, 'last': None},
        }

        # Return empty stats if history is empty
        if len(self.history_df) == 0:
            # For backward compatibility with tests
            stats['operations'] = {}
            stats['first_entry_time'] = None
            stats['last_entry_time'] = None
            return stats

        # Count occurrences of each operation type
        operation_counts = self.history_df[self.OPERATION_COL].value_counts().to_dict()
        stats['operation_counts'] = operation_counts
        # For backward compatibility with tests
        stats['operations'] = operation_counts
        stats['unique_operations'] = len(operation_counts)

        # Get time period if timestamps are available
        if len(self.history_df) > 0:
            # Sort by timestamp to find first and last entry
            sorted_by_time = self.history_df.sort_values(by=self.TIMESTAMP_COL)
            first_timestamp = sorted_by_time.iloc[0][self.TIMESTAMP_COL]
            last_timestamp = sorted_by_time.iloc[-1][self.TIMESTAMP_COL]

            stats['time_period']['first'] = first_timestamp
            stats['time_period']['last'] = last_timestamp

            # For backward compatibility with tests
            stats['first_entry_time'] = first_timestamp
            stats['last_entry_time'] = last_timestamp

        self.logger.info(f"Generated history statistics: {stats['total_entries']} entries, {stats['unique_operations']} unique operations")
        return stats

    def _ensure_directory_exists(self, file_path: str) -> None:
        """
        Ensure the directory for a file path exists, creating it if needed.

        This private helper method centralizes directory creation logic
        to avoid redundancy and ensure consistent error handling.

        Args:
            file_path: Path to a file for which the directory should exist
        """
        directory = os.path.dirname(file_path)
        if directory:  # Only create if there's actually a directory part
            os.makedirs(directory, exist_ok=True)

# Create a singleton instance for the application to use
history_manager = HistoryManager()