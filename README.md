# Rizhi · 知识管家

> 个人知识管理系统 — 摄入、检索、关联、主动提醒

## 功能

- **摄入**：文本/网页 → DeepSeek 自动摘要 + 标签 → SQLite + 向量存储
- **检索**：关键词 + 语义混合搜索
- **关联**：DeepSeek 自动发现知识间关联
- **Web 抓取**：mini_firecrawl 集成，URL → Markdown → 入库
- **每日简报**：定时扫描关联，主动推送

## 技术栈

- Python 3.12 + Flask
- SQLite + sentence-transformers (all-MiniLM-L6-v2)
- DeepSeek API（摘要/翻译/关联分析）
- systemd 守护进程

## 部署

```bash
pip install flask sentence-transformers requests pillow img2pdf
python3 knowledge_butler.py
# 默认运行在 0.0.0.0:9000
```

## API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/ingest` | POST | 摄入知识 `{content, source}` |
| `/api/search?q=` | GET | 搜索知识 |
| `/api/web-ingest` | POST | 网页抓取入库 `{url}` |
| `/api/connections` | GET | 查看关联 |
| `/api/stats` | GET | 统计信息 |

## 配置

环境变量：
- `DEEPSEEK_KEY` — DeepSeek API Key
- `KB_API_KEY` — API 鉴权密钥

## License

MIT
