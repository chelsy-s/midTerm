# Advanced Python Calculator


## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Development Journey](#development-journey)
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
- [Video Demonstration](#video-demonstration)



## Project Overview

This calculator application serves as a practical implementation of theoretical concepts taught in the course, including:

- **Design Patterns**: Practical application of GOF patterns in a real-world context
- **SOLID Principles**: Adherence to key software design principles
- **Test-Driven Development**: Extensive test coverage using pytest
- **Clean Code Practices**: Following PEP 8 and achieving a perfect Pylint score
- **Version Control**: Professional Git workflows with meaningful commits
- **Documentation**: Comprehensive API and user documentation

This calculator application integrates development practices through:

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

The Python Calculator was developed in a series of stages:

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

| Command | Format | 
|---------|--------|
| **Basic Operations** | | | |
| `add` | `add [num1] [num2] ...` | 
| `subtract` | `subtract [num1] [num2] ...` | 
| `multiply` | `multiply [num1] [num2] ...` | 
| `divide` | `divide [num1] [num2] ...` | 
| **Statistical Operations** | | | |
| `mean` | `mean [num1] [num2] ...` | 
| `median` | `median [num1] [num2] ...` | 
| `stddev` | `stddev [num1] [num2] ...` | 


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




## Video Demonstration

[Watch the Calculator Demo Video](https://github.com/chelsy-s/midTerm/issues/2#issue-2923072324)

This video showcases:
- Basic calculator operations
- Statistical functions
- History management features
- Expression evaluation
- Plugin system functionality





