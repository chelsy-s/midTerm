"""
Command implementations for calculator history management.

This module provides command classes that interact with the HistoryManager
to perform operations like:
1. Viewing history entries
2. Saving history to files
3. Loading history from files
4. Clearing history
5. Generating history statistics

These commands implement the Command pattern and can be registered
with the CommandHandler for use in the REPL interface.
"""
import logging
import os
from app.commands import Command
from app.history import history_manager

class HistoryCommand(Command):
    """
    Command to display calculation history.
    
    This command shows recent calculation history entries,
    with options to limit the number of entries shown.
    """
    
    def __init__(self):
        """Initialize the history command."""
        self.logger = logging.getLogger(__name__)
        
    def execute(self, *args, **kwargs):
        """
        Execute the history command to display recent calculation history.
        
        Args:
            *args: First arg can be a number to limit entries shown
            **kwargs: Not used by this command
            
        Returns:
            str: Formatted string containing the history entries
        """
        self.logger.info("Executing history command")
        
        # Get all history entries
        history_df = history_manager.get_all_history()
        
        # Check if history is empty
        if len(history_df) == 0:
            return "No calculation history available."
        
        # Determine how many entries to display
        limit = None
        if args and len(args) > 0:
            try:
                limit = int(args[0])
                if limit <= 0:
                    return "Number of entries must be positive."
            except ValueError:
                return f"Invalid argument: '{args[0]}' - must be a positive number."
        
        # Format the history entries for display
        history_text = ["\n=== Calculation History ==="]
        
        # Get the entries to display (all or limited)
        if limit:
            display_df = history_df.tail(limit)
        else:
            display_df = history_df
        
        # Format each entry
        for idx, row in display_df.iterrows():
            entry_text = f"{idx}: [{row['timestamp']}] {row['operation']} {row['inputs']} = {row['result']}"
            history_text.append(entry_text)
        
        # Add a footer with info
        history_text.append(f"\nShowing {len(display_df)} of {len(history_df)} entries.")
        history_text.append("Use 'history <number>' to limit entries shown.")
        history_text.append("Use 'history-save' to save history to a file.")
        
        self.logger.info(f"Displayed {len(display_df)} history entries")
        return "\n".join(history_text)

class SaveHistoryCommand(Command):
    """
    Command to save calculation history to a CSV file.
    
    This command saves the current calculation history to a file,
    either to the default location or to a specified path.
    """
    
    def __init__(self):
        """Initialize the save history command."""
        self.logger = logging.getLogger(__name__)
        
    def execute(self, *args, **kwargs):
        """
        Execute the command to save history to a file.
        
        Args:
            *args: Optional file path to save to
            **kwargs: Not used by this command
            
        Returns:
            str: Success or error message
        """
        self.logger.info("Executing save-history command")
        
        # Check if history is empty
        if len(history_manager.get_all_history()) == 0:
            return "No history to save."
        
        # Determine file path
        file_path = None
        if args and len(args) > 0:
            file_path = args[0]
            # Add .csv extension if not present
            if not file_path.endswith('.csv'):
                file_path += '.csv'
        
        # Save the history
        success = history_manager.save_history(file_path)
        
        if success:
            saved_path = file_path or history_manager.default_file_path
            return f"History saved to {saved_path}"
        else:
            return "Error saving history. See logs for details."

class LoadHistoryCommand(Command):
    """
    Command to load calculation history from a CSV file.
    
    This command loads calculation history from a file,
    either from the default location or from a specified path.
    """
    
    def __init__(self):
        """Initialize the load history command."""
        self.logger = logging.getLogger(__name__)
        
    def execute(self, *args, **kwargs):
        """
        Execute the command to load history from a file.
        
        Args:
            *args: Optional file path to load from
            **kwargs: Not used by this command
            
        Returns:
            str: Success or error message
        """
        self.logger.info("Executing load-history command")
        
        # Determine file path
        file_path = None
        if args and len(args) > 0:
            file_path = args[0]
            # Add .csv extension if not present
            if not file_path.endswith('.csv'):
                file_path += '.csv'
        
        # Check if file exists (using LBYL approach)
        if file_path and not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        # Load the history
        success = history_manager.load_history(file_path)
        
        if success:
            loaded_path = file_path or history_manager.default_file_path
            entry_count = len(history_manager.get_all_history())
            return f"Loaded {entry_count} history entries from {loaded_path}"
        else:
            return "Error loading history. See logs for details."

class ClearHistoryCommand(Command):
    """
    Command to clear the calculation history.
    
    This command removes all entries from the history.
    """
    
    def __init__(self):
        """Initialize the clear history command."""
        self.logger = logging.getLogger(__name__)
        
    def execute(self, *args, **kwargs):
        """
        Execute the command to clear the history.
        
        Args:
            *args: Not used by this command
            **kwargs: Not used by this command
            
        Returns:
            str: Success message
        """
        self.logger.info("Executing clear-history command")
        
        # Check if history is already empty
        if len(history_manager.get_all_history()) == 0:
            return "History is already empty."
        
        # Clear the history
        history_manager.clear_history()
        return "History cleared."

class DeleteHistoryEntryCommand(Command):
    """
    Command to delete a specific history entry.
    
    This command removes a single entry from the history by its index.
    """
    
    def __init__(self):
        """Initialize the delete history entry command."""
        self.logger = logging.getLogger(__name__)
        
    def execute(self, *args, **kwargs):
        """
        Execute the command to delete a history entry.
        
        Args:
            *args: Index of the entry to delete
            **kwargs: Not used by this command
            
        Returns:
            str: Success or error message
        """
        self.logger.info("Executing delete-history-entry command")
        
        # Check if an index was provided
        if not args or len(args) == 0:
            return "Error: Please specify an entry index to delete."
        
        # Parse the index
        try:
            index = int(args[0])
        except ValueError:
            return f"Error: Invalid index '{args[0]}'. Please provide a numeric index."
        
        # Delete the entry
        success = history_manager.delete_entry(index)
        
        if success:
            return f"Deleted history entry at index {index}."
        else:
            return f"Error: Entry {index} not found."

class HistoryStatsCommand(Command):
    """
    Command to display statistics about the calculation history.
    
    This command shows information like total entries, operation counts,
    and time span of the history.
    """
    
    def __init__(self):
        """Initialize the history stats command."""
        self.logger = logging.getLogger(__name__)
        
    def execute(self, *args, **kwargs):
        """
        Execute the command to display history statistics.
        
        Args:
            *args: Not used by this command
            **kwargs: Not used by this command
            
        Returns:
            str: Formatted string containing history statistics
        """
        self.logger.info("Executing history-stats command")
        
        # Get the statistics
        stats = history_manager.get_stats()
        
        # Check if history is empty
        if stats["total_entries"] == 0:
            return "No history entries available for statistics."
        
        # Format the statistics for display
        stats_text = ["\n=== History Statistics ==="]
        stats_text.append(f"Total entries: {stats['total_entries']}")
        
        # Add operation counts
        stats_text.append("\nOperation counts:")
        for op, count in stats["operations"].items():
            stats_text.append(f"  - {op}: {count}")
        
        # Add time information
        stats_text.append(f"\nFirst entry: {stats['first_entry_time']}")
        stats_text.append(f"Last entry: {stats['last_entry_time']}")
        
        self.logger.info("Displayed history statistics")
        return "\n".join(stats_text)

class SearchHistoryCommand(Command):
    """
    Command to search the calculation history.
    
    This command searches for entries matching a search term
    across all fields in the history.
    """
    
    def __init__(self):
        """Initialize the search history command."""
        self.logger = logging.getLogger(__name__)
        
    def execute(self, *args, **kwargs):
        """
        Execute the command to search history entries.
        
        Args:
            *args: Search term to look for
            **kwargs: Not used by this command
            
        Returns:
            str: Formatted string containing search results
        """
        self.logger.info("Executing search-history command")
        
        # Check if a search term was provided
        if not args or len(args) == 0:
            return "Error: Please provide a search term."
        
        # Join all args to form the search term
        search_term = " ".join(args)
        
        # Perform the search
        results = history_manager.search_history(search_term)
        
        # Format the results
        if len(results) == 0:
            return f"No history entries found matching '{search_term}'."
        
        # Format each matching entry
        result_text = [f"\n=== Search Results for '{search_term}' ==="]
        
        for idx, row in results.iterrows():
            entry_text = f"{idx}: [{row['timestamp']}] {row['operation']} {row['inputs']} = {row['result']}"
            result_text.append(entry_text)
        
        result_text.append(f"\nFound {len(results)} matching entries.")
        
        self.logger.info(f"Found {len(results)} entries matching '{search_term}'")
        return "\n".join(result_text)

def register_history_commands(command_handler):
    """
    Register history management commands with the command handler.
    
    This function creates instances of history command classes
    and registers them with the provided command handler.
    
    Args:
        command_handler: CommandHandler to register commands with
    """
    # Create command instances
    history_cmd = HistoryCommand()
    save_history_cmd = SaveHistoryCommand()
    load_history_cmd = LoadHistoryCommand()
    clear_history_cmd = ClearHistoryCommand()
    delete_entry_cmd = DeleteHistoryEntryCommand()
    stats_cmd = HistoryStatsCommand()
    search_cmd = SearchHistoryCommand()
    
    # Register primary commands with hyphens
    command_handler.register_command("history", history_cmd)
    command_handler.register_command("history-save", save_history_cmd)
    command_handler.register_command("history-load", load_history_cmd)
    command_handler.register_command("history-clear", clear_history_cmd)
    command_handler.register_command("history-delete", delete_entry_cmd)
    command_handler.register_command("history-stats", stats_cmd)
    command_handler.register_command("history-search", search_cmd)
    
    # Register aliases with spaces instead of hyphens
    command_handler.register_command("historysave", save_history_cmd)
    command_handler.register_command("historyload", load_history_cmd)
    command_handler.register_command("historyclear", clear_history_cmd)
    command_handler.register_command("historydelete", delete_entry_cmd)
    command_handler.register_command("historystats", stats_cmd)
    command_handler.register_command("historysearch", search_cmd)
    
    logging.info("History commands registered") 