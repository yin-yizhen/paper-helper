#!/usr/bin/env python3
"""Guard the non-negotiable Chrome-first CNKI workflow instructions."""
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "SKILL.md": [
        "可见、可控的 Chrome 会话",
        "Start-Process <URL>",
        "open-chrome-window.js",
        "只处理 Chrome 连接、登录、权限和验证问题",
        "拖动下方拼图完成验证",
    ],
    "references/browser-readiness.md": [
        "Chrome 扩展会话",
        "应用内浏览器作为题录检索的最后备选",
        "系统默认浏览器",
        "向右滑动完成验证",
        "handoff",
    ],
    "references/environment-and-recovery.md": [
        "Chrome 未运行但插件启动条件正常",
        "不得用系统默认浏览器打开 URL",
        "Chrome 里的知网页签",
    ],
    "references/cnki-browser-workflow.md": [
        "Chrome 里的知网页签",
        "tab.goto()",
        "请完成安全验证",
        "chrome://extensions",
    ],
    "README.md": [
        "固定优先使用已连接的 Chrome profile",
        "不会通过系统默认浏览器打开 CNKI",
        "标题为“安全验证”或 CNKI 的标签",
    ],
}


def main() -> int:
    missing: list[str] = []
    for relative, required in FILES.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for phrase in required:
            if phrase not in text:
                missing.append(f"{relative}: missing {phrase!r}")
    if missing:
        print("CNKI browser policy check failed:", *missing, sep="\n- ", file=sys.stderr)
        return 1
    print("CNKI browser policy check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
