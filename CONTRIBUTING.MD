## Getting Started with Local Development

Before starting, you'll need to ensure you have Python 3.10 or newer installed.

### Python 3

1. Install the virtual environment manager: `python3 -m pip install virtualenv`
2. Navigate to the project directory: `cd <project folder>`
3. Create a new virtual environment using Python 3: `python3 -m virtualenv venv3`
4. Activate the virtual environment. On Windows, use `venv3\Scripts\activate`. On Unix or MacOS, use `source venv3/bin/activate`.
5. Upgrade to pip 25.1 or newer, which supports dependency groups: `python3 -m pip install --upgrade "pip>=25.1"`
6. Install the development dependencies and prepare the local package: `python3 -m pip install -e . --group dev`
7. Run tests with the command:
```bash
pytest
```

The legacy development extra is still available for older tooling that does not support dependency groups:

```bash
python3 -m pip install -e .[dev]
```

### Locked development install

The repository includes `pylock.dev.toml` as a hash-verified Python dependency snapshot for the locked CI job. It is not part of Raygun4Py's public installation contract; applications that use Raygun4Py should manage their own lock files.

The lock file uses pip's experimental PEP 751 support and is generated with CPython 3.13.5 on Linux x86-64 and pip 26.1.2. Install it on CPython 3.13 in that environment with the same pip version:

```bash
python3 -m pip install --upgrade "pip==26.1.2"
python3 -m pip install -r pylock.dev.toml
python3 -m pip install --no-deps --no-build-isolation -e .
python3 -m pip check
```

The lock file contains Raygun4Py's runtime, development, and build dependencies, but not the local package itself. The editable install uses the locked build backend without re-resolving dependencies or creating an isolated build environment. Prefer the dependency-group install above when validating compatibility across other Python versions or platforms.

Regenerate the lock file in the same target environment after changing runtime or development dependencies:

```bash
python3 -m pip install --upgrade "pip==26.1.2"
python3 -m pip lock \
  "jsonpickle>=4.0.4" \
  "blinker>=1.3.0" \
  "requests>=2.9.1" \
  --group dev \
  --output pylock.dev.toml
```

The explicit runtime requirements keep the local editable package out of the lock without manual lock-file edits. Review this command whenever `[project].dependencies` changes.

### Tests

Run the unit and middleware tests with coverage:

```bash
pytest --cov=python3/raygun4py --cov-report=term-missing
```

The functional tests send deliberate test errors to Raygun and are skipped when `RAYGUN_API_KEY` is not set. Run them only against a non-production Raygun application:

```bash
RAYGUN_API_KEY="your_test_api_key" pytest python3/tests/test_functional.py -v
```

Do not commit the API key or store it in this repository.

### Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting and mypy for static type checking.

```bash
# Check formatting
ruff format --check python3/

# Fix formatting
ruff format python3/

# Run linter
ruff check python3/

# Fix auto-fixable lint issues
ruff check --fix python3/

# Check types
mypy python3/raygun4py
```

Build with the locked build toolchain after installing `pylock.dev.toml` as described above:

```bash
python3 -m build --no-isolation
```

- Remember to deactivate the virtual environment when you're done: `deactivate`
