## Why

On many Linux systems, the `python` command doesn't exist by default—only `python3` is available. This creates friction for developers and scripts that expect the traditional `python` and `pip` commands. Setting up these aliases improves compatibility and reduces confusion.

## What Changes

- Create `python` command alias pointing to `python3`
- Create `pip` command alias pointing to `pip3`

## Capabilities

### New Capabilities

- `python-command`: Provides `python` command that executes `python3`
- `pip-command`: Provides `pip` command that executes `pip3`

### Modified Capabilities

None - this is a new capability addition.

## Impact

- Shell configuration files (`.bashrc`, `.zshrc`, or equivalent)
- No breaking changes - only adds new convenient command aliases
- Affects developer workflow and script compatibility