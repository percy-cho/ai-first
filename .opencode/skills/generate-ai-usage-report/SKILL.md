---
name: generate-ai-usage-report
description: 生成AI使用报告 — 扫描本机所有 AI 智能体记录（Codemaker、OpenCode、Claude Code、Copilot），解析对话内容，输出结构化 AI 实践汇报 Markdown 文档。当用户说"生成AI使用报告"、"生成AI报告"、"AI使用汇报"、"generate ai report"、"生成AI汇报文档"、"导出AI使用记录"时使用。
---

# 生成 AI 使用汇报文档

扫描本机所有 AI 智能体使用记录，解析对话内容，自动生成结构化的 AI 实践汇报文档（Markdown）。

## 前提条件

- Python 可用（Conda / 系统 Python 均可）
- 本 Skill 的 `scripts/` 目录下有 `parse_sessions.py` 和 `generate_report.py`

---

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<START_DATE>` | 起始日期（含），格式 `YYYY-MM-DD` | 无，必填 |
| `<END_DATE>` | 结束日期（含），格式 `YYYY-MM-DD` | 当天 |
| `<OUTPUT_DIR>` | 输出目录 | `D:\ai\tmp` |
| `<AUTHOR>` | 报告人姓名 | 从系统用户名推断 |
| `<PROJECT_CONTEXT>` | 项目背景描述（可选） | 空 |

---

## 执行流程

### Phase 1：环境探测

1. 找到可用的 Python 解释器：

```bash
# 优先级：conda python > python3 > python
/c/ProgramData/miniconda3/python --version 2>/dev/null || python3 --version 2>/dev/null || python --version 2>/dev/null
```

2. 记录本 Skill 脚本目录的绝对路径（`<SKILL_DIR>/scripts/`）。

3. 确认输出目录存在，不存在则创建：

```bash
mkdir -p <OUTPUT_DIR>
```

---

### Phase 2：数据采集 — 运行 parse_sessions.py

执行解析脚本，扫描 `~` 目录下所有 AI 智能体记录：

```bash
<PYTHON> <SKILL_DIR>/scripts/parse_sessions.py \
  --start-date <START_DATE> \
  --end-date <END_DATE> \
  --output <OUTPUT_DIR>/parsed_sessions.json
```

脚本会扫描以下数据源：

| 数据源 | 路径 | 内容 |
|--------|------|------|
| Claude Code 项目 Sessions | `~/.claude/projects/*/*.jsonl` | 完整对话（user/assistant/tool） |
| Claude Code 命令历史 | `~/.claude/history.jsonl` | 用户输入命令 |
| Claude Code 全局配置 | `~/.claude.json` | 工具使用统计、Skill 使用统计 |
| OpenCode Transcripts | `~/.claude/transcripts/*.jsonl` | Session 对话记录 |
| OpenCode 配置 | `~/.config/opencode/oh-my-opencode.json` | 模型配置 |
| OpenCode Skills | `~/.config/opencode/skills/` | 已安装 Skill 清单 |
| Copilot Sessions | `~/.copilot/session-state/*/events.jsonl` | 事件流 |
| Copilot IDE Locks | `~/.copilot/ide/*.lock` | IDE 工作区记录 |
| Codemaker Extension Log | `~/.codemaker/log/codemaker_extension.log*` | 插件日志 |
| Codemaker Proxy Log | `~/.codemaker/logs/proxy_*.log` | API 调用日志 |
| Codemaker Plugin Log | `~/.codemaker/pluginLog/rd/codemaker.log*` | Rider 插件日志 |
| GitNexus Registry | `~/.gitnexus/registry.json` | 已索引仓库 |

**输出**: `<OUTPUT_DIR>/parsed_sessions.json`（结构化 JSON，含所有工具的对话摘要）

---

### Phase 3：内容分析

读取 `parsed_sessions.json`，人工（AI）分析以下维度：

#### 3.1 使用场景分类

遍历所有 session 的用户首条消息，按以下主题分类：

| 主题类别 | 关键词 |
|----------|--------|
| 代码理解/分析 | 源码、阅读、分析、理解、what does、how does |
| 文档生成 | wiki、文档、spec、生成文档、总结、report |
| Skill/技能开发 | skill、技能、create skill、生成 skill |
| 工具配置 | 配置、权限、settings、config、模型 |
| Bug 排查 | bug、报错、修复、为什么、卡住、crash |
| 代码生成/修改 | 编写、生成代码、修改、重构、实现 |
| 知识检索 | 查找、搜索、怎么用、如何 |
| 编译/构建 | 编译、build、compile |

#### 3.2 成果提取

从对话中识别以下类型的成果物：
- **生成的文档**: assistant 消息中包含 Write/Edit 工具调用，输出 `.md` 文件的
- **创建的 Skill**: 输出到 `skills/` 目录的
- **解决的问题**: 用户描述问题 → assistant 给出解决方案 → 用户确认
- **配置变更**: 修改了配置文件的

#### 3.3 工具使用统计

从 `~/.claude.json` 的 `toolUsage` 和 `skillUsage` 字段提取各工具/技能的调用次数。

---

### Phase 4：生成汇报文档 — 运行 generate_report.py

```bash
<PYTHON> <SKILL_DIR>/scripts/generate_report.py \
  --input <OUTPUT_DIR>/parsed_sessions.json \
  --output <OUTPUT_DIR>/ai-practice-report.md \
  --start-date <START_DATE> \
  --end-date <END_DATE> \
  --author "<AUTHOR>" \
  --project "<PROJECT_CONTEXT>"
```

脚本生成的文档包含以下章节（参见 `references/report-template.md`）：

```
# AI 编程智能体实践报告

## 一、概述
  - 报告周期、工具矩阵、关键数据汇总表

## 二、核心应用场景
  - 每个场景：痛点 → 做法 → 典型案例 → 成效
  - 场景来自 Phase 3.1 的分类结果

## 三、方法论总结
  - 从实际使用模式中提炼的方法论
  - 工具选型策略

## 四、成效评估
  - 效率提升估算
  - 知识资产积累清单

## 五、问题与展望
  - 遇到的限制
  - 下一步计划
```

---

### Phase 5：人工审阅与补充

脚本生成的是**初稿**。AI 需要在以下方面补充人工判断：

1. **效率提升估算**: 脚本只能统计 session 数和消息数，效率倍数需要根据任务实际复杂度估算
2. **方法论提炼**: 从高频使用模式中抽象方法论（如「三步闭环」、「Skill 驱动开发」）
3. **亮点案例充实**: 选择 3-5 个最有代表性的 session，补充具体的技术细节
4. **展望**: 基于当前使用情况，给出下一步建议

**操作方式**: 读取生成的初稿，逐节审阅并用 Edit 工具补充/修改。

---

### Phase 6：输出确认

最终确认输出文件：

| 文件 | 说明 |
|------|------|
| `<OUTPUT_DIR>/ai-practice-report.md` | **主文档** — 汇报用 |
| `<OUTPUT_DIR>/parsed_sessions.json` | 中间数据 — 结构化 JSON |
| `<OUTPUT_DIR>/ai-agent-usage-records.md` | 附录（可选）— 详细原始记录 |
| `<OUTPUT_DIR>/ai-agent-conversations-detail.md` | 附录（可选）— 完整对话记录 |

---

## JSONL 格式参考

### Claude Code Session JSONL（`~/.claude/projects/*/*.jsonl`）

```jsonl
{"type":"user","message":{"role":"user","content":"..."},"uuid":"...","timestamp":"...","sessionId":"..."}
{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"..."},{"type":"tool_use","name":"Read","input":{...}}]},"uuid":"...","timestamp":"..."}
```

- `type=user` + `isMeta=true` → 系统注入消息，跳过
- `type=user` + `content` 含 `<command-name>` → 命令操作
- `type=assistant` + `content` 为数组 → 遍历取 `type=text` 的 `.text`

### OpenCode Transcript JSONL（`~/.claude/transcripts/*.jsonl`）

```jsonl
{"type":"user","timestamp":"2026-...","content":"用户输入文本"}
{"type":"assistant","timestamp":"2026-...","content":"助手回复文本"}
{"type":"tool_use","timestamp":"2026-...","tool_name":"bash","tool_input":{...}}
{"type":"tool_result","timestamp":"2026-...","tool_name":"bash","tool_output":{...}}
{"type":"text","timestamp":"2026-...","content":"助手的文本片段输出"}
```

- `type=user` → 用户消息（`content` 为字符串）
- `type=assistant` / `type=text` → 助手回复
- `type=tool_use` → 工具调用
- 按 `timestamp` 字段过滤日期范围

### Copilot Session Events JSONL（`~/.copilot/session-state/*/events.jsonl`）

```jsonl
{"type":"session.start","data":{"sessionId":"...","selectedModel":"gpt-4.1","context":{"cwd":"...","repository":"..."}},"timestamp":"..."}
{"type":"user.message","data":{"content":"用户输入"},"timestamp":"..."}
{"type":"assistant.message","data":{"content":"助手回复","toolRequests":[...],"outputTokens":42},"timestamp":"..."}
{"type":"session.shutdown","data":{"modelMetrics":{...},"codeChanges":{...}},"timestamp":"..."}
```

- `type=user.message` → `data.content` 为用户输入
- `type=assistant.message` → `data.content` 为助手回复，`data.toolRequests` 为工具调用
- `type=session.start` → `data.context` 含项目路径信息
- `type=session.shutdown` → `data.modelMetrics` 含 token 使用量

### Codemaker 日志（非 JSONL，文本格式）

```
2026-03-13 10:06:38.758 [INFO] [Codebase Chat] Globby for d:\ai\x20_gitnexus
2026-03-02 21:57:24 - codemaker-proxy - WARNING - 429 Rate limit detected...
```

- 按日期前缀 `YYYY-MM-DD` 过滤
- `[Codebase Chat]` 标记为 Chat 相关条目
- `proxy_*.log` 中 `429 Rate limit` 标记限流事件

---

## 对话主题分类规则

在 Phase 3.1 中，对每个 session 的**首条用户消息**进行关键词匹配分类：

```python
def classify(content):
    c = content.lower()
    if any(k in c for k in ['传送门', 'portal']): return '传送门/Portal'
    if any(k in c for k in ['zombie', '僵尸', 'pve', 'mode_10130']): return '僵尸/PVE模式'
    if any(k in c for k in ['hero', '英雄', '红兜帽', '格尔']): return '英雄技能分析'
    if any(k in c for k in ['wiki', '文档', '总结', '规格', 'spec', 'report']): return '文档生成'
    if any(k in c for k in ['skill', 'openspec']): return 'Skill/技能开发'
    if any(k in c for k in ['权限', 'permission', '配置', 'config', 'settings']): return '工具配置'
    if any(k in c for k in ['gitnexus', '知识图谱', 'index']): return '代码知识图谱'
    if any(k in c for k in ['mcp', 'weather', 'forecast']): return 'MCP协议'
    if any(k in c for k in ['编译', 'build', 'compile']): return '编译/构建'
    if any(k in c for k in ['bug', '报错', '修复', 'fix', '为什么']): return 'Bug排查'
    if any(k in c for k in ['unreal', 'marvel', 'ability', 'ue']): return 'UE代码分析'
    if any(k in c for k in ['模型', 'model', 'hello']): return '模型测试'
    return '其他'
```

> 这只是默认分类器。如果用户指定的 `<PROJECT_CONTEXT>` 涉及特定领域，应调整关键词列表。

---

## 使用方式

### 最简用法

```
生成 2026-02 到 2026-03 的 AI 使用汇报
```

### 完整参数

```
使用 generate-report 技能，生成 AI 使用汇报文档。
时间段: 2026-02-11 到 2026-03-15
输出目录: D:\ai\tmp
报告人: zuopanxing
项目背景: X20（网易 UE5 多人对战游戏 Marvel 项目）
```

### 仅生成原始数据（不含汇报文档）

```
使用 generate-report，只执行 Phase 1-2，解析所有 AI 对话记录到 JSON。
时间段: 2026-03-01 到 2026-03-15
```

---

## 注意事项

1. **隐私**: 解析的对话数据可能包含代码片段和项目信息，输出文件应按项目保密等级处理
2. **大文件**: OpenCode transcripts 可能有数百个文件、总计数十 MB，解析脚本已做流式处理
3. **编码**: Windows 环境下注意 UTF-8 编码，脚本内已设置 `encoding='utf-8'`
4. **时间过滤**: Session 的时间范围取首条消息的 timestamp，跨天 session 按开始时间归属
5. **增量更新**: 如需更新已有报告，重新运行全流程即可，脚本为幂等操作
