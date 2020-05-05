# Development guidelines

## Pair programming

All features should be programmed in pairs, the pairs are decided on when tasks are handed out, and it is up to the pair to decide the best strategy for collaboration, but a good recommendation is the liveshare plugin to visual studio code.
## Python version

All code is developed for python version 3.8.2

## External libraries

### Virtual environment

In order to keep your python installation clean, it is recommended that all libraries are installed in a virtual environment. In order to setup your virtual environment, follow these steps:
1. Open the command line and navigate to the repository folder.
2. Install virtualenv by running `python -m pip install virtualenv`
3. Create a new virtual environment by running `python -m virtualenv venv`
4. To activate the environment, run `venv\Scripts\activate`
5. To activate the environment in Visual Studio Code, open the command palette (<kbd>F1</kbd> ) and Select `Python: Select Interpreter`, and select the virtual environment.
6. Install required libraries by running `python -m pip install -r requirements.txt`

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

Tests are run using Nose testing framework. This will be installed when installing the requirements.txt file. To run the tests in VSCode, open the command palette(<kbd>F1</kbd>) and select `Python: Run All Tests`. To run the tests from the terminal, run the command `python -m nose`.

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
* The name of the test method starts with `test_`

### Integration

Every new feature should be tested for compatibility with the system as a whole. This is the responsibility of both the pair developing and the reviewer.

## Git guidelines

### Issues

Every development task has a separate issue. In this issue you can see information such as:
* Description: A detailed description of what needs to be done
* Labels: Indicates the category of the issue
* Milestone: Which milestone this development task counts towards
* Linked pull request: The pull request created for this issue

Each user story is broken down into several smaller development tasks, but the user story is still kept as an issue for future reference. Once all the development tasks for a user story are completed, the original user story should be closed. If you set up your pull requests correctly, this may be done automatically. More information about this is found below.

#### Dependencies

For dependencies we will use [Panorama](https://panorama-for-github.herokuapp.com/), which allows organization of issues as sub-issues. In Panorama, dependencies for an issue will be shown as sub-issues.

### Project board

In Github, under the tab "Projects", our project board can be found. Here is where all issues are tracked and marked as: To do, In progress, Review in progress, Review approved and Done. All issues that are created should be added to this project board and initialy set to "To do". The issue will then automatically move forwards during development and review if everything is setup correctly.

### Branches

Each user story has a separate branch based on master. From this every new development task related to this user story has a separate branched based on the user story branch. Once all development tasks for a user story are merged into the user story branch, this branch is merged into master.

### Pull requests and code review

#### Creating a branch

When a new branch is created, a pull request should be opened into the branch that the new branch is based on. This pull request should be marked with "WIP" to indicate that it is not ready for review or merging. This pull request is linked with the issue it is trying to resolve through the "Linked issues" in the sidebar. Note that the pull request should not be tied directly to the project.

#### Time to merge
Once the development on the current branch is completed, remove "WIP" from the title to indicate that the feature is completed. Branches can be merged into user story branches without code review, but when merging into the master branch a code review is necessary. This should be done by someone outside the pair. Any conflicts that arise is the responsibility of the pair merging into master.  
Once all conflicts are resolved, the code is reviewed as necessary and everyone is happy, it is time to merge...

#### Merging

When a pull request is approved, the branch is merged by the original authors. Within a user story the "Squash and merge" strategy should be employed. However, when merging into master, the normal "Merge pull request" strategy should be used.