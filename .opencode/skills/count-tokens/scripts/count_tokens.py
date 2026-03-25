#!/usr/bin/env python
"""
count_tokens.py — 精确计算文件或文本的 token 数量

支持多种 tokenizer：
  - cl100k_base  (GPT-4, GPT-3.5-turbo, Claude 等主流模型)
  - o200k_base   (GPT-4o, o1 系列)
  - p50k_base    (text-davinci-003 等旧版 GPT-3)

用法：
  python count_tokens.py <文件路径> [--encoding cl100k_base]
  python count_tokens.py --text "直接统计这段文字"
  python count_tokens.py <文件路径> --all   # 同时输出所有 encoding 的结果

依赖：
  pip install tiktoken
"""

import sys
import argparse
import os

# Windows 终端强制 UTF-8 输出，避免中文乱码
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def ensure_tiktoken():
    try:
        import tiktoken
        return tiktoken
    except ImportError:
        print("[!] 未安装 tiktoken，正在安装...", flush=True)
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tiktoken", "-q"])
        import tiktoken
        return tiktoken


def count_tokens(text: str, encoding_name: str) -> int:
    tiktoken = ensure_tiktoken()
    enc = tiktoken.get_encoding(encoding_name)
    return len(enc.encode(text))


def format_size(n_bytes: int) -> str:
    if n_bytes < 1024:
        return f"{n_bytes} B"
    elif n_bytes < 1024 ** 2:
        return f"{n_bytes / 1024:.1f} KB"
    else:
        return f"{n_bytes / 1024 ** 2:.2f} MB"


def analyze(text: str, encoding_name: str, label: str = ""):
    n_chars = len(text)
    n_bytes = len(text.encode("utf-8"))
    n_tokens = count_tokens(text, encoding_name)
    ratio = n_chars / n_tokens if n_tokens > 0 else 0

    print(f"\n{'─' * 50}")
    if label:
        print(f"  来源     : {label}")
    print(f"  Encoding : {encoding_name}")
    print(f"  字符数    : {n_chars:,}")
    print(f"  字节数    : {format_size(n_bytes)}")
    print(f"  Token 数  : {n_tokens:,}")
    print(f"  字符/Token: {ratio:.2f}")
    print(f"{'─' * 50}")
    return n_tokens


def main():
    parser = argparse.ArgumentParser(
        description="精确计算文件或文本的 token 数",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("file", nargs="?", help="要统计的文件路径")
    parser.add_argument("--text", "-t", help="直接传入文本内容进行统计")
    parser.add_argument(
        "--encoding", "-e",
        default="cl100k_base",
        choices=["cl100k_base", "o200k_base", "p50k_base"],
        help="Tokenizer encoding（默认：cl100k_base）",
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        dest="show_all",
        help="同时显示所有 encoding 的结果",
    )

    args = parser.parse_args()

    # 获取文本内容
    if args.text:
        text = args.text
        label = "(命令行输入)"
    elif args.file:
        path = args.file
        if not os.path.isfile(path):
            print(f"[错误] 文件不存在: {path}", file=sys.stderr)
            sys.exit(1)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        label = path
    else:
        # 从 stdin 读取
        print("[提示] 未指定文件，从 stdin 读取（Ctrl+Z/Ctrl+D 结束）...")
        text = sys.stdin.read()
        label = "(stdin)"

    # 输出统计
    if args.show_all:
        for enc_name in ["cl100k_base", "o200k_base", "p50k_base"]:
            analyze(text, enc_name, label)
    else:
        analyze(text, args.encoding, label)


if __name__ == "__main__":
    main()
