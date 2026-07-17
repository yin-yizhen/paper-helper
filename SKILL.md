---
name: paper-helper
description: Create submission-ready Chinese university course papers from a topic, including a natural original draft, CNKI-verifiable Chinese journal references, citation/download ledger, and a reviewed Word deliverable. Use for course papers, literature reviews, planning/case/strategy papers, CNKI source verification or download, Word-paper delivery, and topic-only requests that need short guided choices.
---

# 论文助手

生成可交付的中文大学结课论文。默认只使用可在 CNKI 定位的中文期刊文献，并交付可追溯的核验台账；不得编造文献、数据、实证过程、下载状态、期刊等级或查重结果。

## 0. 先做环境预检

检查网络、**可见 Chromium 浏览器控制能力**、CNKI 访问会话、文件下载位置和 DOCX 生成/渲染能力。读取 [环境与失败恢复](references/environment-and-recovery.md)。

- CNKI 阶段默认使用用户**可见的浏览器窗口**，而非后台、无头或不可见浏览器会话。需要自动接管时，优先使用已连接的 Chrome 扩展会话或 Codex 应用内浏览器；不要仅因 Windows 安装了 Edge 就宣称能够自动控制 Edge。
- 有 `cnki-search`、`cnki-paper-detail`、`cnki-download`、`cnki-journal-index` 时，也必须将其执行面绑定到可见、已连接的浏览器；不能仅在后台会话检索后声称用户可接手。
- 没有 CNKI 专用 skill 但有可见 Chromium 浏览器控制能力时，读取 [CNKI 浏览器操作](references/cnki-browser-workflow.md)，在该窗口中完成检索和元数据提取。
- 遇到登录、验证码、学校权限、付费页或 `ERR_CERT_*` 证书错误时，保持页面可见并立刻暂停，明确告诉用户在当前浏览器窗口操作；保留 `references.json` 和台账，随后继续。绝不绕过访问控制或忽略证书错误。
- 不能打开或控制可见浏览器时，不得退回后台浏览器冒充 CNKI 核验，也不要通过 `Start-Process`、`cmd start` 或其他命令行方式反复强行启动桌面浏览器。直接提示用户自行在 Chrome 或 Edge 打开 `https://kns.cnki.net/kns8s/search`；用户回复“已打开/继续”后再检查是否存在可接管的浏览器连接，或仅交付“待 CNKI 核验”草稿。

## 1. 最少打扰地确认任务

不要重复询问用户已提供的信息。仅给出缺失的关键选择，最多 3 题、每题 2–3 项；优先确认：

1. 字数：3000 / 5000 / 6000 左右（默认推荐）
2. 类型：文献综述 / 案例分析 / 规划或策略研究 / 理论分析（按题目推荐）
3. 文献层级：核心期刊优先并补充高质量普刊（默认）/ 仅 CSSCI、北大核心、CSCD

学校模板、课程题目边界或案例城市会实质改变结果时，再补问一个短问题。用户上传 `.docx` 模板时，优先复用其版式；PDF 仅作视觉参考。

## 2. 研究与来源闭环

1. 将主题细化为研究问题、暂定题目、适配结构与字数分配；没有用户真实数据时，不写问卷、访谈、计量检验或虚构案例成效。
2. 在可见 Chromium 浏览器中检索 CNKI，候选文献逐篇打开详情页核对作者、题名、期刊、年份/卷期页码或网络首发状态、详情链接与主题相关性。若浏览器显示验证码或证书错误，先由用户完成页面操作再继续。
3. 若用户要求核心期刊，逐刊使用 CNKI 期刊索引页核对，不得由印象推断等级。优先本学科 CSSCI、北大核心、CSCD 与权威专业期刊；不足时说明原因再补充普刊。
4. 在任务目录保存 `references.json`，按 [参考文献数据约定](references/reference-data-contract.md) 记录每篇最终候选。运行：

   ```powershell
   python scripts/reference_ledger.py references.json --report 文献核验结果.md
   ```

5. 锁定“最终引用清单”后，才下载其全文。逐篇记录 `download_status`；只要下载被登录/权限阻断，就如实保留状态。不要下载未进入正文的备选文献。
6. 建立“观点—来源—正文位置”对应关系。外部事实、统计数字、他人结论和具体案例过程必须有已核验来源；只看见题录/摘要的文章，不把摘要细节当作已通读全文的结论。

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
```

修复所有错误后再进入交付：每篇参考文献至少有一处正文引文；每个 `[n]` 都指向存在、已核验的条目；不保留未引用条目。脚本只检查数字顺序制的基本闭环，不能替代人工核对论断是否被来源支持。

## 5. Word 交付与视觉验收

用可用的文档创建能力从经校验的 Markdown/内容生成 `.docx`；没有模板时可使用：

```powershell
python scripts/build_course_paper_docx.py "论文题目.md" --references references.json --output "论文题目.docx"
```

生成后必须按 `documents` 工作流渲染为 PNG，逐页检查标题、正文、页边距、参考文献编号、换页、中文字符与模板样式；修复后重新渲染。若没有 DOCX 渲染能力，交付说明中必须写明“未完成视觉验收”。

## 6. 交付清单

输出并说明：

1. `论文题目.docx`：题目、摘要、关键词、正文、参考文献。
2. `文献核验结果.md`：CNKI 题录、期刊等级核验、下载状态、正文引文位置。
3. `引文一致性检查.md`：引用编号、未引用条目和数据约束检查结果。
4. `references.json`：可继续下载、复核和修改的机器可读台账。

交付说明必须列出实际字数、论文类型、已核验篇数、已下载篇数、未下载原因、DOCX 是否已渲染验收和提交前仍需用户处理的事项。不得宣称保证通过查重或替代学校最终审核。
