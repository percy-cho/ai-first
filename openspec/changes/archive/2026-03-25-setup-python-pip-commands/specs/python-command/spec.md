## ADDED Requirements

### Requirement: Python command executes python3

The system SHALL provide a `python` command that executes `python3` with all passed arguments.

#### Scenario: Basic python command execution

- **WHEN** user runs `python --version`
- **THEN** system returns the Python 3 version string

#### Scenario: Python command with arguments

- **WHEN** user runs `python script.py arg1 arg2`
- **THEN** system executes `python3 script.py arg1 arg2`

#### Scenario: Python command with interactive mode

- **WHEN** user runs `python` without arguments
- **THEN** system starts the Python 3 interactive REPL