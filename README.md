# Running the weather application

## Set up the environment

### Setting up python

1. Open the application folder in Visual Studio Code.
2. Install virtualenv by running `python -m pip install virtualenv` in the terminal.
3. Create a new virtual environment by running `python -m virtualenv venv`
4. To activate the environment in Visual Studio Code, open the command palette (<kbd>F1</kbd> ) and Select `Python: Select Interpreter`, and select the virtual environment.
5. Install the required libraries by running `python -m pip install -r requirements.txt`

### Creating the database

To create the database, run the command `python -m program.backend initialize_database` in the terminal.

## Running the application

To run the application, press <kbd>F5</kbd> and navigate to [localhost:5000](localhost:5000) in the web-browser.
