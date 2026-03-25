## Context

当前项目的 skills 管理存在以下情况：

- **用户级 skills** (`~/.agents/skills/`): 包含 10 个 skills，其中 5 个是文档处理类（docx, pdf, pptx, interview-prep-generator, tailored-resume-generator）
- **项目级 skills**: 无项目级 `.agents/skills/` 目录

这些文档处理 skills 并非所有项目都需要，放在用户级目录会导致不必要的全局加载。同时 `brainstorming` 作为通用工具应在用户级可用。

## Goals / Non-Goals

**Goals:**
- 将文档处理相关的 5 个 skills 从用户级目录移动到项目级 `.agents/skills/` 目录
- 将 `brainstorming` skill 从项目级移动到用户级目录
- 保持核心开发/管理 skills 在用户级目录
- 实现技能的按需可用，避免全局污染

**Non-Goals:**
- 不修改任何 skill 的代码或功能
- 不创建新的 skills
- 不涉及技能版本升级或功能增强

## Decisions

### 1. 技能分类标准

**保留在用户级目录的技能**（通用开发工具）：
- `brainstorming`: 头脑风暴工具
- `codebase-study-guide`: 代码库学习工具
- `find-skills`: 技能发现和管理
- `mcp-builder`: MCP 服务器开发
- `skill-creator`: 技能创建工具
- `skill-vetter`: 技能安全检查

**移动到项目级目录的技能**（文档处理专用）：
- `docx`: Word 文档处理
- `interview-prep-generator`: 面试准备
- `pdf`: PDF 处理
- `pptx`: 演示文稿处理
- `tailored-resume-generator`: 简历生成

**理由**: 文档处理类技能的使用场景与具体项目强相关，而开发工具类技能（包括 brainstorming）具有通用性，应在用户级可用。

### 2. 迁移方式

选择直接使用 `mv` 命令移动文件，而非复制后删除。

**理由**: 这是纯粹的重组织操作，不需要保留原位置的备份。

### 3. 目录结构

项目级 skills 使用 `.agents/skills/` 而非 `.opencode/skills/`，以便使用 `npx skills` 统一管理。

**理由**: `npx skills` 默认扫描 `.agents/skills/` 目录，便于后续管理。

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| 其他项目依赖这些用户级 skills | 其他项目如需使用，需要单独安装到项目目录 |
| 移动后 skill 链接可能丢失 | 检查 skills 状态，必要时重新链接 |

**Trade-offs**:
- **优点**: 用户级目录更精简，核心工具全局可用；文档处理技能按需加载
- **缺点**: 其他项目如需使用文档处理 skills 需要单独配置

## Migration Plan

迁移步骤（已执行）：

1. **创建项目级目录**: 创建 `.agents/skills/` 目录
2. **移动文档处理 skills**: 使用 `mv` 命令将 5 个 skills 从 `~/.agents/skills/` 移动到项目 `.agents/skills/`
3. **移动 brainstorming**: 将 `brainstorming` 从项目 `.agents/skills/` 移动到 `~/.agents/skills/`
4. **验证结果**: 
   - 用户级目录剩余 6 个核心 skills
   - 项目目录 `.agents/skills/` 包含 5 个文档处理 skills

**Rollback**: 如需回滚，将项目 `.agents/skills/` 中的对应技能目录移回 `~/.agents/skills/`
