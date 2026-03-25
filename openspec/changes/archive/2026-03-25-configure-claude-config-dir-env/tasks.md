## 1. Configure Environment Variable

- [x] 1.1 Edit ~/.bashrc and add CLAUDE_CONFIG_DIR export at file end
- [x] 1.2 Verify the configuration line uses correct syntax: export CLAUDE_CONFIG_DIR="$HOME/.config/opencode"
- [x] 1.3 Save the file

## 2. Verify Configuration

- [x] 2.1 Source ~/.bashrc to load the new configuration
- [x] 2.2 Run echo $CLAUDE_CONFIG_DIR to verify the variable is set
- [x] 2.3 Confirm the output shows the correct path: /home/percy/.config/opencode
