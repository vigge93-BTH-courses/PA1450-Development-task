# Development guidelines

## Pair programming

All features should be programmed in pairs, the pairs are decided on when tasks are handed out, and it is up to the pair to decide the best strategy for collaboration.

## Python version

All code is developed for python version 3.8.2

## Style guidelines

### Code formatting

The code should follow PEP8 styling guidelines  
https://www.python.org/dev/peps/pep-0008/  
It is recommended to use a linter to check that the code follows PEP8

### Docstrings

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

### Modules

All modules should have a corresponding test-file with the name test_{module_name}.py.

### Methods

* Every method should have one or more unit-test associated with them to test their functionality.
* All comparisons for testing purposes are done with the assert operation.
* Unit tests should test all paths in a method.

### Integration

Every new feature should be tested for compatibility with the system as a whole. This is the responsibility of both the pair developing and the reviewer.

## Git guidelines

### Branches

Each feature is developed on a separate branch based on the master branch.

### Pull requests and code review

When a feature is completed a pull request is opened. Before merging, the new code should be approved by someone outside the pair.

### Merging

When a pull request is approved, the branched is merged into the master branch. Any conflicts that arise is the responsibility of the pair mergin into master.