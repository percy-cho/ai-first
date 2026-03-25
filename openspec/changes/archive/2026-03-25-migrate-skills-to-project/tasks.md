## 1. 准备工作

- [x] 1.1 检查用户级 skills 目录中需要移动的内容
- [x] 1.2 创建项目级 `.agents/skills/` 目录

## 2. 执行技能迁移（用户级 → 项目级）

- [x] 2.1 移动 `docx` skill 到项目 `.agents/skills/`
- [x] 2.2 移动 `interview-prep-generator` skill 到项目 `.agents/skills/`
- [x] 2.3 移动 `pdf` skill 到项目 `.agents/skills/`
- [x] 2.4 移动 `pptx` skill 到项目 `.agents/skills/`
- [x] 2.5 移动 `tailored-resume-generator` skill 到项目 `.agents/skills/`

## 3. 执行技能迁移（项目级 → 用户级）

- [x] 3.1 移动 `brainstorming` skill 到用户级 `~/.agents/skills/`

## 4. 验证结果

- [x] 4.1 验证用户级目录包含 6 个核心 skills
- [x] 4.2 验证项目目录 `.agents/skills/` 包含 5 个文档处理 skills
- [x] 4.3 运行 `npx skills list` 确认项目级 skills
