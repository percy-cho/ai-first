#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_report.py — 从 parsed_sessions.json 生成 AI 使用汇报 Markdown 初稿。

用法:
  python generate_report.py \
    --input parsed_sessions.json \
    --output ai-practice-report.md \
    --start-date 2026-02-11 --end-date 2026-03-15 \
    --author zuopanxing \
    --project "X20 UE5 项目"
"""
import argparse
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import date


def parse_args():
    p = argparse.ArgumentParser(description="生成 AI 使用汇报文档")
    p.add_argument("--input", required=True, help="parsed_sessions.json 路径")
    p.add_argument("--output", required=True, help="输出 Markdown 路径")
    p.add_argument("--start-date", required=True)
    p.add_argument("--end-date", default=date.today().isoformat())
    p.add_argument("--author", default="")
    p.add_argument("--project", default="")
    return p.parse_args()


def clean(txt, maxlen=200):
    txt = re.sub(r"\[search-mode\].*?---", "", txt, flags=re.DOTALL)
    txt = re.sub(r"\[analyze-mode\].*?---", "", txt, flags=re.DOTALL)
    txt = re.sub(r"<command-instruction>.*?</command-instruction>", "", txt, flags=re.DOTALL)
    txt = re.sub(r"<user-task>(.*?)</user-task>", r"\1", txt, flags=re.DOTALL)
    txt = re.sub(r"<ide_opened_file>.*?</ide_opened_file>", "", txt, flags=re.DOTALL)
    txt = re.sub(r"<task-notification>.*?</task-notification>", "", txt, flags=re.DOTALL)
    txt = re.sub(r"<[^>]+>", "", txt)
    txt = txt.strip()
    return txt[:maxlen] + "..." if len(txt) > maxlen else txt


def classify(content):
    c = content.lower()
    if any(k in c for k in ["传送门", "portal"]):
        return "传送门/Portal"
    if any(k in c for k in ["zombie", "僵尸", "pve", "mode_10130"]):
        return "僵尸/PVE模式"
    if any(k in c for k in ["hero", "英雄", "红兜帽", "格尔"]):
        return "英雄技能分析"
    if any(k in c for k in ["wiki", "文档", "总结", "规格", "spec", "report"]):
        return "文档生成"
    if any(k in c for k in ["skill", "openspec"]):
        return "Skill/技能开发"
    if any(k in c for k in ["权限", "permission", "配置", "config", "settings"]):
        return "工具配置"
    if any(k in c for k in ["gitnexus", "知识图谱", "index"]):
        return "代码知识图谱"
    if any(k in c for k in ["mcp", "weather", "forecast"]):
        return "MCP协议"
    if any(k in c for k in ["编译", "build", "compile"]):
        return "编译/构建"
    if any(k in c for k in ["bug", "报错", "修复", "fix", "为什么", "卡"]):
        return "Bug排查"
    if any(k in c for k in ["unreal", "marvel", "ability", "ue"]):
        return "UE代码分析"
    if any(k in c for k in ["模型", "model", "hello"]):
        return "模型测试"
    return "其他"


def main():
    args = parse_args()
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    L = []
    def w(s=""):
        L.append(s)

    meta = data.get("meta", {})
    cc = data.get("claude_code", [])
    oc = data.get("opencode", [])
    cp = data.get("copilot", [])
    cg = data.get("claude_global", {})
    oc_cfg = data.get("opencode_config", {})
    gn = data.get("gitnexus", [])
    oc_skills = data.get("opencode_skills", [])
    cm = data.get("codemaker", {})

    total_sessions = len(cc) + len(oc) + len(cp)
    cc_users = sum(len([c for c in s.get("conversations", []) if c["role"] == "user"]) for s in cc)
    oc_users = sum(s.get("user_messages", 0) for s in oc)
    cp_users = sum(len([c for c in s.get("conversations", []) if c["role"] == "user"]) for s in cp)
    total_users = cc_users + oc_users + cp_users

    # ── Header ───────────────────────────────────────────────
    w("# AI 编程智能体实践报告")
    w()
    author = args.author or "N/A"
    project = args.project or ""
    w(f"> 报告人: {author}")
    w(f"> 报告周期: {args.start_date} — {args.end_date}")
    if project:
        w(f"> 项目背景: {project}")
    w()
    w("---")
    w()

    # ── 一、概述 ─────────────────────────────────────────────
    w("## 一、概述")
    w()
    w(f"本报告总结了 **{args.start_date}** 至 **{args.end_date}** 期间 AI 编程智能体的使用情况。")
    w(f"累计产生 **{total_sessions}** 个对话 Session、**{total_users}** 条用户指令。")
    w()

    w("### 工具矩阵")
    w()
    w("| 工具 | Session 数 | 用户消息数 | 定位 |")
    w("|------|-----------|-----------|------|")
    w(f"| Claude Code | {len(cc)} | {cc_users} | 终端 AI 助手（代码分析/文档生成） |")
    w(f"| OpenCode | {len(oc)} | {oc_users} | 终端多智能体编排（oh-my-opencode） |")
    w(f"| Copilot | {len(cp)} | {cp_users} | CLI Agent（MCP 测试） |")
    codemaker_days = len(cm.get("proxy_dates", []))
    w(f"| Codemaker | (IDE 插件) | {codemaker_days} 天有代理日志 | IDE 代码补全/Codebase Chat |")
    w()

    # ── 二、对话主题分布 ─────────────────────────────────────
    w("---")
    w()
    w("## 二、对话主题分布")
    w()

    topics = defaultdict(list)
    for source, sessions in [("Claude Code", cc), ("OpenCode", oc), ("Copilot", cp)]:
        for s in sessions:
            for c in s.get("conversations", []):
                if c["role"] == "user":
                    txt = clean(c["content"], 300)
                    if len(txt) >= 5:
                        topic = classify(txt)
                        topics[topic].append({"source": source, "text": txt[:100], "ts": s.get("first_ts", "")[:10]})
                    break

    w("| 主题 | 次数 | 涉及工具 | 示例 |")
    w("|------|------|---------|------|")
    for topic, items in sorted(topics.items(), key=lambda x: -len(x[1])):
        sources = ", ".join(sorted(set(i["source"] for i in items)))
        example = items[0]["text"][:80].replace("|", "/") if items else ""
        w(f"| {topic} | {len(items)} | {sources} | {example} |")
    w()

    # ── 三、核心应用场景 ─────────────────────────────────────
    w("---")
    w()
    w("## 三、核心应用场景")
    w()
    w("> 以下场景基于对话数据自动提取，效率提升倍数和详细案例需人工补充。")
    w()

    # Group significant sessions
    big_sessions = sorted(oc, key=lambda x: x.get("file_size_kb", 0), reverse=True)[:15]
    for i, s in enumerate(big_sessions, 1):
        user_msgs = [c for c in s.get("conversations", []) if c["role"] == "user"]
        if not user_msgs:
            continue
        first_q = clean(user_msgs[0]["content"], 200)
        if len(first_q) < 10:
            continue
        topic = classify(first_q)
        w(f"### 场景 {i}: {topic}")
        w(f"- **Session**: `{s['session_id']}`")
        w(f"- **时间**: {s.get('first_ts', '')[:19]}")
        w(f"- **规模**: {s.get('file_size_kb', 0):.0f} KB, {s.get('total_messages', 0)} 条消息")
        w(f"- **用户指令**: {first_q}")
        w()

    # ── 四、工具使用统计 ─────────────────────────────────────
    w("---")
    w()
    w("## 四、工具使用统计")
    w()

    tool_usage = cg.get("tool_usage", {})
    if tool_usage:
        w("### Claude Code 工具调用")
        w()
        w("| 工具 | 调用次数 |")
        w("|------|----------|")
        for k, v in sorted(tool_usage.items(), key=lambda x: -x[1]):
            w(f"| {k} | {v} |")
        w()

    skill_usage = cg.get("skill_usage", {})
    if skill_usage:
        w("### Claude Code Skill 调用")
        w()
        w("| Skill | 调用次数 |")
        w("|-------|----------|")
        for k, v in sorted(skill_usage.items(), key=lambda x: -x[1]):
            w(f"| {k} | {v} |")
        w()

    # ── 五、已安装 Skill 清单 ────────────────────────────────
    if oc_skills:
        w("### OpenCode 已安装 Skills")
        w()
        for s in oc_skills:
            w(f"- `{s}`")
        w()

    # ── 六、模型配置 ─────────────────────────────────────────
    agents = oc_cfg.get("agents", {})
    if agents:
        w("---")
        w()
        w("## 五、模型配置")
        w()
        w("| 智能体 | 模型 |")
        w("|--------|------|")
        for name, cfg in agents.items():
            model = cfg.get("model", "N/A")
            w(f"| {name} | `{model}` |")
        w()

    # ── GitNexus ─────────────────────────────────────────────
    if gn:
        w("---")
        w()
        w("## 六、代码知识图谱 (GitNexus)")
        w()
        w("| 仓库 | 路径 | 文件数 | 节点数 | 索引时间 |")
        w("|------|------|--------|--------|----------|")
        for r in gn:
            stats = r.get("stats", {})
            w(f"| {r.get('name','')} | `{r.get('path','')}` | {stats.get('files',0)} | {stats.get('nodes',0)} | {r.get('indexedAt','')[:10]} |")
        w()

    # ── Footer ───────────────────────────────────────────────
    w("---")
    w()
    w("## 附录")
    w()
    w("### 方法论总结")
    w()
    w("> **TODO**: 请根据上述场景数据，手动补充以下内容：")
    w("> 1. 从实际使用模式中提炼 2-3 条方法论")
    w("> 2. 为核心场景补充效率提升估算")
    w("> 3. 总结遇到的问题与下一步计划")
    w()
    w("### 数据源")
    w()
    w(f"- 解析数据: `{args.input}`")
    w(f"- 生成时间: {meta.get('generated_at', 'N/A')}")
    w(f"- 扫描范围: {args.start_date} ~ {args.end_date}")
    w()

    # Write
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"报告已生成: {out} ({len(L)} 行)")


if __name__ == "__main__":
    main()
