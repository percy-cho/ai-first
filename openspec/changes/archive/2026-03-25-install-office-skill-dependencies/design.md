## Context

.agents/skills 目录下包含四个 Office 相关 skill：
- **docx** - Word 文档处理
- **pdf** - PDF 处理
- **pptx** - PowerPoint 处理
- **xlsx** - Excel 处理

这些 skill 依赖外部工具才能正常工作。当前环境缺少这些依赖，需要一次性安装所有必需的工具。

### 当前状态
- 系统基础环境已配置（Debian 12, Python 3.11, Node.js 20）
- OpenCode 框架已初始化
- 四个 Office skill 已定义但依赖未安装

### 约束
- Python 环境使用系统包管理（PEP 668），需要使用 `--break-system-packages`
- 部分系统工具需要 sudo 权限安装
- 安装顺序：系统工具 → Python 包 → Node.js 包

## Goals / Non-Goals

**Goals:**
- 安装所有 Python 依赖（9个包）
- 安装所有 Node.js 依赖（2个包）
- 安装所有系统工具（7个工具）
- 验证所有依赖安装成功

**Non-Goals:**
- 不修改任何 skill 的代码
- 不创建新的 capability
- 不改变现有项目配置

## Decisions

### 决策 1: 使用 `--break-system-packages` 安装 Python 包
**原因**: 环境使用系统 Python，PEP 668 阻止直接安装。该环境是隔离的 AI-first workspace，使用系统包不会破坏其他项目。

**替代方案考虑**: 创建虚拟环境
- 被拒绝：增加复杂性，OpenCode 默认使用系统 Python

### 决策 2: 全局安装 Node.js 包
**原因**: docx 和 pptxgenjs 是 CLI 工具，需要全局访问。使用 `-g` 标志安装到用户目录。

### 决策 3: 批量安装系统工具
**原因**: 使用 `apt install` 一次性安装所有系统工具，减少交互次数。接受 sudo 权限要求。

## Risks / Trade-offs

| Risk | 影响 | 缓解措施 |
|------|------|----------|
| 磁盘空间不足 | 高 | LibreOffice 约 300MB，Python 包约 200MB。确保 1GB+ 可用空间 |
| 网络下载失败 | 中 | 使用国内镜像或重试机制。apt 和 pip 都支持缓存 |
| 权限不足 | 中 | 部分工具需要 sudo。如无权限则跳过，记录缺失项 |
| 版本冲突 | 低 | 使用版本锁定或检查现有版本。当前环境是干净的 |

## Migration Plan

无需迁移，此 change 仅安装新依赖。

## Open Questions

无
