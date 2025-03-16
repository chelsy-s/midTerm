<<<<<<< HEAD
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
=======
# Advanced Python Calculator

An advanced Python-based calculator application designed to demonstrate professional software development practices for the Software Engineering Graduate Course.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Development Journey](#development-journey)
- [Technical Architecture](#technical-architecture)
- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Design Patterns Implementation](#design-patterns-implementation)
- [Error Handling Approaches](#error-handling-approaches)
- [Calculator Operations](#calculator-operations)
- [Command Reference](#command-reference)
- [History Management](#history-management)
- [Logging Implementation](#logging-implementation)
- [Data Handling with Pandas](#data-handling-with-pandas)
- [Testing and Code Quality](#testing-and-code-quality)
- [Version Control](#version-control)
- [GitHub Actions Implementation](#github-actions-implementation)
- [Project Benefits and Advantages](#project-benefits-and-advantages)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Video Demonstration](#video-demonstration)
- [Contributors](#contributors)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Project Overview

This calculator application was developed as part of the Software Engineering Graduate Course to demonstrate mastery of professional software engineering principles. It serves as a practical implementation of theoretical concepts taught in the course, including:

- **Design Patterns**: Practical application of GOF patterns in a real-world context
- **SOLID Principles**: Adherence to key software design principles
- **Test-Driven Development**: Extensive test coverage using pytest
- **Clean Code Practices**: Following PEP 8 and achieving a perfect Pylint score
- **Version Control**: Professional Git workflows with meaningful commits
- **Documentation**: Comprehensive API and user documentation

This calculator application integrates professional software development practices through:

- Clean, maintainable code with extensive documentation
- Strategic implementation of design patterns (Command, Factory, Facade, etc.)
- Comprehensive logging with configurable severity levels
- Dynamic configuration via environment variables
- Sophisticated data handling with Pandas
- Interactive command-line interface (REPL)
- Extensive test coverage (>90%)
- Code quality validation with Pylint

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

## Development Journey

The Advanced Python Calculator was developed in a series of structured stages:

### Stage 1: Core Architecture and Basic Operations
- Established the command-line interface (REPL)
- Implemented the Command pattern and CommandHandler
- Created the basic arithmetic operations (add, subtract, multiply, divide)
- Set up initial project structure and documentation

### Stage 2: Plugin System and History Management
- Developed the plugin system for dynamic loading of operations
- Implemented the HistoryManager using Pandas for data handling
- Created CSV export/import functionality
- Added history commands (view, save, load, clear)

### Stage 3: Advanced Features and Testing
- Integrated statistical operations (mean, median, standard deviation)
- Enhanced the expression parser for direct mathematical expressions
- Implemented comprehensive logging with configurable levels
- Created extensive test suite with Pytest

### Stage 4: Code Quality and Refinement
- Ensured code quality with Pylint (achieving 10.00/10 score)
- Improved test coverage (reaching >90%)
- Enhanced documentation with comprehensive README
- Added GitHub Actions for continuous integration

## Technical Architecture

The calculator follows a modular architecture with clear separation of concerns:

```
                      +--------------------+
                      |        App         |
                      | (Main Application) |
                      +--------+-----------+
                               |
                               v
       +-------------------------------------------+
       |              CommandHandler               |
       | (Processes and routes user commands)      |
       +---+-----------------+---------------+-----+
           |                 |               |
           v                 v               v
+-------------------+ +-------------+ +-------------+
|   Plugin System   | |  History    | |  Expression |
| (Dynamic loading) | |  Manager    | |  Evaluator  |
+--------+----------+ +------+------+ +------+------+
         |                   |               |
         v                   v               |
+--------+------+       +----+----+          |
| Operations    |       | Pandas   |          |
| (Add,Divide,  +<----->+ (Data    |          |
|  etc.)        |       | Handling) |          |
+---------------+       +-----------+          |
                               ^               |
                               |               |
                      +--------+--------------+
                      |    Results Processing  |
                      +------------------------+
```

This architecture provides:
1. **Loose coupling** between components
2. **High cohesion** within modules
3. **Extensibility** through the plugin system
4. **Maintainability** through clear separation of concerns

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
| `HISTORY_FILE_PATH` | Custom file path for history storage | data/history.csv |

You can set these variables in a `.env` file in the project root directory.

Example `.env` file:
```
ENVIRONMENT=DEVELOPMENT
LOG_LEVEL=DEBUG
HISTORY_FILE_PATH=data/custom_history.csv
```

## Design Patterns Implementation

The calculator applies several design patterns to create a maintainable, flexible architecture:

### Command Pattern

The Command Pattern encapsulates operations as objects, enabling:
- Parameterization of clients with different requests
- Queueing or logging of requests
- Support for undoable operations

**Implementation**: See [app/commands/__init__.py](app/commands/__init__.py)

### Factory Method Pattern

The Factory Method pattern defines an interface for creating objects but lets subclasses decide which classes to instantiate. This is implemented in the calculator operations.

**Implementation**: See [app/plugins/operations/__init__.py](app/plugins/operations/__init__.py)

### Facade Pattern

The Facade pattern provides a simplified interface to a complex subsystem. This is implemented in the history management module to provide a clean interface for Pandas operations.

**Implementation**: See [app/history/__init__.py](app/history/__init__.py)

### Strategy Pattern

The Strategy Pattern allows defining a family of algorithms, encapsulating each one, and making them interchangeable. This is implemented in the calculator operations.

**Implementation**: Each operation implements the same interface but with different algorithms.

### Plugin System

The application uses a dynamic plugin system to load command implementations at runtime.

**Implementation**: See [app/__init__.py](app/__init__.py)

This design allows for extending the application's functionality without modifying core code, adhering to the Open/Closed Principle.

## Error Handling Approaches

The application demonstrates two complementary error handling approaches:

### Look Before You Leap (LBYL)

The LBYL approach checks conditions before performing an operation. This approach is implemented in the CommandHandler's execute_command_lbyl method.

### Easier to Ask for Forgiveness than Permission (EAFP)

The EAFP approach uses try/except to handle errors after they occur. This approach is implemented in the CommandHandler's execute_command_eafp method.

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

## Command Reference

Below is a comprehensive reference of all available commands:

| Command | Format | Description | Example |
|---------|--------|-------------|---------|
| **Basic Operations** | | | |
| `add` | `add [num1] [num2] ...` | Adds two or more numbers | `add 5 10 15` → `30.0` |
| `subtract` | `subtract [num1] [num2] ...` | Subtracts numbers from the first | `subtract 20 5 3` → `12.0` |
| `multiply` | `multiply [num1] [num2] ...` | Multiplies numbers together | `multiply 2 3 4` → `24.0` |
| `divide` | `divide [num1] [num2] ...` | Divides first number by others | `divide 100 4 5` → `5.0` |
| **Statistical Operations** | | | |
| `mean` | `mean [num1] [num2] ...` | Calculates the arithmetic mean | `mean 10 20 30 40` → `25.0` |
| `median` | `median [num1] [num2] ...` | Finds the middle value | `median 1 3 5 7 9` → `5.0` |
| `stddev` | `stddev [num1] [num2] ...` | Calculates standard deviation | `stddev 2 4 4 4 5 5 7 9` → `2.0` |
| **History Management** | | | |
| `history` | `history [limit]` | Shows calculation history | `history 5` → Last 5 entries |
| `history-save` | `history-save [filepath]` | Saves history to CSV | `history-save data/backup.csv` |
| `history-load` | `history-load [filepath]` | Loads history from CSV | `history-load data/backup.csv` |
| `history-clear` | `history-clear` | Clears all history entries | `history-clear` |
| `history-delete` | `history-delete [index]` | Deletes a specific entry | `history-delete 3` |
| `history-stats` | `history-stats` | Shows usage statistics | `history-stats` |
| `history-search` | `history-search [term]` | Searches history entries | `history-search 5` |
| **Utility Commands** | | | |
| `help` | `help` | Shows help information | `help` |
| `menu` | `menu` | Shows available operations | `menu` |
| `clear` or `cls` | `clear` | Clears the screen | `clear` |
| `exit` | `exit` | Exits the calculator | `exit` |
| **Expressions** | | | |
| Mathematical expressions | `[expression]` | Evaluates expressions | `5+10*2` → `25.0` |

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

### CSV Data Storage Format

The history data is stored in a structured CSV format with the following columns:

| Column Name | Description | Example Value |
|-------------|-------------|---------------|
| `id` | Unique identifier for each calculation | 1, 2, 3, ... |
| `timestamp` | Date and time when the calculation was performed | 2025-03-15 14:30:45 |
| `operation` | The operation that was performed | add, subtract, multiply, divide, mean, median, stddev, expression |
| `input` | The input parameters for the operation | 5 10 15 |
| `result` | The result of the calculation | 30.0 |

Example CSV content:
```csv
id,timestamp,operation,input,result
1,2025-03-15 14:30:45,add,"5 10 15",30.0
2,2025-03-15 14:31:20,multiply,"2 3 4",24.0
3,2025-03-15 14:32:05,expression,"5+10*2",25.0
```

This structured format enables:
- Easy import/export of calculation history
- Data analysis and visualization
- Filtering and searching of past calculations
- Generation of usage statistics

## Logging Implementation

The application implements a comprehensive logging system that:

1. Configures logging based on logging.conf file
2. Falls back to basic configuration if the file is missing
3. Adjusts log levels based on environment variables
4. Uses rotating file handlers to manage log size
5. Differentiates log messages by severity

**Implementation**: See [app/__init__.py](app/__init__.py) and [logging.conf](logging.conf)

The logging configuration file (`logging.conf`) defines:
- Multiple loggers (root and application-specific)
- Console and file handlers
- Different formatting for console vs. file output
- Rotation of log files to manage file size

## Data Handling with Pandas

The application uses Pandas for sophisticated data management:

1. **DataFrame Storage**: History is maintained in a structured Pandas DataFrame
2. **CSV Import/Export**: History can be saved to and loaded from CSV files
3. **Data Filtering**: Advanced filtering and search capabilities for history entries
4. **Statistics Generation**: Analysis of operation usage patterns

**Implementation**: See [app/history/__init__.py](app/history/__init__.py)

## Testing and Code Quality

### Test Coverage

The application has comprehensive test coverage:
- Over 90% overall code coverage
- 105 passing tests covering all components
- 2 skipped tests (related to Python 3.12 limitations)
- Edge case testing (like division by zero)
- Mock objects for external dependencies

### Continuous Integration

The project uses GitHub Actions for continuous integration to ensure code quality:
- Automated test execution on every push
- Code coverage reporting
- Pylint code quality checks
- Dependency vulnerability scanning

### Code Quality with Pylint

The codebase achieves a perfect Pylint score of 10.00/10, indicating exceptional code quality:
- Adherence to PEP 8 style guidelines
- Proper docstrings and documentation
- Appropriate naming conventions
- Optimal code organization
- No unused variables or imports
- No duplicated code

To run the tests:

```bash
python -m pytest -v
```

To generate a coverage report:

```bash
python -m pytest --cov=app --cov-report=html
```

To check code quality:

```bash
pylint app/
```

## Version Control

The project follows professional version control practices:

### Branching Strategy
- `main` branch for stable, production-ready code
- Feature branches for new functionality
- Bugfix branches for issue resolution
- Pull requests with code reviews before merging

### Commit Conventions
- Clear, descriptive commit messages
- Logical grouping of changes
- References to issues or requirements
- Regular, small commits rather than large, infrequent ones

### CI/CD Integration
- GitHub Actions workflows triggered on push events
- Automated testing and linting in the CI pipeline
- Quality gates to prevent merging of problematic code

## GitHub Actions Implementation

This project uses GitHub Actions to automate testing and quality assurance. The workflow runs automatically on every push to the main branch and on pull requests, ensuring all code changes meet the project's quality standards.

### Workflow Features

The GitHub Actions workflow includes:

- **Automated Testing**: Runs all pytest tests automatically
- **Code Coverage**: Ensures test coverage remains above 90%
- **Code Quality**: Verifies all code meets Pylint standards (10.00/10 score)
- **Badge Generation**: Creates a coverage badge for the repository
- **Failure Prevention**: Prevents merging code that doesn't meet standards

### Benefits of CI/CD

- **Early Detection**: Identifies issues immediately, not at submission time
- **Quality Assurance**: Maintains consistently high code quality
- **Documentation**: Provides ongoing evidence of meeting course requirements
- **Professional Practice**: Follows industry standards for software delivery

### How to Use

1. **View Run Results**: After each push, check the "Actions" tab in your GitHub repository
2. **Fix Failing Tests**: If tests fail, the logs provide detailed information on what needs fixing
3. **Manual Triggering**: You can manually trigger workflow runs from the Actions tab
4. **Local Verification**: Run `pytest` and `pylint` locally before pushing to ensure success

## Project Benefits and Advantages

### Educational Value
- Demonstrates multiple design patterns in a practical context
- Shows how to implement a plugin architecture
- Exemplifies professional logging practices
- Illustrates test-driven development approaches

### Extensibility
- New operations can be added as plugins without modifying core code
- Additional commands can be implemented by extending the Command pattern
- Environment configuration provides deployment flexibility

### Code Quality
- High test coverage ensures reliability
- Perfect Pylint score indicates excellent code quality
- Comprehensive documentation for future maintainability
- Clear separation of concerns through modular design

### Real-world Applications
- The architecture can be adapted for various computational tools
- The plugin system demonstrates extensible application design
- The history management shows practical Pandas usage for data analysis

## Troubleshooting

Below are solutions to common issues you might encounter:

### Installation Issues

**Problem**: Dependencies fail to install  
**Solution**: Ensure you're using Python 3.10+ and try installing dependencies individually:
```bash
pip install python-dotenv==1.0.0
pip install pandas==2.1.0
# etc.
```

**Problem**: ModuleNotFoundError when running the application  
**Solution**: Verify that all dependencies are installed and you're running from the project root directory.

### Runtime Issues

**Problem**: History doesn't persist between sessions  
**Solution**: Use `history-save` before exiting and `history-load` when starting a new session.

**Problem**: "Invalid syntax" when entering an expression  
**Solution**: Ensure expressions follow the supported format. Complex expressions may require parentheses for proper order of operations.

**Problem**: Logging not working as expected  
**Solution**: Check your `.env` file settings and ensure the logs directory exists and is writable.

## Future Enhancements

The following enhancements are planned:

1. ~~Additional statistical operations (mean, median, standard deviation)~~ ✓ Implemented
2. Data visualization for calculation history
3. Extended CSV import/export capabilities
4. User profiles with separate history tracking
5. Web API for remote calculator access
6. Interactive graphical user interface (GUI)
7. Expression parser improvements for more complex calculations
8. Support for scientific notation and complex numbers
9. Custom operator plugins for specialized mathematical functions
10. Result caching for performance optimization

## Video Demonstration

[Watch the Calculator Demo Video](https://youtu.be/your-video-id)

This video showcases:
- Basic calculator operations
- Statistical functions
- History management features
- Expression evaluation
- Plugin system functionality

## Contributors

- Chelsy - Project Creator and Developer - [GitHub Profile](https://github.com/chelsy-s)

## Acknowledgments

- Software Engineering Graduate Course Instructors for guidance and requirements
- Python community for excellent documentation and libraries
- Pandas development team for the powerful data analysis library
- Open-source community for inspiration on plugin architectures and design patterns




>>>>>>> deploy/prod-code
