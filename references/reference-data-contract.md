# 参考文献数据约定

`references.json` 是最终来源的证据台账，数组顺序即参考文献编号。链接本身不等于核验：每项必须同时记录核验时间、页面所见证据、稳定标识、全文状态和论断落点。

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
  "publication_status": "published",
  "online_first_date": "",
  "cnki_url": "核验时实际打开的详情页 URL",
  "stable_cnki_url": "去掉会话参数后仍可定位的 URL（能取得时填写）",
  "stable_cnki_id": "filename/数据库记录号/DOI 等稳定标识",
  "cnki_verified": true,
  "verified_at": "2026-07-17T10:00:00+08:00",
  "verification_evidence": {"detail_title": "页面题名", "source": "页面期刊名"},
  "selection_tier": "core",
  "journal_index_verified": true,
  "journal_indexes": ["CSSCI"],
  "journal_index_evidence": "CNKI 期刊导航详情页所见标签",
  "download_status": "downloaded",
  "fulltext_path": "downloads/作者甲-文章题名.pdf",
  "fulltext_read": true,
  "citation_locations": ["2.1", "3.2"],
  "claim_support_locations": ["PDF p.6：支持的具体观点"],
  "accessed_at": "2026-07-17",
  "notes": ""
}
```

- `publication_status` 仅可为 `published` 或 `online_first`。网络首发必须填写 `online_first_date`、`accessed_at`，并按 `[J/OL]` 输出；不要虚构卷期页码。
- `selection_tier=core` 时，必须有 `journal_index_verified=true` 和 `journal_index_evidence`；不能凭刊名、搜索摘要或印象判断核心等级。
- `downloaded` 只有本地文件实际存在且非空时才能填写；最终门禁会真实检查 `fulltext_path`。`fulltext_read=true` 只有实际打开并阅读全文后才能填写。
- `claim_support_locations` 要写页码/章节与所支持观点，不能只写“已阅读”。
- 最终交付必须运行 `reference_ledger.py --require-final`。任一最终来源未下载、未读或无论断证据，门禁失败并停止写作/交付。

支持的下载状态：`downloaded`、`catalog_verified`、`waiting_for_login`、`no_access`、`not_available`、`not_attempted`。
