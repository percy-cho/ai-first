### Requirement: Pip command executes pip3

The system SHALL provide a `pip` command that executes `pip3` with all passed arguments.

#### Scenario: Basic pip command execution

- **WHEN** user runs `pip --version`
- **THEN** system returns the pip3 version string

#### Scenario: Pip install package

- **WHEN** user runs `pip install <package>`
- **THEN** system executes `pip3 install <package>`

#### Scenario: Pip with subcommands

- **WHEN** user runs `pip list` or `pip show <package>`
- **THEN** system executes `pip3 list` or `pip3 show <package>`