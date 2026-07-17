# paper-helper

面向中文大学结课论文的 Codex skill：从题目开始，按需要少量确认字数与类型，检索并核验 CNKI 中文期刊文献，维护可审计的文献/下载/引文台账，生成并检查 Word 交付件。

它不是“直接拼出一篇看似有文献的文章”的提示词集合：最终引用必须在 CNKI 中逐条核验，文内编号与文末条目可由脚本检查；下载受 CNKI 账户和机构权限约束，登录、验证码和付费操作始终由用户完成。

## 安装

```powershell
git clone https://github.com/yin-yizhen/paper-helper.git
Copy-Item -Recurse .\paper-helper "$env:CODEX_HOME\skills\paper-helper"
```

若未设置 `CODEX_HOME`，将文件夹复制到 `%USERPROFILE%\.codex\skills\paper-helper`。重启或刷新 Codex 后使用：

```text
用 $paper-helper 写一篇关于……的 6000 字课程论文，中文文献必须在知网可查。
```

## 需要什么

- 可联网的 Codex；用于 CNKI 检索的浏览器控制能力，或已安装的 `cnki-*` skills。
- CNKI 账号/学校机构访问权限（仅在下载全文时需要）。本 skill 不保存或索要密码、Cookie、验证码。
- Word 交付需可用的 DOCX 创建与渲染能力。上传 `.docx` 可作为模板；PDF 仅能作为视觉参考。
- Python 3。台账与引文脚本仅用标准库；基础 Word 生成器额外需要 `python-docx`。

首次使用时，缺少其中任何能力都将明确报出，而不会假装已核验、已下载或已视觉检查。

## 交付物

- `论文题目.docx`：已生成并在能力具备时渲染检查的论文。
- `references.json`：CNKI 题录、期刊索引核验、下载状态和引文位置。
- `文献核验结果.md`：人可读的台账报告。
- `引文一致性检查.md`：数字顺序制引文与文末条目的基本闭环报告。

## 能与不能

- 能：让流程可执行、可恢复、可核验；基于核验来源写原创的课程论文初稿；在用户有权限时触发并记录最终引用文献的下载。
- 不能：绕过 CNKI 登录/验证码/付费限制；保证知网或其他平台的具体相似率、AI 检测结果或学校最终审核；将无来源信息写成事实。

详细工作流见 [SKILL.md](SKILL.md)，可执行数据格式见 [reference-data-contract.md](references/reference-data-contract.md)。
