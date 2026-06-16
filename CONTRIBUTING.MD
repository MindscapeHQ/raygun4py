## Getting Started with Local Development

Before starting, you'll need to ensure you have Python 3.10 or newer installed.

### Python 3

1. Install the virtual environment manager: `python3 -m pip install virtualenv`
2. Navigate to the project directory: `cd <project folder>`
3. Create a new virtual environment using Python 3: `python3 -m virtualenv venv3`
4. Activate the virtual environment. On Windows, use `venv3\Scripts\activate`. On Unix or MacOS, use `source venv3/bin/activate`.
5. Upgrade pip: `python3 -m pip install --upgrade pip`
6. Install the development dependencies and prepare the local package: `python3 -m pip install -e . --group dev`
7. Run tests with the command:
```bash
pytest
```

The legacy development extra is still available for older tooling that does not support dependency groups:

```bash
python3 -m pip install -e .[dev]
```

### Reproducible development install

The repository includes `pylock.dev.toml` as a known-good development environment snapshot for contributors and CI. It is not part of Raygun4Py's public installation contract; applications that use Raygun4Py should manage their own lock files.

To install from the lock file with pip 26.1 or newer:

```bash
python3 -m pip install -r pylock.dev.toml
```

The lock file is generated on Linux with Python 3.13, so prefer the dependency-group install above when validating compatibility across other Python versions or platforms.

To run tests with coverage:
```bash
pytest --cov=python3/raygun4py --cov-report=term-missing
```

### Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

```bash
# Check formatting
ruff format --check python3/

# Fix formatting
ruff format python3/

# Run linter
ruff check python3/

# Fix auto-fixable lint issues
ruff check --fix python3/
```

- Remember to deactivate the virtual environment when you're done: `deactivate`
