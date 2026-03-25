## Context

oh-my-opencode 插件需要 CLAUDE_CONFIG_DIR 环境变量来定位其配置目录。当前系统未设置此变量，导致插件初始化时无法找到配置位置。

**当前状态**:
- `~/.bashrc` 已存在，包含用户现有的 shell 配置
- CLAUDE_CONFIG_DIR 环境变量未定义
- 目标目录 `~/.config/opencode` 已存在（包含 OpenCode 配置）

**约束**:
- 修改必须兼容 bash shell
- 使用 `$HOME` 变量而非硬编码路径，确保跨用户可移植性
- 配置应放在文件末尾，保持与现有配置分离

## Goals / Non-Goals

**Goals:**
- 在 `~/.bashrc` 中永久添加 CLAUDE_CONFIG_DIR 环境变量配置
- 确保所有新启动的 bash 会话自动加载该变量
- 使用 `$HOME/.config/opencode` 作为配置目录

**Non-Goals:**
- 不支持其他 shell（zsh、fish 等）
- 不修改现有 bash 配置的其他部分
- 不处理配置文件权限问题

## Decisions

### 使用 export 命令
**选择**: `export CLAUDE_CONFIG_DIR="$HOME/.config/opencode"`
**理由**: export 使变量在当前 shell 及其子进程中可用，是环境变量的标准设置方式
**替代方案**: 不使用 export 直接赋值 - 拒绝，因为只设置 shell 变量而非环境变量

### 放在文件末尾
**选择**: 将配置行添加到 `~/.bashrc` 末尾
**理由**: 
- 避免干扰现有配置
- 便于后续维护和识别
- 与现有 Python alias 配置放在一起
**替代方案**: 添加到文件开头 - 拒绝，因为可能被后续配置覆盖

### 使用 $HOME 而非 ~
**选择**: `"$HOME/.config/opencode"`
**理由**: $HOME 在双引号中正确解析，而 ~ 在某些上下文中不会展开
**替代方案**: 硬编码完整路径 `/home/percy/.config/opencode` - 拒绝，因为缺乏可移植性

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| 用户切换 shell 类型 | 文档说明当前仅配置 bash；如需其他 shell 需单独配置 |
| ~/.config/opencode 目录不存在 | 由 OpenCode 在安装时创建，此配置假定目录已存在 |
| 现有终端未加载新变量 | 文档说明需要 source ~/.bashrc 或重新打开终端 |

## Migration Plan

**部署步骤**:
1. 编辑 `~/.bashrc` 文件
2. 在文件末尾添加环境变量配置行
3. 保存文件

**验证**:
1. 运行 `source ~/.bashrc` 重新加载配置
2. 运行 `echo $CLAUDE_CONFIG_DIR` 验证变量已设置
3. 预期输出: `/home/percy/.config/opencode`

**回滚**:
- 编辑 `~/.bashrc`，删除添加的配置行
- 重新加载配置或打开新终端
