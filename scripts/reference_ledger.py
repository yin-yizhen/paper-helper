#!/usr/bin/env python3
"""Validate a CNKI reference ledger and render a human-auditable Markdown report."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

STATUSES = {"downloaded", "catalog_verified", "waiting_for_login", "no_access", "not_available", "not_attempted"}
REQUIRED = ("id", "authors", "title", "journal", "year", "cnki_url", "cnki_verified", "download_status")


def load_items(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("references.json 必须是对象数组")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("references.json 的每一项必须是对象")
    return data


def validate(items: list[dict]) -> list[str]:
    problems: list[str] = []
    ids = [item.get("id") for item in items]
    if ids != list(range(1, len(items) + 1)):
        problems.append("id 必须从 1 开始连续编号，且与数组顺序一致")
    for item in items:
        ident = item.get("id", "?")
        for key in REQUIRED:
            if key not in item or item[key] in (None, "", []):
                problems.append(f"[{ident}] 缺少 {key}")
        if item.get("download_status") not in STATUSES:
            problems.append(f"[{ident}] download_status 不合法")
        if item.get("cnki_verified") is not True:
            problems.append(f"[{ident}] 尚未完成 CNKI 题录/详情页核验")
        if item.get("download_status") == "downloaded" and not item.get("download_path"):
            problems.append(f"[{ident}] 标为 downloaded 但缺少 download_path")
        if item.get("journal_indexes") and not item.get("journal_index_verified"):
            problems.append(f"[{ident}] 声明期刊收录但 journal_index_verified 不是 true")
    return problems


def citation(item: dict) -> str:
    authors = "，".join(item.get("authors", [])) or "作者不详"
    volume = item.get("volume") or ""
    issue = item.get("issue") or ""
    vi = f"{volume}" + (f"({issue})" if issue else "")
    pages = item.get("pages") or ""
    tail = ":" + pages if pages else ""
    return f"{authors}. {item.get('title', '')}[J]. {item.get('journal', '')}, {item.get('year', '')}{', ' + vi if vi else ''}{tail}."


def report(items: list[dict], problems: list[str]) -> str:
    lines = ["# 文献核验结果", "", f"共 {len(items)} 篇；CNKI 已核验 {sum(i.get('cnki_verified') is True for i in items)} 篇；已下载 {sum(i.get('download_status') == 'downloaded' for i in items)} 篇。", "", "| 编号 | 文献 | CNKI 核验 | 期刊收录核验 | 下载状态 | 正文位置 |", "| --- | --- | --- | --- | --- | --- |"]
    for item in items:
        level = "、".join(item.get("journal_indexes", [])) or "未声明"
        positions = "、".join(item.get("citation_locations", [])) or "待填写"
        lines.append(f"| {item.get('id', '')} | {citation(item)} | {'是' if item.get('cnki_verified') is True else '否'} | {level if item.get('journal_index_verified') else '未核验'} | {item.get('download_status', '')} | {positions} |")
        if item.get("cnki_url"):
            lines.append(f"|  | CNKI：{item['cnki_url']} |  |  |  |  |")
    lines.extend(["", "## 校验结论", ""])
    if problems:
        lines.extend(f"- {p}" for p in problems)
    else:
        lines.append("- 结构校验通过。仍需人工确认每个论断与来源内容相符。")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("references", type=Path)
    parser.add_argument("--report", type=Path, default=Path("文献核验结果.md"))
    args = parser.parse_args()
    try:
        items = load_items(args.references)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"无法读取台账：{exc}", file=sys.stderr)
        return 2
    problems = validate(items)
    args.report.write_text(report(items, problems), encoding="utf-8")
    print(f"已生成 {args.report}；发现 {len(problems)} 个问题。")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
