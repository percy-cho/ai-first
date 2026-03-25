## ADDED Requirements

### Requirement: CLAUDE_CONFIG_DIR is set in bash environment
The system SHALL set CLAUDE_CONFIG_DIR environment variable pointing to `$HOME/.config/opencode` in `~/.bashrc`.

#### Scenario: Environment variable is configured
- **WHEN** a new bash shell is started
- **THEN** the CLAUDE_CONFIG_DIR environment variable SHALL be set to the user's home config directory

#### Scenario: Configuration uses portable path
- **WHEN** the configuration is read
- **THEN** it SHALL use `$HOME/.config/opencode` format rather than hardcoded absolute paths

#### Scenario: Configuration is appended to file
- **WHEN** ~/.bashrc is examined
- **THEN** the CLAUDE_CONFIG_DIR export SHALL appear at the end of the file

#### Scenario: Variable is exported
- **WHEN** the configuration line is parsed
- **THEN** it SHALL use `export` command to make the variable available to child processes
