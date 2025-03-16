"""
Tests for the statistical operations (mean, median, standard deviation).
"""
import pytest
from unittest.mock import patch
from app.plugins.operations.statistics import MeanOperation, MedianOperation, StddevOperation

class TestMeanOperation:
    """Test cases for the Mean operation."""

    def setup_method(self):
        """Set up for each test method."""
        self.operation = MeanOperation()

    def test_validate_args_valid(self):
        """Test validation with valid arguments."""
        # Test with integers
        is_valid, error_message = self.operation.validate_args("1", "2", "3", "4")
        assert is_valid is True
        assert error_message is None

        # Test with floats
        is_valid, error_message = self.operation.validate_args("1.5", "2.5", "3.5")
        assert is_valid is True
        assert error_message is None

    def test_validate_args_invalid(self):
        """Test validation with invalid arguments."""
        # Test with too few arguments
        is_valid, error_message = self.operation.validate_args("5")
        assert is_valid is False
        assert "requires at least two numbers" in error_message

        # Test with non-numeric arguments
        is_valid, error_message = self.operation.validate_args("1", "two", "3")
        assert is_valid is False
        assert "not a valid number" in error_message

    def test_execute_success(self):
        """Test successful execution of the mean operation."""
        # Test with integers
        result = self.operation.execute("2", "4", "6", "8")
        assert result == "5.0"

        # Test with floats
        result = self.operation.execute("1.5", "2.5", "3.5")
        assert result == "2.5"

        # Test with mixed numbers
        result = self.operation.execute("1", "2.5", "3")
        assert float(result) == pytest.approx(2.1666, 0.001)

    def test_execute_invalid_args(self):
        """Test execution with invalid arguments."""
        # Should return the error message from validate_args
        result = self.operation.execute("5")
        assert "requires at least two numbers" in result

        result = self.operation.execute("1", "not_a_number", "3")
        assert "not a valid number" in result

    def test_execute_unexpected_error(self):
        """Test handling of unexpected errors during execution."""
        # Mock the statistics.mean function to raise an exception
        with patch('statistics.mean', side_effect=Exception("Test error")):
            result = self.operation.execute("1", "2", "3")
            assert "Error during mean calculation" in result
            assert "Test error" in result

class TestMedianOperation:
    """Test cases for the Median operation."""

    def setup_method(self):
        """Set up for each test method."""
        self.operation = MedianOperation()

    def test_validate_args_valid(self):
        """Test validation with valid arguments."""
        # Test with odd number of arguments
        is_valid, error_message = self.operation.validate_args("1", "2", "3", "4", "5")
        assert is_valid is True
        assert error_message is None

        # Test with even number of arguments
        is_valid, error_message = self.operation.validate_args("1.5", "2.5", "3.5", "4.5")
        assert is_valid is True
        assert error_message is None

    def test_validate_args_invalid(self):
        """Test validation with invalid arguments."""
        # Test with too few arguments
        is_valid, error_message = self.operation.validate_args("5", "6")
        assert is_valid is False
        assert "requires at least three numbers" in error_message

        # Test with non-numeric arguments
        is_valid, error_message = self.operation.validate_args("1", "2", "three", "4")
        assert is_valid is False
        assert "not a valid number" in error_message

    def test_execute_success(self):
        """Test successful execution of the median operation."""
        # Test with odd number of integers (should return the middle value)
        result = self.operation.execute("1", "3", "5")
        assert result == "3.0"

        # Test with even number of integers (should return the average of the two middle values)
        result = self.operation.execute("1", "3", "5", "7")
        assert result == "4.0"

        # Test with unsorted values
        result = self.operation.execute("5", "2", "8", "1", "9")
        assert result == "5.0"

    def test_execute_invalid_args(self):
        """Test execution with invalid arguments."""
        # Should return the error message from validate_args
        result = self.operation.execute("5", "6")
        assert "requires at least three numbers" in result

        result = self.operation.execute("1", "2", "not_a_number")
        assert "not a valid number" in result

    def test_execute_unexpected_error(self):
        """Test handling of unexpected errors during execution."""
        # Mock the statistics.median function to raise an exception
        with patch('statistics.median', side_effect=Exception("Test error")):
            result = self.operation.execute("1", "2", "3", "4", "5")
            assert "Error during median calculation" in result
            assert "Test error" in result

class TestStddevOperation:
    """Test cases for the Standard Deviation operation."""

    def setup_method(self):
        """Set up for each test method."""
        self.operation = StddevOperation()

    def test_validate_args_valid(self):
        """Test validation with valid arguments."""
        # Test with integers
        is_valid, error_message = self.operation.validate_args("1", "2", "3", "4")
        assert is_valid is True
        assert error_message is None

        # Test with floats
        is_valid, error_message = self.operation.validate_args("1.5", "2.5", "3.5")
        assert is_valid is True
        assert error_message is None

    def test_validate_args_invalid(self):
        """Test validation with invalid arguments."""
        # Test with too few arguments
        is_valid, error_message = self.operation.validate_args("5")
        assert is_valid is False
        assert "requires at least two numbers" in error_message

        # Test with non-numeric arguments
        is_valid, error_message = self.operation.validate_args("1", "two", "3")
        assert is_valid is False
        assert "not a valid number" in error_message

    def test_execute_success(self):
        """Test successful execution of the standard deviation operation."""
        # Test with values having a known standard deviation
        # For [2, 4, 4, 4, 5, 5, 7, 9], the sample standard deviation is ~2.14
        result = self.operation.execute("2", "4", "4", "4", "5", "5", "7", "9")
        assert float(result) == pytest.approx(2.14, 0.01)

        # Test with another set of values
        # For [1, 2, 3, 4, 5], the sample standard deviation is ~1.58
        result = self.operation.execute("1", "2", "3", "4", "5")
        assert float(result) == pytest.approx(1.58, 0.01)

    def test_execute_invalid_args(self):
        """Test execution with invalid arguments."""
        # Should return the error message from validate_args
        result = self.operation.execute("5")
        assert "requires at least two numbers" in result

        result = self.operation.execute("1", "not_a_number", "3")
        assert "not a valid number" in result

    def test_execute_unexpected_error(self):
        """Test handling of unexpected errors during execution."""
        # Mock the statistics.stdev function to raise an exception
        with patch('statistics.stdev', side_effect=Exception("Test error")):
            result = self.operation.execute("1", "2", "3")
            assert "Error during standard deviation calculation" in result
            assert "Test error" in result
