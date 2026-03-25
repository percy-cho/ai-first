## Why

当前用户级 skills 目录包含过多的文档处理类 skills（docx, pdf, pptx 等），这些 skills 并非所有项目都需要。为了更好地管理项目特定的工具依赖，将文档处理相关的 skills 迁移到当前项目目录，使技能管理更加模块化和按需加载。

## What Changes

- **移动技能到项目级**: 将以下 5 个 skills 从 `~/.agents/skills/` (用户级) 移动到项目 `.agents/skills/` (项目级):
  - `docx` - Word 文档操作
  - `interview-prep-generator` - 面试准备生成器  
  - `pdf` - PDF 文件处理
  - `pptx` - 演示文稿处理
  - `tailored-resume-generator` - 定制简历生成器

- **移动技能到用户级**: 将 `brainstorming` skill 从项目 `.agents/skills/` 移动到 `~/.agents/skills/` (用户级)，作为通用工具使用

- **保留核心技能**: 以下 6 个 skills 保留在用户级目录:
  - `brainstorming` - 头脑风暴工具
  - `codebase-study-guide` - 代码库学习指南
  - `find-skills` - 发现和安装 skill
  - `mcp-builder` - MCP 服务器构建
  - `skill-creator` - 创建新 skills
  - `skill-vetter` - Skill 安全检查

## Capabilities

### New Capabilities

<!-- 这是一个技能重组改动，不涉及新功能能力 -->

### Modified Capabilities

<!-- 这是一个技能重组改动，不涉及现有能力修改 -->

## Impact

- **技能加载**: 文档处理 skills 现在仅在当前项目中可用；brainstorming 现在全局可用
- **用户级目录**: 从 10 个 skills 减少到 6 个核心 skills，更加精简
- **项目目录**: 创建项目级 `.agents/skills/`，包含 5 个文档处理 skills
- **无代码变更**: 纯文件移动操作，不影响现有功能
