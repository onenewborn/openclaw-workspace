---
name: notion
description: Notion API 集成，支持读取页面、数据库、创建和更新内容。用于知识管理和文档协作。
---

# Notion Skill

## 配置

API Key 存储在: `/root/.openclaw/secrets/notion-api.key`

## 使用方式

通过 `exec` 调用 Notion API，使用 curl 发送请求。

### 基础请求格式

```bash
NOTION_API_KEY=$(cat /root/.openclaw/secrets/notion-api.key)

curl -X GET \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  https://api.notion.com/v1/users/me
```

## 常用 API 端点

### 用户相关
- `GET /v1/users/me` - 获取当前用户信息
- `GET /v1/users` - 列出所有用户

### 页面相关
- `GET /v1/pages/{page_id}` - 获取页面信息
- `PATCH /v1/pages/{page_id}` - 更新页面
- `GET /v1/blocks/{block_id}/children` - 获取页面内容

### 数据库相关
- `GET /v1/databases/{database_id}` - 获取数据库信息
- `POST /v1/databases/{database_id}/query` - 查询数据库
- `POST /v1/databases` - 创建数据库

### 搜索
- `POST /v1/search` - 搜索页面和数据库

## 使用示例

### 搜索页面
```bash
curl -X POST \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query": "Linux 命令"}' \
  https://api.notion.com/v1/search
```

### 获取页面内容
```bash
curl -X GET \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  https://api.notion.com/v1/blocks/{page_id}/children
```

### 创建页面
```bash
curl -X POST \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": { "database_id": "{database_id}" },
    "properties": {
      "Name": { "title": [{ "text": { "content": "新页面" } }] }
    }
  }' \
  https://api.notion.com/v1/pages
```

## 注意事项

1. **API Key 安全**: 不要硬编码 API key，从文件读取
2. **Notion-Version**: 必须包含版本头（2022-06-28 或更新）
3. **权限**: 确保集成已添加到对应的工作空间和页面
4. **Rate Limit**: 每秒 3 次请求

## 相关链接

- [Notion API 文档](https://developers.notion.com/)
- [API 参考](https://developers.notion.com/reference/intro)
