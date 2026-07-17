#!/usr/bin/env python3
"""Measure Chinese course-paper length without counting references or Markdown syntax."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REFERENCE_HEADING = re.compile(r"^#{1,6}\s*(参考文献|References)\s*$", re.I)


def main_text(source: str) -> str:
    kept: list[str] = []
    skip_front_section = False
    first_h1_skipped = False
    for raw in source.splitlines():
        stripped = raw.strip()
        if REFERENCE_HEADING.match(stripped):
            break
        heading = re.match(r"^(#{1,6})\s*(.+)$", stripped)
        if heading:
            level, name = len(heading.group(1)), heading.group(2).strip()
            if level == 1 and not first_h1_skipped:
                first_h1_skipped = True
                continue
            if re.fullmatch(r"摘要|关键词|Abstract|Keywords", name, re.I):
                skip_front_section = True
                continue
            skip_front_section = False
        if skip_front_section or re.match(r"^(摘要|关键词|Abstract|Keywords)\s*[：:]", stripped, re.I):
            continue
        line = re.sub(r"^#{1,6}\s*", "", stripped)
        line = re.sub(r"\[(?:\d+[，,、\-—–]?\s*)+\]", "", line)
        line = re.sub(r"[*_`>#|]", "", line)
        if line:
            kept.append(line)
    return "\n".join(kept)


def counts(text: str) -> dict[str, int]:
    cjk = len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", text))
    latin_words = len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", text))
    digits = len(re.findall(r"\d+(?:\.\d+)?", text))
    return {"body_cjk_characters": cjk, "body_latin_words": latin_words, "body_number_tokens": digits, "effective_length": cjk + latin_words + digits}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--report", type=Path, default=Path("字数检查.json"))
    parser.add_argument("--target", type=int)
    parser.add_argument("--tolerance", type=float, default=0.1)
    args = parser.parse_args()
    if args.target is not None and args.target <= 0:
        print("target 必须大于 0", file=sys.stderr)
        return 2
    try:
        result = counts(main_text(args.manuscript.read_text(encoding="utf-8")))
    except OSError as exc:
        print(f"无法读取正文：{exc}", file=sys.stderr)
        return 2
    if args.target:
        lower = round(args.target * (1 - args.tolerance))
        upper = round(args.target * (1 + args.tolerance))
        result.update({"target": args.target, "allowed_min": lower, "allowed_max": upper, "within_target": lower <= result["effective_length"] <= upper})
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"正文有效长度：{result['effective_length']}；报告：{args.report}")
    return 1 if args.target and not result["within_target"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
