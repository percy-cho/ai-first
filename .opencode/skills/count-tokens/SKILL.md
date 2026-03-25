---
name: count-tokens
description: 精确计算文件或文本内容占用的 token 数量，使用 tiktoken 库支持 cl100k_base（GPT-4/Claude）、o200k_base（GPT-4o/o1）等主流 tokenizer。当用户说"统计token"、"计算token数"、"这个文件多少token"、"token占用"、"count tokens"、"token消耗"、"上下文窗口占用"时使用。
---

# count-tokens — Token 精确计数

使用 [tiktoken](https://github.com/openai/tiktoken) 对文件或文本进行精确 token 计数，同时输出字符数、字节数和字符/token 比率。

## 核心脚本

`scripts/count_tokens.py` — 依赖 `tiktoken`，会在首次运行时自动安装。

## 用法

### 1. 统计单个文件

```bash
python <skill-scripts-dir>/count_tokens.py <文件路径>
```

示例：
```bash
python .claude/skills/count-tokens/scripts/count_tokens.py C:\Users\me\.config\opencode\Agents.md
```

### 2. 直接统计文本

```bash
python <skill-scripts-dir>/count_tokens.py --text "需要统计的文字内容"
```

### 3. 指定 tokenizer encoding

```bash
python <skill-scripts-dir>/count_tokens.py <文件> --encoding o200k_base
```

| Encoding | 适用模型 |
|---|---|
| `cl100k_base`（默认）| GPT-4、GPT-3.5-turbo、Claude 系列 |
| `o200k_base` | GPT-4o、o1 系列 |
| `p50k_base` | text-davinci-003 等旧版 GPT-3 |

### 4. 同时输出所有 encoding 的结果

```bash
python <skill-scripts-dir>/count_tokens.py <文件> --all
```

## 输出示例

```
──────────────────────────────────────────────────
  来源     : C:\Users\me\Agents.md
  Encoding : cl100k_base
  字符数    : 583
  字节数    : 744 B
  Token 数  : 371
  字符/Token: 1.57
──────────────────────────────────────────────────
```

## 使用流程

1. 用户询问某文件/文本占多少 token
2. 用 Bash 工具调用脚本（**Windows 下需设置 `PYTHONIOENCODING=utf-8`**）：
   ```bash
   # Windows（推荐写法，避免中文乱码）
   python -c "
   import subprocess, sys, os
   env = {**os.environ, 'PYTHONIOENCODING': 'utf-8'}
   r = subprocess.run([sys.executable, r'<skill-scripts-dir>/count_tokens.py', r'<文件路径>'], capture_output=True, env=env)
   print(r.stdout.decode('utf-8'))
   "
   ```
   或者直接在 Bash 工具里用 Python 调用 `count_tokens` 函数（见下方）。
3. 将统计结果直接告知用户（Token 数、字符数、编码类型）

### 最简内联用法（无需脚本文件）

当只需要快速统计时，可直接内联运行：

```python
# 在 Bash 工具中执行
import tiktoken
text = open(r"<文件路径>", encoding="utf-8", errors="replace").read()
enc = tiktoken.get_encoding("cl100k_base")
tokens = len(enc.encode(text))
print(f"Token 数: {tokens:,}  字符数: {len(text):,}")
```

## 依赖

| 包 | 安装命令 |
|---|---|
| `tiktoken` | `pip install tiktoken`（脚本首次运行时自动安装）|

## 注意事项

- 脚本默认使用 `cl100k_base`，与 GPT-4 / Claude 系列一致
- 中文字符 token 效率较低，通常 1 汉字 ≈ 1–2 tokens
- 如文件为非 UTF-8 编码，脚本以 `errors='replace'` 容错读取
- 可对 stdin 输入进行统计（不传任何参数时等待 stdin）
