## Why

oh-my-opencode 插件依赖 CLAUDE_CONFIG_DIR 环境变量来定位配置目录。当前该环境变量未设置，导致插件无法正常工作。需要将 CLAUDE_CONFIG_DIR 永久配置到 shell 配置文件中，确保每次新终端会话都能正确加载。

## What Changes

- 在 `~/.bashrc` 文件末尾添加环境变量配置行
- 设置 `CLAUDE_CONFIG_DIR="$HOME/.config/opencode"`
- 使用 `$HOME` 变量确保路径在不同用户环境下正确解析

## Capabilities

### New Capabilities
- `env-var-config`: 配置 CLAUDE_CONFIG_DIR 环境变量到 bash shell 配置文件

### Modified Capabilities
<!-- 无现有 spec 需要修改 -->

## Impact

- 受影响文件：`~/.bashrc`
- 依赖：bash shell 环境
- 系统影响：所有新打开的 bash 终端会话将自动加载该环境变量
