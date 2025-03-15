# Advanced Python Calculator

An advanced Python-based calculator application designed to demonstrate professional software development practices for the Software Engineering Graduate Course.

## Project Overview

This calculator application integrates professional software development practices through:

- Clean, maintainable code with extensive documentation
- Strategic implementation of design patterns (Command, Factory, Facade, etc.)
- Comprehensive logging with configurable severity levels
- Dynamic configuration via environment variables
- Sophisticated data handling with Pandas
- Interactive command-line interface (REPL)
- Extensive test coverage (>98%)

## Features

- **Basic Calculator Operations**: Add, Subtract, Multiply, and Divide implemented as plugins
- **Statistical Operations**: Mean, Median, Standard Deviation implemented as plugins
- **Calculation History Management**: Track, save, load, and analyze calculation history using Pandas
- **CSV File Handling**: Save and load calculation history to/from CSV files
- **Command Pattern Implementation**: Encapsulates operations as objects for flexible execution
- **Factory Method Pattern**: Creates operation instances dynamically
- **Facade Pattern**: Simplifies interaction with Pandas for history management
- **Plugin System**: Dynamically loads commands without modifying core code
- **Environment Variable Configuration**: Customizes behavior through environment settings
- **Comprehensive Logging**: Records operations at configurable detail levels
- **Error Handling**: Demonstrates both LBYL and EAFP approaches

## Setup

### Prerequisites

- Python 3.10 or higher
- Required packages (see requirements.txt)

### Installation

1. Clone the repository
   ```
   git clone https://github.com/YOUR_USERNAME/midTerm.git
   cd midTerm
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Run the application
   ```
   python main.py
   ```

## Environment Variables

The application can be configured using these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Running environment (DEVELOPMENT, TESTING, PRODUCTION) | PRODUCTION |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | INFO |

You can set these variables in a `.env` file in the project root directory.

Example `.env` file:
```
ENVIRONMENT=DEVELOPMENT
LOG_LEVEL=DEBUG
```

## Design Patterns Implementation

The calculator applies several design patterns to create a maintainable, flexible architecture:

### Command Pattern

The Command Pattern encapsulates operations as objects, enabling:
- Parameterization of clients with different requests
- Queueing or logging of requests
- Support for undoable operations

**Implementation**: [app/commands/__init__.py](app/commands/__init__.py)

```python
class Command(ABC):
    """
    Command Pattern: Abstract base class for all commands.
    """
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

class CommandHandler:
    """CommandHandler manages and executes commands."""
    def __init__(self):
        self.commands = {}
        self.logger = logging.getLogger(__name__)

    def register_command(self, command_name: str, command: Command):
        self.commands[command_name] = command
```

### Factory Method Pattern

The Factory Method pattern defines an interface for creating objects but lets subclasses decide which classes to instantiate. This is implemented in the calculator operations:

**Implementation**: [app/plugins/operations/__init__.py](app/plugins/operations/__init__.py)

```python
class OperationFactory:
    """
    Factory Method pattern implementation for creating operations.
    """
    _operations: Dict[str, Type[Operation]] = {}
    
    @classmethod
    def register_operation(cls, name: str, operation_class: Type[Operation]) -> None:
        cls._operations[name] = operation_class
    
    @classmethod
    def create_operation(cls, name: str) -> Optional[Operation]:
        if name in cls._operations:
            return cls._operations[name]()
        return None
```

### Facade Pattern

The Facade pattern provides a simplified interface to a complex subsystem. This is implemented in the history management module to provide a clean interface for Pandas operations:

**Implementation**: [app/history/__init__.py](app/history/__init__.py)

```python
class HistoryManager:
    """
    Manages calculator operation history using Pandas.
    
    This class implements the Facade pattern by providing a simplified interface
    to complex Pandas data operations.
    """
    # Methods for add_entry, save_history, load_history, etc.
    # that simplify interactions with the underlying Pandas DataFrame
```

### Plugin System

The application uses a dynamic plugin system to load command implementations at runtime:

**Implementation**: [app/__init__.py](app/__init__.py)

This design allows for extending the application's functionality without modifying core code, adhering to the Open/Closed Principle.

## Error Handling Approaches

The application demonstrates two complementary error handling approaches:

### Look Before You Leap (LBYL)

The LBYL approach checks conditions before performing an operation:

```python
# LBYL approach in CommandHandler.execute_command_lbyl
if command_name not in self.commands:
    error_msg = f"Unknown command: '{command_name}'"
    self.logger.warning(error_msg)
    return error_msg
    
try:
    command = self.commands[command_name]
    result = command.execute(*args, **kwargs)
    return result
except Exception as e:
    # ...
```

### Easier to Ask for Forgiveness than Permission (EAFP)

The EAFP approach uses try/except to handle errors after they occur:

```python
# EAFP approach in CommandHandler.execute_command_eafp
try:
    # Try to execute the command (Easier to Ask for Forgiveness)
    command = self.commands[command_name]
    result = command.execute(*args, **kwargs)
    return result
except KeyError:
    # Command not found
    error_msg = f"Unknown command: '{command_name}'. Type 'help' for available commands."
    self.logger.warning(error_msg)
    return error_msg
except Exception as e:
    # Other execution errors
    # ...
```

## Calculator Operations

The calculator implements basic arithmetic and statistical operations as plugins:

### Basic Operations

1. **Addition**: Adds two or more numbers together
   - Implementation: [app/plugins/operations/add/__init__.py](app/plugins/operations/add/__init__.py)

2. **Subtraction**: Subtracts numbers from the first operand
   - Implementation: [app/plugins/operations/subtract/__init__.py](app/plugins/operations/subtract/__init__.py)

3. **Multiplication**: Multiplies two or more numbers together
   - Implementation: [app/plugins/operations/multiply/__init__.py](app/plugins/operations/multiply/__init__.py)

4. **Division**: Divides the first operand by subsequent operands
   - Implementation: [app/plugins/operations/divide/__init__.py](app/plugins/operations/divide/__init__.py)
   - Special handling for division by zero

### Statistical Operations

5. **Mean**: Calculates the arithmetic mean (average) of multiple numbers
   - Implementation: [app/plugins/operations/statistics/__init__.py](app/plugins/operations/statistics/__init__.py)

6. **Median**: Calculates the median value of a set of numbers
   - Implementation: [app/plugins/operations/statistics/__init__.py](app/plugins/operations/statistics/__init__.py)

7. **Standard Deviation**: Calculates the sample standard deviation of a set of numbers
   - Implementation: [app/plugins/operations/statistics/__init__.py](app/plugins/operations/statistics/__init__.py)

Each operation implements validation to ensure proper arguments and error handling.

## History Management

The calculator includes a history management system that tracks all calculations:

1. **History Tracking**: Automatic recording of all calculator operations
   - Implementation: [app/history/__init__.py](app/history/__init__.py)

2. **History Commands**: View, save, load, clear, and analyze history
   - Implementation: [app/history/commands.py](app/history/commands.py)

3. **CSV Integration**: Save and load history data in CSV format using Pandas
   - Default location: `data/history.csv`

4. **History Statistics**: Analyze usage patterns with operation frequency and timestamps

### History Command Examples

```
history           # Show all calculation history
history 5         # Show the last 5 entries
history-save      # Save history to default file
history-load      # Load history from default file
history-clear     # Clear all history entries
history-stats     # Show statistics about your calculations
history-search 5  # Search for entries containing "5"
```

## Logging Implementation

The application implements a comprehensive logging system that:

1. Configures logging based on logging.conf file
2. Falls back to basic configuration if the file is missing
3. Adjusts log levels based on environment variables
4. Uses rotating file handlers to manage log size
5. Differentiates log messages by severity

**Implementation**: [app/__init__.py](app/__init__.py) and [logging.conf](logging.conf)

```python
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
```

## Data Handling with Pandas

The application uses Pandas for sophisticated data management:

1. **DataFrame Storage**: History is maintained in a structured Pandas DataFrame
2. **CSV Import/Export**: History can be saved to and loaded from CSV files
3. **Data Filtering**: Advanced filtering and search capabilities for history entries
4. **Statistics Generation**: Analysis of operation usage patterns

**Implementation**: [app/history/__init__.py](app/history/__init__.py)

## Testing

The application has comprehensive test coverage:
- Over 98% code coverage
- Unit tests for all core components and operations
- Edge case testing (like division by zero)
- Mock objects for external dependencies
- Continuous integration through GitHub Actions

To run the tests:

```bash
python -m pytest -v
```

To generate a coverage report:

```bash
python -m pytest --cov=app --cov-report=html
```

## Future Enhancements

The following enhancements are planned:

1. ~~Additional statistical operations (mean, median, standard deviation)~~ ✓ Implemented
2. Data visualization for calculation history
3. Extended CSV import/export capabilities
4. User profiles with separate history tracking
5. Web API for remote calculator access



© 2025 Advanced Python Calculator
