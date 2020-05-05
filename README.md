# Development guidelines

## Pair programming

All features should be programmed in pairs, the pairs are decided on when tasks are handed out, and it is up to the pair to decide the best strategy for collaboration, but a good recommendation is the liveshare plugin to visual studio code.
## Python version

All code is developed for python version 3.8.2

## External libraries

### Virtual environment

In order to keep your python installation clean, it is recommended that all libraries are installed in a virtual environment. In order to setup your virtual environment, follow these steps:
1. Open the command line and navigate to the repository folder.
2. Install virtualenv by running ```python -m pip install virtualenv```
3. Create a new virtual environment by running ```python -m virtualenv venv```
4. To activate the environment, run ```venv\Scripts\activate```
5. To activate the environment in Visual Studio Code, open the command palette (<kbd>F1</kbd> ) and Select ```Python: Select Interpreter```, and select the virtual environment.
6. Install required libraries by running ```python -m pip install -r requirements.txt```

### Requirements.txt
All externally installed libraries should be saved to the requirements.txt file. This is most easily done by running the command  
```
python -m pip freeze > requirements.txt
```

## Style guidelines

### Code formatting

The code should follow PEP8 styling guidelines  
https://www.python.org/dev/peps/pep-0008/  
It is recommended to use a linter to check that the code follows PEP8

### Docstrings

Docstrings are not required for test files.

#### Methods and functions

The docstring for public methods and functions should be structured in the following way:  
```python
def some_method(param1, param2):
    """Short description of the method.

    More information about the method, what it does, and how you use it etc.

    Args:
        param1: A description of the parameter.
        param2: E.g data type, default values, usage, etc.

    Returns:
        Information about the return value of the method.

    Raises:
        ValueError: Description of why the error was raised.
    """
    pass
```
This should be followed unless:
* The method is not externally visible
* It is very short
* Its function is very obvious

#### Classes

The docstring for classes should be structured in the following way:
```python
class SomeClass:
    """Summary of class here.

    Longer class information....

    Attributes:
        attr1: Information about attr1.
        attr2: Information about attr2.
    """
```

More information about docstyle formatting can be found here:  
http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings

## Testing

Tests are run using Nose testing framework. This will be installed when installing the requirements.txt file. To run the tests in VSCode, open the command palette(<kbd>F1</kbd>) and select ```Python: Run All Tests```. To run the tests from the terminal, run the command ```python -m nose```.

### Given-When-Then

All tests should follow the pattern
```python
# Given
"""Initialize variables and setup environment for the tests."""
# When
"""Perform the action(s)."""
# Then
"""Assert the results."""
```

### Modules

All modules should have a corresponding test-file with the name test_{module_name}.py placed in the tests folder. Don't forget to import the module you are testing!

### Methods

* Every method should have one or more unit-test associated with them to test their functionality.
* All comparisons for testing purposes are done with the assert operation.
* Unit tests should test all execution paths in a method. This is measured with the coverage coverage.
* The name of the test method starts with ``test_``

### Integration

Every new feature should be tested for compatibility with the system as a whole. This is the responsibility of both the pair developing and the reviewer.

## Git guidelines

### Branches

Each feature is developed on a separate branch based on the master branch.

### Pull requests and code review

When a feature is completed a pull request is opened. Before merging, the new code should be approved by someone outside the pair.

### Merging

When a pull request is approved, the branched is merged by the original authors into the master branch. Any conflicts that arise is the responsibility of the pair merging into master.