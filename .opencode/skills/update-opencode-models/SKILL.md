---
name: update-opencode-models
description: 优化和更新 oh-my-opencode.json 中的 AI 模型配置。当用户提到"更新模型配置"、"优化模型"、"换模型"、"模型太慢了"、"切换到最新模型"、"优化opencode配置"、"oh-my-opencode.json"、"opencode models"、"agent模型分配"或"模型性价比优化"时，必须使用此技能。即使没有明确说"更新"，只要涉及到模型配置的变更或查询，也要触发此技能。
---

# 更新 Oh-My-OpenCode 模型配置

根据官方文档的推荐规则，自动为 `oh-my-opencode.json` 中的每个 agent 和 category 分配最合适的可用模型。

## 配置文件路径
- 默认（项目级）：`.opencode/oh-my-opencode.json`
- 备选（用户级）：`~/.config/opencode/oh-my-opencode.json`

## 执行流程

### Phase 1：收集信息

**1. 获取已认证提供商及可用模型**
```bash
opencode auth list  # 获取已认证提供商（如 github-copilot, opencode-go）
opencode models     # 获取全部模型列表
```

**2. 筛选模型候选池**
从 `opencode models` 结果中筛选，必须同时满足：
- 提供商必须在 `opencode auth list` 中，排除免费模型
- 排除不可用/禁用系列：`claude-*`（网络受限）、`deepseek-*`、`qwen*`

**3. 获取官方匹配规则**
抓取唯一依据文档（若失败则终止，不要使用其他来源）：
```bash
curl -sL https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/dev/docs/guide/agent-model-matching.md
```

### Phase 2：模型分配策略

对配置中的每个 agent/category 执行：
1. 在官方 guide 中查找该槽位的 fallback chain（降级链）。
2. 在候选池中选择顺序最靠前的可用模型。
   - **特殊约束**：对于 `deep` category，**禁止分配** `codex` 系列模型（例如 `gpt-5.3-codex`），需在降级链中跳过并选择下一个。
3. 若无匹配或 guide 无此槽位，则标记为“无法自动匹配”，并在最终向用户确认时请用户手动指定。

### Phase 3：应用与验证

**1. 向用户展示变更摘要**
以表格展示：
```text
### Agents / Categories
| 名称 | 当前模型 | → 新模型 | variant | 依据（guide条目） |
```
*(注：未变更项标注 ✅)*

**2. 征求确认与应用**
询问用户是否同意或需要微调。确认后，使用 `Read` 和 `Edit`（或 `Write`）工具更新 `oh-my-opencode.json`：
- 仅更新 `agents` 和 `categories` 下的 `model` 和必要的 `variant`
- `variant` 仅在官方 guide 明确要求时添加
- **严禁**修改其他字段（如 `experimental`、`background_task`）和注释

**3. 语法与合法性验证**
修改完成后再次使用 `Read` 检查文件，确保 JSON(C) 格式合法且结构未被破坏。
同时，**验证所有分配的模型**：检查文件中每一个更新后的 `model` 值，确保其均在最初获取模型候选池内，以保证分配的模型实际合法且可用。
