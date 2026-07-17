# CNKI 浏览器操作

优先调用已安装的 `cnki-search`、`cnki-paper-detail`、`cnki-journal-index` 与 `cnki-download` skills。本文件只在没有专用 skill、但当前 Codex 有浏览器控制工具时使用。

1. 打开 `https://kns.cnki.net/kns8s/search`。
2. 在页面上下文以 Unicode 字符串写入 `input.search-input`，触发 `input` 与 `change` 事件，再点击 `input.search-btn`。
3. 仅在 `#tcaptcha_transform_dy` 可见时认定为验证码。结果行使用 `.result-table-list tbody tr`，题名链接使用 `td.name a.fz14`，期刊使用 `td.source a`。
4. 打开每个候选的详情页；核验 `.brief h1`、`h3.author`、`.doc-top a`、`.head-time`、`.abstract-text`、`p.keywords a`。保留详情页 URL。
5. 对需要核心筛选的期刊，在 `https://navi.cnki.net/knavi` 打开期刊详情；根据页面“被以下数据库收录”区域记录 CSSCI、北大核心、CSCD 等标签，而不是凭刊名猜测。
6. 只有锁定为最终引用的条目才触发下载。优先点击 `#pdfDown`，无 PDF 时尝试 `#cajDown`；随后在浏览器下载管理或本地文件夹确认文件存在，再写入 `downloaded`。

出现登录、权限或验证码界面时暂停并请求用户操作；不得使用非页面授权的下载路径或规避措施。
