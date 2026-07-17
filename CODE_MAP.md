# paper-helper Code Map

最近完整验收提交：`unknown`（2026-07-17 本地完成结构、台账、引文、字数、网络首发格式与 DOCX 生成验证；当前机器仍缺 LibreOffice 渲染后端）。

## 先看这里

| 目标 | 主要文件 | 配套测试 | 验证命令 |
| --- | --- | --- | --- |
| 改总流程与硬门禁 | `SKILL.md`、`references/environment-and-recovery.md` | 烟雾测试 + 应用内浏览器手工验收 | `python <skill-creator>/scripts/quick_validate.py .` |
| 改浏览器接管、验证码、筛选与期刊取证 | `references/browser-readiness.md`、`references/cnki-browser-workflow.md` | CNKI 真机手工验收 | 复用标签、新建标签、验证码真可见、筛选保留、期刊精确匹配各验一次 |
| 改来源数量与全文阅读规则 | `references/source-workflow.md`、`references/reference-data-contract.md` | 合法/非法台账夹具 | `powershell -ExecutionPolicy Bypass -File tests/run_smoke_tests.ps1` |
| 改 CNKI 证据台账与 `[J/OL]` | `scripts/reference_ledger.py` | `tests/fixtures/references.*.json` | 同上 |
| 改数字引文检查 | `scripts/check_citations.py` | `tests/fixtures/manuscript.md` | 同上 |
| 改正文字数 | `scripts/count_manuscript.py` | `tests/fixtures/manuscript.md` | 同上 |
| 改 Word 交付 | `scripts/build_course_paper_docx.py` | 合法台账夹具 + 实际 DOCX | 用 bundled Python 生成，再按 documents 工作流渲染 |

## End-to-End Flow

```text
用户主题
-> 浏览器自动取得（应用内已有 -> 用户浏览器 -> 应用内新建）
-> CNKI 正常页 / 验证码真可见判断
-> 每次检索重施并核对筛选
-> 详情页证据 + 核心期刊索引证据
-> 锁定最终清单 -> 全文逐篇下载、通读、记录论断页码
-> reference_ledger.py --require-final（失败即停）
-> 正文 [n] -> check_citations.py + count_manuscript.py
-> build_course_paper_docx.py -> DOCX 渲染验收（失败不得称最终版）
```

## 常见风险点

- `browser.user.openTabs()` 为空不代表应用内浏览器没有标签；先检查应用内选中标签和标签列表。
- `#tcaptcha_transform_dy` 存在不代表验证码可见；必须同时检查 display、visibility、opacity、尺寸和视口交集。
- CNKI 换关键词可能重置 CSSCI/北大核心/年份筛选；每次检索后都要重施并读取已选状态。
- 期刊导航可能显示最近浏览/推荐结果；等待真实结果容器，再精确匹配规范化刊名。
- 长 `v=` URL 可能随会话失效；台账同时保留实际证据 URL 与 filename/记录号/DOI 等稳定标识。
- “点击下载”不等于文件存在，“有摘要”不等于通读全文。最终门禁要求本地文件、`fulltext_read=true` 和论断页码。
- 网络首发使用 `[J/OL]`；没有正式卷期页码时不补造。
- 当前机器没有 LibreOffice；DOCX 可生成但无法完成最终视觉验收。

## 本地验证命令

```powershell
python -m py_compile scripts\reference_ledger.py scripts\check_citations.py scripts\count_manuscript.py scripts\build_course_paper_docx.py
powershell -ExecutionPolicy Bypass -File tests\run_smoke_tests.ps1
python D:\codex_home\skills\.system\skill-creator\scripts\quick_validate.py .
```

真实验收还要在 CNKI 页面覆盖：已有标签接管、新建应用内标签、透明验证码元素、重新检索后的筛选状态、期刊精确匹配、PDF 下载落盘与全文页码记录。DOCX 改动必须生成、渲染并逐页检查；无渲染后端时不可宣称最终交付。
