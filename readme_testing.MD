# Testing Guide for LLM Prompt Engineering Framework

This document provides guidelines for testing the LLM Prompt Engineering Framework application.

## Setting Up the Testing Environment

1. Install the required testing dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you're in the project root directory when running tests.

## Running Tests

### Running All Tests

To run all tests:
```bash
pytest
```

### Running Specific Test Categories

To run only unit tests:
```bash
pytest -m unit
```

To run only integration tests:
```bash
pytest -m integration
```

To run only UI-related tests:
```bash
pytest -m ui
```

### Testing Specific Components

To test just the prompt generator:
```bash
pytest tests/test_prompt_generator.py
```

To test just the content generator:
```bash
pytest tests/test_content_generator.py
```

To test just the UI helpers:
```bash
pytest tests/test_ui_helpers.py
```

## Test Coverage

To generate a test coverage report:
```bash
pytest --cov=. --cov-report=html
```

This will create an HTML report in the `htmlcov` directory that you can open in your browser.

## Writing New Tests

When adding new features or components, please follow these guidelines for writing tests:

1. Create a new test file in the `tests` directory with the naming convention `test_*.py`
2. Use appropriate pytest markers (`unit`, `integration`, `ui`) to categorize your tests
3. Mock external dependencies when appropriate
4. For UI components, use the `@pytest.mark.ui` marker and mock Streamlit components

Example test structure:
```python
import pytest

@pytest.mark.unit
class TestMyFeature:
    """Tests for my feature"""
    
    def test_basic_functionality(self):
        """Test that basic functionality works"""
        # Test code here
        assert True
    
    def test_edge_cases(self):
        """Test edge cases"""
        # Test edge cases here
        assert True
```

## Continuous Integration

The tests are automatically run in the CI/CD pipeline on each pull request and push to the main branch. Make sure all tests pass before submitting a pull request.

## Troubleshooting

If you encounter issues when running tests:

1. Make sure all dependencies are installed
2. Check that you're running from the project root directory
3. Try running with higher verbosity: `pytest -vv`
4. For UI test failures, ensure you've properly mocked all Streamlit components