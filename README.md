# paper-helper

面向中文大学结课论文的 Codex 技能：从主题出发，协助选择论文类型与字数，核验知网期刊文献、在用户拥有访问权限时下载最终引用文献，并生成带参考文献的 Word 初稿。

## 安装

将仓库克隆或下载为 `paper-helper` 文件夹，复制到 Codex 的个人技能目录：

- 已设置 `CODEX_HOME`：`%CODEX_HOME%\\skills\\paper-helper`
- 未设置时：`%USERPROFILE%\\.codex\\skills\\paper-helper`

重启或刷新 Codex 后，在聊天中使用：

```text
用 $paper-helper 写一篇关于……的课程论文
```

## 要求与限制

- 需要网络和可用的浏览器自动化能力。
- 知网题录检索通常无需登录；全文下载取决于用户的知网权限，并在登录、验证码或付费页面由用户手动完成。
- 技能不编造文献、数据或查重结果，也不保证任何查重系统的具体百分比。
- 请勿提交账号信息、Cookie、下载的受版权保护论文或含个人信息的课程材料到本仓库。

详见 [SKILL.md](SKILL.md)。
