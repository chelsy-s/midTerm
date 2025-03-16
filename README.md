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
- **Command Pattern Implementation**: Encapsulates operations as objects for flexible execution
- **Factory Method Pattern**: Creates operation instances dynamically
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
   git clone https://github.com/chelsy-s/midTerm.git
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

## Design Patterns

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

### Plugin System

The application uses a dynamic plugin system to load command implementations at runtime:

**Implementation**: [app/__init__.py](app/__init__.py)

This design allows for extending the application's functionality without modifying core code.

## Error Handling Approaches

The application demonstrates two complementary error handling approaches:

### Look Before You Leap (LBYL)

The LBYL approach checks conditions before performing an operation:

```python
# LBYL approach in CommandHandler.execute_command
if command_name in self.commands:
    return self.commands[command_name].execute(*args, **kwargs)
else:
    return f"No such command: {command_name}"
```

### Easier to Ask for Forgiveness than Permission (EAFP)

The EAFP approach uses try/except to handle errors after they occur:

```python
# EAFP approach in CommandHandler.execute_command_eafp
try:
    return self.commands[command_name].execute(*args, **kwargs)
except KeyError:
    return f"No such command: {command_name}"
except Exception as e:
    return f"Error executing command {command_name}: {str(e)}"
```

## Calculator Operations

The calculator implements four basic operations as plugins:

1. **Addition**: Adds two or more numbers together
   - Implementation: [app/plugins/operations/add/__init__.py](app/plugins/operations/add/__init__.py)

2. **Subtraction**: Subtracts numbers from the first operand
   - Implementation: [app/plugins/operations/subtract/__init__.py](app/plugins/operations/subtract/__init__.py)

3. **Multiplication**: Multiplies two or more numbers together
   - Implementation: [app/plugins/operations/multiply/__init__.py](app/plugins/operations/multiply/__init__.py)

4. **Division**: Divides the first operand by subsequent operands
   - Implementation: [app/plugins/operations/divide/__init__.py](app/plugins/operations/divide/__init__.py)
   - Special handling for division by zero

Each operation implements validation to ensure proper arguments and error handling.

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

1. Statistical operations
2. Calculation history management with Pandas
3. CSV data handling
4. Extended operation plugins

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

© 2025 Advanced Python Calculator
