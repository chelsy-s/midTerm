"""
Advanced Python Calculator Application Module.

This module contains the core App class that serves as the main entry point
for the calculator application. It handles initialization, configuration,
plugin loading, and command execution through a REPL interface.

The application demonstrates professional software development practices including:
- Design Patterns (Command, Factory Method)
- Comprehensive logging
- Environment variable configuration
- Plugin architecture
- Error handling strategies (LBYL and EAFP)
"""
import os
import sys
import pkgutil
import importlib
import logging
import logging.config
import re
from dotenv import load_dotenv
import inspect
from abc import ABC

from app.commands import CommandHandler, Command
from app.history import history_manager  # Import the history manager

class App:
    """
    Main application class for the calculator.
    
    This class handles initialization, configuration, and command execution 
    through a Read-Eval-Print Loop (REPL) interface. It implements a plugin
    system that dynamically loads commands and operations at runtime.
    
    The class demonstrates several design patterns:
    - Command Pattern: Through the CommandHandler and Command interfaces
    - Factory Method: For creating operation instances
    - Plugin System: For dynamic loading of functionality
    """
    def __init__(self):
        """
        Initialize the calculator application.
        
        This constructor:
        1. Creates necessary directories
        2. Configures logging
        3. Loads environment variables
        4. Initializes the command handler
        """
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Configure logging
        self.configure_logging()
        
        # Load environment variables - using the imported function to ensure it can be mocked in tests
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        
        # Initialize command handler
        self.command_handler = CommandHandler()
        
        # Log application initialization
        logging.info("Calculator application initialized")

    def configure_logging(self):
        """
        Configure the logging system based on logging.conf.
        
        This method demonstrates:
        1. Configuration file-based setup
        2. Dynamic log level adjustment via environment variables
        3. Fallback to basic configuration if file is missing
        """
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Dynamic log level based on environment variable if set
        env_log_level = os.environ.get('LOG_LEVEL')
        if env_log_level:
            numeric_level = getattr(logging, env_log_level.upper(), None)
            if isinstance(numeric_level, int):
                logging.getLogger().setLevel(numeric_level)
        
        logging.info("Logging configured")

    def load_environment_variables(self):
        """
        Load environment variables into settings dictionary.
        
        This method demonstrates environment variable configuration
        for application settings.
        
        Returns:
            dict: Dictionary containing environment variables
        """
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        """
        Get the value of an environment variable.
        
        Args:
            env_var: Name of the environment variable to get
            
        Returns:
            Value of the environment variable or None if not found
        """
        return self.settings.get(env_var, None)

    def load_plugins(self):
        """
        Dynamically load plugins from the app/plugins directory.
        
        This method implements a plugin system that enables extending
        the application without modifying core code - a key principle
        of the Open/Closed SOLID principle.
        """
        plugins_package = 'app.plugins'
        plugins_path = os.path.dirname(__file__) + '/plugins'
        
        if not os.path.exists(plugins_path):
            logging.warning(f"Plugins directory '{plugins_path}' not found")
            return
        
        # Load all plugin packages (menu, operations, etc.)
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.register_plugin_commands(plugin_module, plugin_name)
                    
                    # For plugins with subpackages (like operations), load those too
                    plugin_dir = os.path.join(plugins_path, plugin_name)
                    for _, subplugin_name, subplugin_is_pkg in pkgutil.iter_modules([plugin_dir]):
                        if subplugin_is_pkg:
                            try:
                                # Import the subplugin module
                                subplugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}.{subplugin_name}')
                                logging.info(f"Loaded subplugin: {plugin_name}.{subplugin_name}")
                            except ImportError as e:
                                logging.error(f"Error importing subplugin {plugin_name}.{subplugin_name}: {str(e)}")
                except ImportError as e:
                    logging.error(f"Error importing plugin {plugin_name}: {str(e)}")
        
        # Register operation commands
        try:
            from app.plugins.operations.command_mapper import register_operation_commands
            register_operation_commands(self.command_handler)
        except ImportError as e:
            logging.error(f"Error importing operation command mapper: {str(e)}")
        
        # Register history commands
        try:
            from app.history.commands import register_history_commands
            register_history_commands(self.command_handler)
            logging.info("History commands registered")
        except ImportError as e:
            logging.error(f"Error importing history commands: {str(e)}")
        
        # Register utility commands
        try:
            from app.utils import register_utility_commands
            register_utility_commands(self.command_handler)
            logging.info("Utility commands registered")
        except ImportError as e:
            logging.error(f"Error importing utility commands: {str(e)}")
        
        # Register built-in commands
        self.register_help_command()
        self.register_expression_handler()

    def register_plugin_commands(self, plugin_module, plugin_name):
        """
        Register commands from a plugin module.
        
        This method reflects on the module to find Command subclasses
        and registers them with the command handler.
        
        Args:
            plugin_module: The imported plugin module
            plugin_name: Name of the plugin
        """
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            # Check if it's a class, a subclass of Command, not an abstract class,
            # and not the Command class itself
            if (isinstance(item, type) 
                and issubclass(item, Command) 
                and item is not Command 
                and not inspect.isabstract(item)):
                command_instance = item()
                self.command_handler.register_command(plugin_name, command_instance)
                logging.info(f"Command '{plugin_name}' from plugin '{plugin_name}' registered")
                
    def register_help_command(self):
        """
        Register a built-in help command.
        
        This method creates and registers a command that provides
        help information to the user about available commands.
        """
        class HelpCommand(Command):
            """Command that displays help information about calculator usage."""
            def __init__(self, app):
                self.app = app
                self.logger = logging.getLogger(__name__)
                
            def execute(self, *args, **kwargs):
                """Display comprehensive help information about available commands."""
                self.logger.info("Executing help command")
                help_text = """
======= CALCULATOR COMMANDS =======

Basic Operations:
  add [number1] [number2] ...     - Add numbers together
  subtract [number1] [number2] ... - Subtract subsequent numbers from the first
  multiply [number1] [number2] ... - Multiply numbers together
  divide [number1] [number2] ...   - Divide the first number by subsequent numbers

Calculator Interface:
  help                           - Show this help message
  menu                           - Show available calculator operations
  clear                          - Clear the screen
  cls                            - Clear the screen (alias)
  exit                           - Exit the calculator

Mathematical Expressions:
  You can also enter expressions directly, like: 2+3*4

History Management:
  history [limit]                - Show calculation history (optional: limit entries)
  history-save [filepath]        - Save history to CSV file (default: data/history.csv)
                                   (Can also use "history save")
  history-load [filepath]        - Load history from CSV file
                                   (Can also use "history load")
  history-clear                  - Clear all history entries
                                   (Can also use "history clear")
  history-delete [index]         - Delete a specific history entry
                                   (Can also use "history delete")
  history-stats                  - Show statistics about your calculations
                                   (Can also use "history stats")
  history-search [term]          - Search history for matching entries
                                   (Can also use "history search")

Examples:
  add 5 10 15      => Result: 30.0
  subtract 20 5 3  => Result: 12.0
  multiply 2 3 4   => Result: 24.0
  divide 100 4 5   => Result: 5.0
  5+10-2           => Result: 13.0
  history 5        => Shows the last 5 entries in history
  history stats    => Shows statistics about your calculations
                """
                return help_text.strip()
                
        self.command_handler.register_command("help", HelpCommand(self))
        logging.info("Help command registered")

    def register_expression_handler(self):
        """
        Register a command handler for mathematical expressions.
        
        This enables the calculator to evaluate expressions like "2+3*4".
        """
        class ExpressionCommand(Command):
            """Command that evaluates mathematical expressions like 2+3*4."""
            def __init__(self):
                self.logger = logging.getLogger(__name__)
                # Define operation mapping for expression parsing
                self.operations = {
                    '+': lambda x, y: x + y,
                    '-': lambda x, y: x - y,
                    '*': lambda x, y: x * y,
                    '/': lambda x, y: x / y if y != 0 else float('nan')
                }
            
            def execute(self, expression, *args, **kwargs):
                """
                Parse and evaluate a mathematical expression.
                
                Args:
                    expression: The mathematical expression as a string
                    
                Returns:
                    The result of the evaluation as a string
                """
                self.logger.info(f"Evaluating expression: {expression}")
                
                try:
                    # Simple expression evaluator - for production, use a proper parser
                    # This is just a demonstration for basic operations
                    # First, handle multiplication and division
                    result = self._evaluate_expression(expression)
                    self.logger.info(f"Expression result: {result}")
                    return str(result)
                except Exception as e:
                    self.logger.error(f"Error evaluating expression: {str(e)}")
                    return f"Error evaluating expression: {str(e)}"
            
            def _evaluate_expression(self, expression):
                """
                Evaluate a mathematical expression using a simple algorithm.
                
                Warning: This is a simplified implementation for demonstration purposes.
                         It doesn't handle all edge cases and operator precedence properly.
                
                Args:
                    expression: The expression to evaluate
                    
                Returns:
                    The numeric result
                """
                # Remove all spaces
                expression = expression.replace(' ', '')
                
                # Basic validation
                if not re.match(r'^[\d+\-*/().]+$', expression):
                    raise ValueError("Invalid characters in expression")
                
                # Handle parentheses first
                if '(' in expression:
                    # Find the innermost parentheses
                    start = expression.rfind('(')
                    end = expression.find(')', start)
                    if end == -1:
                        raise ValueError("Mismatched parentheses")
                    
                    # Evaluate the sub-expression inside parentheses
                    sub_result = self._evaluate_expression(expression[start+1:end])
                    
                    # Replace the parenthesized expression with its result
                    new_expr = expression[:start] + str(sub_result) + expression[end+1:]
                    return self._evaluate_expression(new_expr)
                
                # Find the terms and operators
                terms = re.findall(r'[+\-*/]?\d+\.?\d*', expression)
                if not terms:
                    raise ValueError("No valid terms found")
                
                # Handle first term which might have a sign
                result = float(terms[0])
                
                # Process remaining operations
                for i in range(1, len(terms)):
                    term = terms[i]
                    op = term[0] if term[0] in '+-*/' else '+'
                    value = float(term[1:] if term[0] in '+-*/' else term)
                    
                    result = self.operations[op](result, value)
                
                return result
            
        # Register the expression handler
        self.command_handler.register_command("expression", ExpressionCommand())
        logging.info("Expression handler registered")

    def start(self):
        """
        Start the calculator application and run the REPL loop.
        
        This method implements a Read-Eval-Print Loop (REPL) that:
        1. Reads user input
        2. Evaluates the command or expression
        3. Prints the result
        4. Loops for the next input
        
        Returns:
            int: Exit code (0 for success)
        """
        self.load_plugins()
        print("\n===== Advanced Python Calculator =====")
        print("Type 'help' for available commands or 'exit' to quit.")
        print("You can use commands like 'add 5 3' or expressions like '5+3'")
        print("Try 'menu' to see available operations")
        print("Type 'history' to view your calculation history")
        print("=======================================\n")
        logging.info("Application started. Type 'exit' to exit.")
        
        try:
            # REPL - Read-Eval-Print Loop
            while True:
                cmd_input = input("calc> ").strip()
                
                if not cmd_input:
                    continue
                    
                if cmd_input.lower() == 'exit':
                    print("Thank you for using Advanced Python Calculator. Goodbye!")
                    logging.info("Application exit")
                    break
                
                # First try to see if this is a known command
                command_parts = cmd_input.split()
                command = command_parts[0].lower() if command_parts else ""
                args = command_parts[1:] if len(command_parts) > 1 else []
                
                # Check for commands with subcommands (e.g., "history stats" instead of "history-stats")
                if len(command_parts) > 1 and command == "history":
                    # Check if "history-subcommand" exists
                    possible_command = f"history-{command_parts[1].lower()}"
                    if possible_command in self.command_handler.commands:
                        command = possible_command
                        args = command_parts[2:] if len(command_parts) > 2 else []
                
                # Check if this is a registered command
                is_registered_command = command in self.command_handler.commands
                
                # Special case: check if it's a mathematical expression
                # Only treat it as an expression if it's not a registered command
                if not is_registered_command and any(op in cmd_input for op in '+-*/') and not command.isalpha():
                    result = self.command_handler.execute_command_eafp("expression", cmd_input)
                    
                    # Add to history if it's a valid expression result
                    if result is not None and not result.startswith("Error"):
                        history_manager.add_entry("expression", cmd_input, result)
                else:
                    # Execute as a normal command
                    result = self.command_handler.execute_command_eafp(command, *args)
                    
                    # Add to history if it's a calculator operation (not a utility command)
                    if result is not None and command in ["add", "subtract", "multiply", "divide"] and not result.startswith("Error"):
                        history_manager.add_entry(command, ' '.join(args), result)
                
                if result is not None:
                    print(result)
                    
        except KeyboardInterrupt:
            print("\nCalculator interrupted. Goodbye!")
            logging.info("Application interrupted")
        except Exception as e:
            logging.error(f"Unexpected error in calculator: {str(e)}")
            print(f"\nAn unexpected error occurred: {str(e)}")
            print("Please check the logs for more information.")
            return 1
        finally:
            logging.info("Application shutdown")
            return 0
