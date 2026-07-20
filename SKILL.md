---
name: paper-helper
description: Create submission-ready Chinese university course papers from a topic, including a natural original draft, CNKI-verifiable Chinese journal references, citation/download ledger, and a reviewed Word deliverable. Use for course papers, literature reviews, planning/case/strategy papers, CNKI source verification or download, Word-paper delivery, and topic-only requests that need short guided choices.
---

# 论文助手

生成可交付的中文大学结课论文。默认只使用可在 CNKI 定位的中文期刊文献，并交付可追溯的核验台账；不得编造文献、数据、实证过程、下载状态、期刊等级或查重结果。

## 0. 先做环境预检

检查网络、**可见浏览器连接能力**、CNKI 访问会话、文件下载位置和 DOCX 生成/渲染能力。读取 [浏览器就绪门](references/browser-readiness.md) 与 [环境与失败恢复](references/environment-and-recovery.md)。

- CNKI 阶段默认使用用户**可见、可控的 Chrome 会话**，以复用机构登录、个人账号、验证码和下载权限。取得顺序固定为：“Chrome 扩展已连接的 CNKI 标签 → 已连接 Chrome 的新 CNKI 标签 → 经用户同意启动 Chrome 后重试 → 应用内浏览器最后兜底”。应用内浏览器仅用于 Chrome 不可用时的题录检索备选，不得假定它拥有 Chrome 的登录态或下载权限。
- 不得通过 `Start-Process <URL>`、`cmd start`、系统默认浏览器、外部链接外跳或其他桌面启动方式打开 CNKI；它们可能把页面送到 Edge。进入 CNKI 必须在已选中的可控 Chrome 标签内使用 `tab.goto()` 或等价浏览器导航能力。
- 若 Chrome 已安装、扩展与 native host 均可用但 Chrome 未运行，先明确询问用户“是否允许现在启动 Chrome 并连接当前个人 profile？”；仅在用户同意后，调用**当前 Chrome 插件明确提供**的 `open-chrome-window.js` 或等价启动器，再重新检查连接。没有该启动器时不得猜测路径或改用系统默认浏览器。
- 有 `cnki-search`、`cnki-paper-detail`、`cnki-download`、`cnki-journal-index` 时，也必须将其执行面绑定到可见、已连接的浏览器；不能仅在后台会话检索后声称用户可接手。
- 没有 CNKI 专用 skill 但有可见 Chromium 浏览器控制能力时，读取 [CNKI 浏览器操作](references/cnki-browser-workflow.md)，在该窗口中完成检索和元数据提取。
- 遇到登录、验证码、学校权限、付费页或 `ERR_CERT_*` 证书错误时，必须把当前**Chrome 里的知网页签**作为 `handoff` 保留并前台可见，再暂停。提示用户切换到标题为“安全验证”或 CNKI 的 Chrome 标签完成操作；若 Chrome 当前显示 `chrome://extensions` 等不可脚本页面，提示用户手动切到该验证标签，不要继续自动点击或改开 Edge。绝不绕过访问控制或忽略证书错误。
- 不能打开或控制可见浏览器时，不得退回后台浏览器冒充 CNKI 核验，也不要通过 `Start-Process`、`cmd start` 或其他命令行方式反复强行启动桌面浏览器。完成上述三种自动接管尝试后，报告阻塞原因并硬停止；**不得**生成题目、提纲、草稿、参考文献、台账或 DOCX。
- 用户仅回复“继续”不等于浏览器已经连接，也不等于 CNKI 已恢复。只有实际读取到 CNKI 结果页的检索框或结果列表后，才能进入文献核验。CNKI 未通过来源门时，只处理 Chrome 连接、登录、权限和验证问题；不要先询问字数、论文类型或文献层级。页面是 418、`ERR_CERT_*`、登录/验证码或无法访问页时，立即停止；不写论文、不写参考文献、不创建“待核验版”。

## 1. 最少打扰地确认任务

仅在 CNKI 来源门通过后，不要重复询问用户已提供的信息。仅给出缺失的关键选择，最多 3 题、每题 2–3 项；优先确认：

1. 字数：3000 / 5000 / 6000 左右（默认推荐）
2. 类型：文献综述 / 案例分析 / 规划或策略研究 / 理论分析（按题目推荐）
3. 文献层级：核心期刊优先并补充高质量普刊（默认）/ 仅 CSSCI、北大核心、CSCD

学校模板、课程题目边界或案例城市会实质改变结果时，再补问一个短问题。用户上传 `.docx` 模板时，优先复用其版式；PDF 仅作视觉参考。

## 2. 研究与来源闭环

1. 将主题细化为研究问题、暂定题目、适配结构与字数分配；没有用户真实数据时，不写问卷、访谈、计量检验或虚构案例成效。
2. 在当前 Chrome 里的知网页签中检索 CNKI，候选文献逐篇打开详情页核对作者、题名、期刊、年份/卷期页码或网络首发状态、详情链接与主题相关性。若页面显示验证码或证书错误，先由用户完成页面操作再继续。
3. 每次换关键词、检索模式或翻页后重新应用并读取筛选状态，防止 CNKI 自动清空核心/年份条件。验证码阻塞条件为：验证码元素真正可见，**或**页面可见正文出现“请完成安全验证”“向右滑动完成验证”“拖动下方拼图完成验证”之一；任一成立即 handoff 并硬停止。
4. 若用户要求核心期刊，逐刊使用 CNKI 期刊索引页精确匹配完整刊名并保存页面证据，不得由印象、最近浏览或推荐结果推断等级。优先本学科 CSSCI、北大核心、CSCD 与权威专业期刊；不足时说明原因再补充普刊。
5. 默认 6000 字综述使用 15—20 篇最终来源，以近五年为主并保留 2—4 篇真正重要的早期文献；不要全部依赖同一年网络首发文章。其他字数按论证需要调整。
6. 在任务目录保存 `references.json`，按 [参考文献数据约定](references/reference-data-contract.md) 记录每篇最终候选。候选阶段可运行普通结构校验：

   ```powershell
   python scripts/reference_ledger.py references.json --report 文献核验结果.md
   ```

7. 锁定“最终引用清单”后，下载并实际通读**全部**最终全文，记录本地路径、阅读状态及“观点—全文页码/章节—正文位置”。只要一篇被登录/权限/付费阻断，就保存证据并硬停止；不得依靠摘要先写论文。
8. 动笔前运行最终来源硬门禁；非零退出时不得进入写作：

   ```powershell
   python scripts/reference_ledger.py references.json --require-final --report 文献核验结果.md
   ```

## 3. 写作规则

- 综述：引言—概念与理论—研究脉络—主题争议—评述与研究空白—结论。
- 案例/策略：问题界定—分析框架—证据与诊断—策略或机制—讨论与结论。
- 每段遵循“观点—证据—分析—过渡”。综合多篇研究形成判断，不顺抄单篇文章结构或措辞。
- 保持自然、具体、克制的学生课程论文语体；不以复制、拼贴、同义替换或刻意重复来追求任何相似比。
- “约 10%”只能作为低重复风险期望，不承诺知网、维普、Turnitin 或 AI 检测结果；相似率不等于 AI 写作判定。
- 采用用户指定格式；未指定时采用 GB/T 7714—2015 数字顺序制，网络首发按学校规则标为 `[J/OL]` 或替换为正式刊出文献。

## 4. 文内引文与文末文献校验

完成正文后，将正文保存为 `论文题目.md`，并运行：

```powershell
python scripts/check_citations.py "论文题目.md" references.json --report 引文一致性检查.md
python scripts/count_manuscript.py "论文题目.md" --target 6000 --report 字数检查.json
```

将 `--target` 替换为用户确认字数。字数脚本不计题目、摘要、关键词和参考文献。修复所有错误后再进入交付：每篇参考文献至少有一处正文引文；每个 `[n]` 都指向存在、已核验且通读的条目；不保留未引用条目。脚本只检查基本闭环，人工还要逐条核对正文论断与 `claim_support_locations`。

## 5. Word 交付与视觉验收

用可用的文档创建能力从经校验的 Markdown/内容生成 `.docx`；没有模板时可使用：

```powershell
python scripts/build_course_paper_docx.py "论文题目.md" --references references.json --output "论文题目.docx"
```

生成后必须按 `documents` 工作流渲染为 PNG，逐页检查标题、正文、页边距、参考文献编号、换页、中文字符与模板样式；修复后重新渲染。用户要求“直接使用/最终交付”时，没有 DOCX 渲染能力就硬停止，不能把未验收文件称为最终版。网络首发必须输出 `[J/OL]`，不能虚构卷期页码。

## 6. 交付清单

输出并说明：

1. `论文题目.docx`：题目、摘要、关键词、正文、参考文献。
2. `文献核验结果.md`：CNKI 题录、期刊等级核验、下载状态、正文引文位置。
3. `引文一致性检查.md`：引用编号、未引用条目和数据约束检查结果。
4. `字数检查.json`：不含参考文献和 Markdown 标记的正文有效长度。
5. `references.json`：包含 CNKI 页面证据、稳定标识、期刊等级证据、全文路径和论断页码的机器可读台账。

交付说明必须列出实际字数、论文类型、已核验篇数、已下载篇数、未下载原因、DOCX 是否已渲染验收和提交前仍需用户处理的事项。不得宣称保证通过查重或替代学校最终审核。
