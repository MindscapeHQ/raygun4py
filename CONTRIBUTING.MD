## Getting Started with Local Development
Before starting, you'll need to ensure you have the appropriate version of Python installed.

---

# Python 2
1. Install the virtual environment manager: `python2 -m pip install virtualenv`
2. Navigate to the project directory: `cd <project folder>`
3. Create a new virtual environment using Python 2: `python2 -m virtualenv venv2`
4. Activate the virtual environment. On Windows, use `venv2\Scripts\activate`. On Unix or MacOS, use `source venv2/bin/activate`.
5. Install the development dependencies: `python2 -m pip install .[dev]`
6. Run tests with the command: 
```bash
python2 -m unittest discover python2/tests
```
- Remember to deactivate the virtual environment when you're done: `deactivate`

---

# Python 3
1. Install the virtual environment manager: `python3 -m pip install virtualenv`
2. Navigate to the project directory: `cd <project folder>`
3. Create a new virtual environment using Python 3: `python3 -m virtualenv venv3`
4. Activate the virtual environment. On Windows, use `venv3\Scripts\activate`. On Unix or MacOS, use `source venv3/bin/activate`.
5. Install the development dependencies: `python3 -m pip install .[dev]`
6. Run tests with the command: 
```bash
python3 -m unittest discover python3/tests
```
- Remember to deactivate the virtual environment when you're done: `deactivate`

---
