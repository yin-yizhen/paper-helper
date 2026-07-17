#!/usr/bin/env python3
"""Validate a CNKI evidence ledger and render a human-auditable report."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

STATUSES = {"downloaded", "catalog_verified", "waiting_for_login", "no_access", "not_available", "not_attempted"}
PUBLICATION_STATUSES = {"published", "online_first"}
SELECTION_TIERS = {"core", "quality_general"}
REQUIRED = (
    "id", "authors", "title", "journal", "year", "cnki_url", "cnki_verified",
    "verified_at", "verification_evidence", "publication_status", "download_status",
)


def load_items(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("references.json 必须是对象数组")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("references.json 的每一项必须是对象")
    return data


def _missing(value: object) -> bool:
    return value is None or value == "" or value == [] or value == {}


def validate(items: list[dict], require_final: bool = False, base_dir: Path | None = None) -> list[str]:
    problems: list[str] = []
    if not items:
        problems.append("参考文献台账不能为空")
    ids = [item.get("id") for item in items]
    if ids != list(range(1, len(items) + 1)):
        problems.append("id 必须从 1 开始连续编号，且与数组顺序一致")
    for item in items:
        ident = item.get("id", "?")
        for key in REQUIRED:
            if key not in item or _missing(item[key]):
                problems.append(f"[{ident}] 缺少 {key}")
        if item.get("download_status") not in STATUSES:
            problems.append(f"[{ident}] download_status 不合法")
        if item.get("publication_status") not in PUBLICATION_STATUSES:
            problems.append(f"[{ident}] publication_status 必须是 published 或 online_first")
        if item.get("selection_tier") and item.get("selection_tier") not in SELECTION_TIERS:
            problems.append(f"[{ident}] selection_tier 不合法")
        if item.get("cnki_verified") is not True:
            problems.append(f"[{ident}] 尚未完成 CNKI 结果页与详情页核验")
        if item.get("download_status") == "downloaded" and not (item.get("fulltext_path") or item.get("download_path")):
            problems.append(f"[{ident}] 标为 downloaded 但缺少 fulltext_path")
        if item.get("journal_indexes") and not item.get("journal_index_verified"):
            problems.append(f"[{ident}] 声明期刊收录但 journal_index_verified 不是 true")
        if item.get("selection_tier") == "core" and not (item.get("journal_index_verified") and item.get("journal_index_evidence")):
            problems.append(f"[{ident}] 核心来源缺少 CNKI 期刊索引证据")
        if item.get("publication_status") == "online_first":
            for key in ("online_first_date", "accessed_at"):
                if _missing(item.get(key)):
                    problems.append(f"[{ident}] 网络首发缺少 {key}")
        if require_final:
            if item.get("download_status") != "downloaded":
                problems.append(f"[{ident}] 最终交付前全文必须实际下载")
            if item.get("fulltext_read") is not True:
                problems.append(f"[{ident}] 最终交付前全文必须实际阅读并标记 fulltext_read=true")
            for key in ("stable_cnki_id", "fulltext_path", "citation_locations", "claim_support_locations"):
                if _missing(item.get(key)):
                    problems.append(f"[{ident}] 最终交付缺少 {key}")
            fulltext = item.get("fulltext_path")
            if fulltext and base_dir is not None:
                path = Path(fulltext)
                path = path if path.is_absolute() else base_dir / path
                if not path.is_file() or path.stat().st_size == 0:
                    problems.append(f"[{ident}] fulltext_path 对应文件不存在或为空：{path}")
    return problems


def citation(item: dict) -> str:
    authors = "，".join(item.get("authors", [])) or "作者不详"
    title = item.get("title", "")
    journal = item.get("journal", "")
    year = item.get("year", "")
    if item.get("publication_status") == "online_first":
        date = item.get("online_first_date", year)
        url = item.get("stable_cnki_url") or item.get("cnki_url", "")
        accessed = item.get("accessed_at", "")
        return f"{authors}. {title}[J/OL]. {journal}, {date}. {url}[{accessed}]."
    volume = item.get("volume") or ""
    issue = item.get("issue") or ""
    vi = f"{volume}" + (f"({issue})" if issue else "")
    pages = item.get("pages") or ""
    tail = ":" + pages if pages else ""
    return f"{authors}. {title}[J]. {journal}, {year}{', ' + vi if vi else ''}{tail}."


def report(items: list[dict], problems: list[str], require_final: bool) -> str:
    read_count = sum(i.get("fulltext_read") is True for i in items)
    lines = [
        "# 文献核验结果", "",
        f"共 {len(items)} 篇；CNKI 已核验 {sum(i.get('cnki_verified') is True for i in items)} 篇；已下载 {sum(i.get('download_status') == 'downloaded' for i in items)} 篇；已通读 {read_count} 篇。",
        f"校验模式：{'最终交付硬门禁' if require_final else '候选台账结构校验'}。", "",
        "| 编号 | 文献 | CNKI 证据 | 期刊等级 | 全文 | 论断证据 |", "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        level = "、".join(item.get("journal_indexes", [])) or "未声明"
        evidence = item.get("verification_evidence") or "缺失"
        if isinstance(evidence, dict):
            evidence = "；".join(f"{k}={v}" for k, v in evidence.items())
        support = "、".join(item.get("claim_support_locations", [])) or "待填写"
        fulltext = f"{item.get('download_status', '')}/{'已读' if item.get('fulltext_read') else '未读'}"
        lines.append(f"| {item.get('id', '')} | {citation(item)} | {item.get('verified_at', '')}；{evidence} | {level if item.get('journal_index_verified') else '未核验'} | {fulltext} | {support} |")
    lines.extend(["", "## 校验结论", ""])
    if problems:
        lines.extend(f"- {p}" for p in problems)
    else:
        lines.append("- 门禁通过。仍需人工确认每个论断与所标全文页码/章节相符。")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("references", type=Path)
    parser.add_argument("--report", type=Path, default=Path("文献核验结果.md"))
    parser.add_argument("--require-final", action="store_true", help="要求所有最终来源均已下载、通读并建立论断证据")
    args = parser.parse_args()
    try:
        items = load_items(args.references)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"无法读取台账：{exc}", file=sys.stderr)
        return 2
    problems = validate(items, require_final=args.require_final, base_dir=args.references.resolve().parent)
    args.report.write_text(report(items, problems, args.require_final), encoding="utf-8")
    print(f"已生成 {args.report}；发现 {len(problems)} 个问题。")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
