# Python Project

This is a comprehensive Python project that provides a simple note-taking command-line application.

## Features

*   **CLI Application**: A note-taking app built with `typer`.
*   **Modern Packaging**: Uses `pyproject.toml` and `hatch` for building.
*   **Structured Code**: Follows a `src` layout with separated logic, database, and configuration.
*   **Testing**: Includes a test suite with `pytest` and coverage reporting.
*   **Linting and Formatting**: Enforced with `ruff`.
*   **Automation**: A `Makefile` provides commands for common development tasks.

## Getting Started

### Prerequisites

*   Python 3.8+
*   `make`

### Installation

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd python-project
    ```

2.  **Create the virtual environment and install dependencies:**
    This command will create a `.venv` directory, activate it, and install all the necessary packages defined in `pyproject.toml`.
    ```sh
    make install
    ```

## Usage

The application is a command-line tool for taking notes. You can run it using the `make run` command, which is a shortcut for activating the virtual environment and running the `note` script.

### Commands

*   **`add`**: Add a new note.
    ```sh
    make run -- add "My first note"
    ```

*   **`list`**: List all existing notes.
    ```sh
    make run -- list
    ```

*   **`clear`**: Clear all notes. You will be prompted for confirmation.
    ```sh
    make run -- clear
    ```
    To bypass the confirmation prompt, use the `--force` flag:
    ```sh
    make run -- clear --force
    ```

## Development

### Running Tests

To run the test suite, use the `test` command. This will execute all tests in the `tests/` directory and generate a coverage report.
```sh
make test
```

### Linting and Formatting

To check for code quality and format the code according to the project style, use the `lint` command.
```sh
make lint
``` 