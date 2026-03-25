#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_sessions.py — 扫描本机所有 AI 智能体记录，解析对话内容为结构化 JSON。

数据源:
  - Claude Code:  ~/.claude/projects/*/*.jsonl, ~/.claude.json, ~/.claude/history.jsonl
  - OpenCode:     ~/.claude/transcripts/*.jsonl
  - Copilot:      ~/.copilot/session-state/*/events.jsonl
  - Codemaker:    ~/.codemaker/log/*.log (摘要信息)
  - GitNexus:     ~/.gitnexus/registry.json

用法:
  python parse_sessions.py --start-date 2026-02-01 --end-date 2026-03-15 --output out.json
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime, date
from collections import defaultdict

HOME = Path(os.path.expanduser("~"))


def parse_args():
    p = argparse.ArgumentParser(description="解析 AI 智能体 session 记录")
    p.add_argument("--start-date", required=True, help="起始日期 YYYY-MM-DD")
    p.add_argument("--end-date", default=date.today().isoformat(), help="结束日期 YYYY-MM-DD")
    p.add_argument("--output", default="parsed_sessions.json", help="输出文件路径")
    return p.parse_args()


def in_date_range(ts_str, start, end):
    """判断 ISO timestamp 是否在日期范围内。"""
    if not ts_str:
        return True  # 无时间戳的保留
    try:
        d = ts_str[:10]
        return start <= d <= end
    except Exception:
        return True


def safe_json_lines(filepath):
    """从 JSONL 文件逐行解析 JSON 对象。"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass


def extract_text(content):
    """从各种 content 格式中提取纯文本。"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, dict):
                if c.get("type") == "text":
                    parts.append(c.get("text", ""))
                elif c.get("type") == "tool_use":
                    parts.append(f"[Tool: {c.get('name', '')}]")
            elif isinstance(c, str):
                parts.append(c)
        return " ".join(parts)
    return str(content) if content else ""


def truncate(text, max_len=800):
    text = text.replace("\n", " ").strip()
    return text[:max_len] + "..." if len(text) > max_len else text


# ── Claude Code Sessions ─────────────────────────────────────
def parse_claude_sessions(start, end):
    results = []
    projects_dir = HOME / ".claude" / "projects"
    if not projects_dir.exists():
        return results

    for proj_dir in sorted(projects_dir.iterdir()):
        if not proj_dir.is_dir():
            continue
        for jsonl_file in sorted(proj_dir.glob("*.jsonl")):
            messages, first_ts, last_ts = [], None, None
            for obj in safe_json_lines(jsonl_file):
                ts = obj.get("timestamp", "")
                if ts:
                    if not first_ts:
                        first_ts = ts
                    last_ts = ts
                if obj.get("type") == "user":
                    if obj.get("isMeta"):
                        continue
                    content = extract_text(obj.get("message", {}).get("content", ""))
                    if "<command-name>" in content:
                        m = re.search(r"<command-name>(.*?)</command-name>", content)
                        messages.append({"role": "user", "content": f"[CMD] {m.group(1) if m else ''}"})
                        continue
                    if "<local-command-" in content:
                        continue
                    if content.strip():
                        messages.append({"role": "user", "content": content})
                elif obj.get("type") == "assistant":
                    content = extract_text(obj.get("message", {}).get("content", ""))
                    if content.strip():
                        messages.append({"role": "assistant", "content": content})

            if messages and in_date_range(first_ts, start, end):
                results.append({
                    "project": proj_dir.name,
                    "session_id": jsonl_file.stem,
                    "first_ts": first_ts,
                    "last_ts": last_ts,
                    "total_messages": len(messages),
                    "conversations": [
                        {"role": m["role"], "content": truncate(m["content"])}
                        for m in messages if m["role"] in ("user", "assistant")
                    ][:60],
                })
    return results


# ── OpenCode Transcripts ─────────────────────────────────────
def parse_opencode_transcripts(start, end):
    results = []
    tdir = HOME / ".claude" / "transcripts"
    if not tdir.exists():
        return results

    for f in sorted(tdir.glob("*.jsonl")):
        messages, first_ts, last_ts = [], None, None
        fsize = f.stat().st_size
        for obj in safe_json_lines(f):
            ts = obj.get("timestamp", "")
            if ts:
                if not first_ts:
                    first_ts = ts
                last_ts = ts
            t = obj.get("type", "")
            if t == "user":
                c = obj.get("content", "")
                if isinstance(c, str) and c.strip() and not c.startswith("[SYSTEM"):
                    messages.append({"role": "user", "content": c})
            elif t in ("assistant", "text"):
                c = obj.get("content", "")
                if isinstance(c, str) and c.strip():
                    messages.append({"role": "assistant", "content": c})
            elif t == "tool_use":
                messages.append({"role": "tool", "content": f"[Tool: {obj.get('tool_name', '')}]"})

        user_msgs = [m for m in messages if m["role"] == "user"]
        if user_msgs and in_date_range(first_ts, start, end):
            results.append({
                "session_id": f.stem,
                "first_ts": first_ts,
                "last_ts": last_ts,
                "total_messages": len(messages),
                "user_messages": len(user_msgs),
                "file_size_kb": round(fsize / 1024, 1),
                "conversations": [
                    {"role": m["role"], "content": truncate(m["content"])}
                    for m in messages if m["role"] in ("user", "assistant")
                ][:40],
            })
    return results


# ── Copilot Sessions ─────────────────────────────────────────
def parse_copilot_sessions(start, end):
    results = []
    sdir = HOME / ".copilot" / "session-state"
    if not sdir.exists():
        return results

    for sess_dir in sorted(sdir.iterdir()):
        if not sess_dir.is_dir():
            continue
        evts = sess_dir / "events.jsonl"
        if not evts.exists():
            continue

        messages, first_ts, last_ts = [], None, None
        info = {"session_id": sess_dir.name, "cwd": "", "repo": "", "model": ""}
        total_in, total_out = 0, 0

        for obj in safe_json_lines(evts):
            ts = obj.get("timestamp", "")
            if ts:
                if not first_ts:
                    first_ts = ts
                last_ts = ts
            t, d = obj.get("type", ""), obj.get("data", {})
            if t == "session.start":
                info["model"] = d.get("selectedModel", "")
                ctx = d.get("context", {})
                info["cwd"] = ctx.get("cwd", "")
                info["repo"] = ctx.get("repository", "")
            elif t == "user.message":
                c = d.get("content", "")
                if c.strip():
                    messages.append({"role": "user", "content": c})
            elif t == "assistant.message":
                c = d.get("content", "")
                if c.strip():
                    messages.append({"role": "assistant", "content": c})
                for tool in d.get("toolRequests", []):
                    args_s = json.dumps(tool.get("arguments", {}), ensure_ascii=False)[:100]
                    messages.append({"role": "tool", "content": f"[Tool: {tool.get('name','')}({args_s})]"})
            elif t == "session.shutdown":
                for _, v in d.get("modelMetrics", {}).items():
                    u = v.get("usage", {})
                    total_in += u.get("inputTokens", 0)
                    total_out += u.get("outputTokens", 0)

        if messages and in_date_range(first_ts, start, end):
            info.update({
                "first_ts": first_ts, "last_ts": last_ts,
                "total_messages": len(messages),
                "input_tokens": total_in, "output_tokens": total_out,
                "conversations": [
                    {"role": m["role"], "content": truncate(m["content"])}
                    for m in messages
                ][:30],
            })
            results.append(info)
    return results


# ── Claude Code Global Stats ─────────────────────────────────
def parse_claude_global():
    fp = HOME / ".claude.json"
    if not fp.exists():
        return {}
    try:
        with open(fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        return {
            "first_start": d.get("firstStartTime", ""),
            "num_startups": d.get("numStartups", 0),
            "version": d.get("lastReleaseNotesSeen", ""),
            "tool_usage": {k: v.get("usageCount", 0) for k, v in d.get("toolUsage", {}).items()},
            "skill_usage": {k: v.get("usageCount", 0) for k, v in d.get("skillUsage", {}).items()},
            "projects": list(d.get("projects", {}).keys()),
        }
    except Exception:
        return {}


# ── OpenCode Config ──────────────────────────────────────────
def parse_opencode_config():
    fp = HOME / ".config" / "opencode" / "oh-my-opencode.json"
    if not fp.exists():
        return {}
    try:
        with open(fp, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# ── GitNexus Registry ────────────────────────────────────────
def parse_gitnexus():
    fp = HOME / ".gitnexus" / "registry.json"
    if not fp.exists():
        return []
    try:
        with open(fp, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


# ── OpenCode Skills ──────────────────────────────────────────
def list_opencode_skills():
    skills = []
    for d in [HOME / ".config" / "opencode" / "skills", HOME / ".config" / "opencode" / "skill"]:
        if d.exists():
            for s in sorted(d.iterdir()):
                if s.is_dir() or s.is_symlink():
                    skills.append(s.name)
    return skills


# ── Codemaker Summary ────────────────────────────────────────
def parse_codemaker_summary():
    info = {"log_files": [], "proxy_dates": [], "total_log_size_mb": 0}
    log_dir = HOME / ".codemaker" / "log"
    if log_dir.exists():
        total = 0
        for f in log_dir.iterdir():
            if f.is_file():
                total += f.stat().st_size
                info["log_files"].append(f.name)
        info["total_log_size_mb"] = round(total / (1024 * 1024), 1)
    proxy_dir = HOME / ".codemaker" / "logs"
    if proxy_dir.exists():
        for f in sorted(proxy_dir.glob("proxy_2*.log")):
            m = re.search(r"proxy_(\d{8})\.log", f.name)
            if m:
                ds = m.group(1)
                info["proxy_dates"].append(f"{ds[:4]}-{ds[4:6]}-{ds[6:]}")
    return info


# ── Main ─────────────────────────────────────────────────────
def main():
    args = parse_args()
    start, end = args.start_date, args.end_date
    print(f"扫描时间范围: {start} ~ {end}")

    print("  解析 Claude Code sessions...")
    claude = parse_claude_sessions(start, end)
    print(f"    → {len(claude)} sessions")

    print("  解析 OpenCode transcripts...")
    opencode = parse_opencode_transcripts(start, end)
    print(f"    → {len(opencode)} sessions")

    print("  解析 Copilot sessions...")
    copilot = parse_copilot_sessions(start, end)
    print(f"    → {len(copilot)} sessions")

    print("  收集全局统计...")
    claude_global = parse_claude_global()
    opencode_config = parse_opencode_config()
    gitnexus = parse_gitnexus()
    opencode_skills = list_opencode_skills()
    codemaker = parse_codemaker_summary()

    output = {
        "meta": {"start_date": start, "end_date": end, "generated_at": datetime.now().isoformat()},
        "claude_code": claude,
        "opencode": opencode,
        "copilot": copilot,
        "claude_global": claude_global,
        "opencode_config": opencode_config,
        "gitnexus": gitnexus,
        "opencode_skills": opencode_skills,
        "codemaker": codemaker,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    total = len(claude) + len(opencode) + len(copilot)
    print(f"\n完成! 共 {total} 个 session → {out_path} ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
