"""
Advanced Python Calculator Application Module.

This module contains the core App class that serves as the main entry point
for the calculator application. It serves as the application's foundation,
orchestrating initialization, configuration, plugin discovery, and command execution.

The application demonstrates professional software engineering practices including:
- Design Patterns (Command, Factory Method, Facade, Strategy)
- Plugin-based architecture for extensibility
- Comprehensive logging with configurable levels
- Environment variable configuration for deployment flexibility
- Error handling strategies (LBYL and EAFP)
- Separation of concerns through modular design
"""
import os
import sys
import pkgutil
import importlib
import logging
import logging.config
import re
import inspect
from datetime import datetime
from typing import Dict, Any, Optional, List

from dotenv import load_dotenv

from app.commands import CommandHandler, Command
from app.history import history_manager  # Import the history manager

class App:
    """
    Main application class that orchestrates the calculator functionality.

    This class serves as the central coordinator, handling initialization,
    configuration, plugin loading, and command execution through a
    Read-Eval-Print Loop (REPL) interface. It implements a plugin
    system that dynamically discovers and loads functionality at runtime.

    The class demonstrates several design patterns:
    - Command Pattern: Commands are encapsulated as objects with a uniform interface
    - Factory Method: Operations are created through a factory for loose coupling
    - Strategy Pattern: Different operations implement the same interface but vary in behavior
    - Plugin Architecture: Functionality is added without modifying core code

    Attributes:
        command_handler: Central registry and executor for calculator commands
        settings: Dictionary of environment-based configuration settings
    """
    def __init__(self):
        """
        Initialize the calculator application.

        This constructor establishes the application environment by:
        1. Creating necessary directories
        2. Configuring the logging system
        3. Loading environment variables for configuration
        4. Initializing the command handler for processing user inputs

        The initialization follows a consistent sequence to ensure
        dependencies are properly established before they're needed.
        """
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)

        # Configure logging first for proper diagnostics during startup
        self.configure_logging()

        # Load environment variables from .env file if present
        env_loaded = load_dotenv(verbose=True)
        if env_loaded:
            logging.info("Environment variables loaded from .env file")
        else:
            logging.info("No .env file found, using system environment variables")

        # Parse environment variables into settings dictionary
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')

        # Initialize command handler for processing user commands
        self.command_handler = CommandHandler()

        # Log successful application initialization
        logging.info("Calculator application initialized in %s mode", self.settings.get('ENVIRONMENT'))

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
        for application settings. It leverages python-dotenv to load
        variables from a .env file if present, falling back to system
        environment variables.

        Supported variables:
            ENVIRONMENT: Running environment (DEVELOPMENT, TESTING, PRODUCTION)
            LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

        Returns:
            dict: Dictionary containing environment variables
        """
        settings = dict(os.environ.items())
        
        # Log loaded environment variables (excluding sensitive ones)
        safe_vars = {k: v for k, v in settings.items() 
                     if not any(sensitive in k.lower() for sensitive in ['pass', 'secret', 'key', 'token'])}

        logging.info(f"Environment: {settings.get('ENVIRONMENT', 'PRODUCTION')}")
        logging.info(f"Log level: {settings.get('LOG_LEVEL', 'INFO')}")

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
        Dynamically discover and load plugins from the app/plugins directory.

        This method implements a plugin system that enables extending
        the application without modifying core code, following the
        Open/Closed Principle from SOLID design principles.

        The plugin discovery process:
        1. Locates plugin packages in the designated plugins directory
        2. Imports each plugin module dynamically
        3. Registers commands found in each plugin
        4. Handles nested plugin structures (e.g., operation subplugins)
        5. Gracefully handles import errors for robust operation

        This approach enables a truly extensible architecture where
        new functionality can be added simply by creating new plugin
        packages that follow the established conventions.
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

        # Register specialized command handlers
        self._register_specialized_commands()

        # Register built-in commands
        self.register_help_command()
        self.register_expression_handler()

    def _register_specialized_commands(self):
        """
        Register specialized command handlers from various modules.

        This private helper method centralizes the registration of
        command handlers from specialized modules like operations,
        history, and utilities. It uses a consistent try-except pattern
        for robust error handling.
        """
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

Statistical Operations:
  mean [number1] [number2] ...    - Calculate the arithmetic mean (average) of a set of numbers
                                    Example: mean 10 20 30 40 => 25.0

  median [number1] [number2] ...  - Find the middle value in a set of numbers
                                    For odd sets: the middle value
                                    For even sets: the average of the two middle values
                                    Example: median 1 3 5 7 9 => 5.0

  stddev [number1] [number2] ...  - Calculate the sample standard deviation
                                    (a measure of how spread out the values are)
                                    Example: stddev 2 4 4 4 5 5 7 9 => 2.0

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
  add 5 10 15                 => Result: 30.0 (sum of all numbers)
  subtract 20 5 3             => Result: 12.0 (20 - 5 - 3)
  multiply 2 3 4              => Result: 24.0 (2 × 3 × 4)
  divide 100 4 5              => Result: 5.0 (100 ÷ 4 ÷ 5)

  # Statistical operations examples
  mean 10 20 30 40 50         => Result: 30.0 (average of all values)
  median 10 50 20 40 30       => Result: 30.0 (middle value when sorted)
  median 10 20 30 40          => Result: 25.0 (average of two middle values)
  stddev 10 10 10 10          => Result: 0.0 (no variation in the data)
  stddev 0 10 20 30           => Result: 12.91 (higher spread = higher std dev)

  # Expression examples
  5+10-2                      => Result: 13.0
  3*4/2                       => Result: 6.0
  (10+5)*2                    => Result: 30.0

  # History examples
  history 5                   => Shows the last 5 entries in history
  history-search 5            => Finds all calculations containing "5"
  history-stats               => Shows statistics about your calculations
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
        1. Loads plugins to establish available commands
        2. Presents a user-friendly interface
        3. Processes user input to execute commands or evaluate expressions
        4. Records calculation history for successful operations
        5. Handles interruptions and errors gracefully

        The REPL pattern provides an interactive environment where users
        can perform calculations, explore available commands, and manage
        calculation history without needing to restart the application.

        Returns:
            int: Exit code (0 for success, non-zero for error)
        """
        # Initialize by loading plugins
        self.load_plugins()

        # Display welcome message with instructions
        self._display_welcome_message()

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

                result = self._process_command(cmd_input)

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
            logging.info("Application shutdown complete")
            return 0

    def _display_welcome_message(self):
        """
        Display a welcome message with usage instructions.

        This private helper method centralizes the welcome message
        to keep the start method cleaner and more focused.
        """
        print("\n===== Advanced Python Calculator =====")
        print("Type 'help' for available commands or 'exit' to quit.")
        print("You can use commands like 'add 5 3' or expressions like '5+3'")
        print("Try 'menu' to see available operations")
        print("Type 'history' to view your calculation history")
        print("=======================================\n")
        logging.info("Application started. Type 'exit' to exit.")

    def _process_command(self, cmd_input):
        """
        Process a command or expression input by the user.

        This private helper method:
        1. Parses the input to determine if it's a command or expression
        2. Handles special cases like history subcommands
        3. Executes the appropriate command or evaluates the expression
        4. Records successful calculations in the history

        Args:
            cmd_input: The raw input string from the user

        Returns:
            The result of processing the command or None
        """
        # Parse command and arguments
        command_parts = cmd_input.split()
        command = command_parts[0].lower() if command_parts else ""
        args = command_parts[1:] if len(command_parts) > 1 else []

        # Handle history subcommands (e.g., "history stats" instead of "history-stats")
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
            if result is not None and command in ["add", "subtract", "multiply", "divide", "mean", "median", "stddev"] and not result.startswith("Error"):
                history_manager.add_entry(command, ' '.join(args), result)

        return result
