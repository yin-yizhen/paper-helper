#!/usr/bin/env python3
"""Check basic numeric in-text citation consistency against references.json."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BRACKET = re.compile(r"\[([^\]]+)\]")


def extract_numbers(text: str) -> tuple[set[int], list[str]]:
    found: set[int] = set()
    malformed: list[str] = []
    for body in BRACKET.findall(text):
        normalized = body.replace("，", ",").replace("－", "-").replace("—", "-").replace("–", "-")
        if not re.fullmatch(r"\s*\d+(?:\s*[-,]\s*\d+)*\s*", normalized):
            continue
        for part in normalized.split(","):
            bits = [x.strip() for x in part.split("-")]
            if len(bits) == 1:
                found.add(int(bits[0]))
            elif len(bits) == 2:
                start, end = map(int, bits)
                if start > end:
                    malformed.append(f"倒序范围 [{body}]")
                elif end - start > 100:
                    malformed.append(f"范围过大 [{body}]")
                else:
                    found.update(range(start, end + 1))
    return found, malformed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("references", type=Path)
    parser.add_argument("--report", type=Path, default=Path("引文一致性检查.md"))
    args = parser.parse_args()
    try:
        text = args.manuscript.read_text(encoding="utf-8")
        refs = json.loads(args.references.read_text(encoding="utf-8"))
        ids = {int(item["id"]) for item in refs}
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"无法读取输入：{exc}", file=sys.stderr)
        return 2
    cited, malformed = extract_numbers(text)
    unknown = sorted(cited - ids)
    unused = sorted(ids - cited)
    lines = ["# 引文一致性检查", "", f"检测到正文数字引文：{', '.join(map(str, sorted(cited))) or '无'}。", "", "## 结果", ""]
    if unknown:
        lines.append("- 正文存在无对应参考文献的编号：" + "、".join(map(str, unknown)))
    if unused:
        lines.append("- 文末台账存在未在正文引用的条目：" + "、".join(map(str, unused)))
    lines.extend(f"- {item}" for item in malformed)
    if not (unknown or unused or malformed):
        lines.append("- 数字顺序制基本闭环通过。请继续人工核对引文是否真正支持对应论断。")
    args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"已生成 {args.report}。")
    return 1 if unknown or unused or malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
