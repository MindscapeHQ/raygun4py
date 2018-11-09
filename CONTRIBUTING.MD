# Getting Started with Local Development
The following will show you how to get started with local development

## Python 2
1. `cd <project folder> && virtualenv -p <PATH TO PYTHON2> venv2`
1. activate the virtual env
1. `pip install .[dev]`
1. Run tests
```
python -m unittest2 discover python2
```

## Python 3
1. `cd <project folder> && virtualenv -p <PATH TO PYTHON3> venv3`
1. activate the virtual env
1. `pip install .[dev]`
1. Run tests
```
python -m unittest discover python3
```
