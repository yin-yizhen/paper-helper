# paper-helper Code Map

最近完整验收提交：`aadc210`（台账、引文烟雾测试与 skill 结构校验通过；当前环境缺少 DOCX 渲染后端）。

## 先看这里

| 目标 | 主要文件 | 配套测试 | 验证命令 |
| --- | --- | --- | --- |
| 改任务调度、浏览器就绪门与承诺边界 | `SKILL.md`、`references/browser-readiness.md`、`references/environment-and-recovery.md` | `tests/run_smoke_tests.ps1` + Chrome 扩展/应用内浏览器手工验收 | `python ...quick_validate.py .` |
| 改 CNKI 题录台账 | `scripts/reference_ledger.py` | `tests/fixtures/references.valid.json` | `tests/run_smoke_tests.ps1` |
| 改数字引文检查 | `scripts/check_citations.py` | `tests/fixtures/manuscript.md` | `tests/run_smoke_tests.ps1` |
| 改 Word 交付 | `scripts/build_course_paper_docx.py` | 手工样例 | 生成后按 documents 渲染检查 |

## End-to-End Flow

```text
用户主题 -> 浏览器就绪门（失败即报告阻塞并结束）-> SKILL.md 最少选择 -> 用户可见且已连接的浏览器中的 CNKI 专用 skill / 浏览器核验
-> references.json -> reference_ledger.py -> 正文 [n] 引文
-> check_citations.py -> build_course_paper_docx.py -> DOCX 渲染验收
```

## 风险与验收

- CNKI 登录、验证码和权限不能自动绕过；状态必须写入台账。
- CNKI 访问必须在用户可见且已连接的浏览器中进行；Chrome 扩展会话或应用内浏览器是自动接管路径，Edge 仅在存在明确控制能力时可自动接管。`ERR_CERT_*` 时停在当前窗口让用户处理，不能切到后台浏览器或忽略证书错误；若桌面窗口启动被系统拦截，要求用户手动打开浏览器，禁止反复用 `Start-Process`/`cmd start` 尝试。
- “继续”或“已打开”不是 CNKI 连接成功证据；必须实际读取检索框或结果列表。418、证书错误、验证码和登录页均不能通过来源门，且必须硬停止：不生成提纲、草稿、参考文献、台账或 Word。
- `journal_indexes` 只有完成 CNKI 期刊索引页核验后才能填入。
- `build_course_paper_docx.py` 是无模板的基础生成器；有用户模板时应由 documents 工作流优先复用模板。
- 运行 `powershell -ExecutionPolicy Bypass -File tests/run_smoke_tests.ps1`；再运行 skill-creator 的 `quick_validate.py`。DOCX 改动还需实际生成、渲染并检查所有页。若机器没有 LibreOffice/等价渲染后端，记录“未完成视觉验收”，不可伪称已验收。
