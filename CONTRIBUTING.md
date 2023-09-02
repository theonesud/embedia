# How can I contribute?

## Guidelines

### Environment
- Use Python 3.9 for development

### Core Library
- Add type hints wherever possible
- Add docstrings to all internal classes and functions
- Make every function async if possible
- An async function should not contain a long running sync code, move long running things to background tasks
- Do not catch general exception: `Exception` until absolutely needed, catch specific exceptions

### Tests
- Write tests for every possible scenario
- Run mypy and all tests before creating a PR


### Commands
- flake8
- autopep8

- python -m pytest --cov=./ --cov-report=html

- mypy embedia
- isort .