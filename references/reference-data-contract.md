# 参考文献数据约定

`references.json` 必须是对象数组；数组顺序即参考文献编号。每项至少包含：

```json
{
  "id": 1,
  "authors": ["作者甲", "作者乙"],
  "title": "文章题名",
  "journal": "期刊名",
  "year": 2024,
  "volume": "",
  "issue": "3",
  "pages": "45-53",
  "cnki_url": "https://kns.cnki.net/...",
  "cnki_verified": true,
  "journal_index_verified": true,
  "journal_indexes": ["CSSCI"],
  "download_status": "downloaded",
  "download_path": "downloads/作者甲-文章题名.pdf",
  "citation_locations": ["2.1", "3.2"],
  "notes": ""
}
```

`id` 必须从 1 连续编号；`cnki_verified` 只有在 CNKI 题录与详情页均已核对时才可为 `true`。`journal_index_verified` 仅表示期刊收录信息已在 CNKI 期刊索引页核对。`download_path` 只在文件实际已下载时填写。

支持的 `download_status`：`downloaded`、`catalog_verified`、`waiting_for_login`、`no_access`、`not_available`、`not_attempted`。
