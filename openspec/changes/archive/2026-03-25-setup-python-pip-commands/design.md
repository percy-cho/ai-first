## Context

On Linux systems, Python 3 is typically installed as `python3` without a `python` command. Many scripts and developer tools expect `python` and `pip` commands to exist. This design establishes a simple approach to create these command aliases.

## Goals / Non-Goals

**Goals:**
- Provide `python` command that executes `python3`
- Provide `pip` command that executes `pip3`
- Make aliases available in interactive shells

**Non-Goals:**
- System-wide installation requiring root privileges
- Modifying system-level Python configuration
- Impacting existing `python3` or `pip3` commands

## Decisions

### Approach: Shell Aliases vs Symlinks

**Decision:** Use shell aliases in `.bashrc`/`.zshrc`

**Rationale:**
- Aliases are user-level and don't require root access
- Easy to modify or remove if needed
- Work in interactive shells where developers typically use these commands
- No risk of conflicting with system-level Python management

**Alternatives considered:**
- Symlinks in `/usr/local/bin`: Requires root, may conflict with package manager
- PATH wrapper scripts: More complex, unnecessary for simple aliasing

### Configuration Location

**Decision:** Add aliases to the user's shell configuration file (`~/.bashrc` or `~/.zshrc`)

**Rationale:**
- Standard location for user-level shell customizations
- Automatically loaded in interactive sessions
- Does not require system-level changes

### Implementation

Add the following lines to the user's shell configuration:

```bash
# Python aliases for convenience
alias python='python3'
alias pip='pip3'
```

## Risks / Trade-offs

- **Risk:** Aliases only work in interactive shells, not in scripts
  - **Mitigation:** Scripts should use `#!/usr/bin/env python3` shebang or explicit `python3` command
- **Risk:** May shadow other `python` commands if installed later
  - **Mitigation:** User can remove or modify aliases as needed