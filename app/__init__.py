import os
import sys
import pkgutil
import importlib
import logging
import logging.config
from dotenv import load_dotenv

from app.commands import CommandHandler, Command

class App:
    """
    Main application class for the calculator.
    Handles initialization, configuration, and command execution.
    """
    def __init__(self):
        """Initialize the calculator application."""
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
        """Configure the logging system based on logging.conf."""
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
        This enables extending the application without modifying core code.
        """
        plugins_package = 'app.plugins'
        plugins_path = os.path.dirname(__file__) + '/plugins'
        
        if not os.path.exists(plugins_path):
            logging.warning(f"Plugins directory '{plugins_path}' not found")
            return
        
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.register_plugin_commands(plugin_module, plugin_name)
                except ImportError as e:
                    logging.error(f"Error importing plugin {plugin_name}: {e}")

    def register_plugin_commands(self, plugin_module, plugin_name):
        """
        Register commands from a plugin module.
        
        Args:
            plugin_module: The imported plugin module
            plugin_name: Name of the plugin
        """
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                command_instance = item()
                self.command_handler.register_command(plugin_name, command_instance)
                logging.info(f"Command '{plugin_name}' from plugin '{plugin_name}' registered")

    def start(self):
        """
        Start the calculator application and run the REPL loop.
        """
        self.load_plugins()
        logging.info("Application started. Type 'exit' to exit.")
        
        try:
            # REPL - Read-Eval-Print Loop
            while True:
                cmd_input = input("calc> ").strip()
                
                if cmd_input.lower() == 'exit':
                    logging.info("Application exit")
                    break
                
                # Use EAFP approach for command execution
                result = self.command_handler.execute_command_eafp(cmd_input)
                if result is not None:
                    print(result)
                    
        except KeyboardInterrupt:
            logging.info("Application interrupted")
        finally:
            logging.info("Application shutdown")
            return 0
