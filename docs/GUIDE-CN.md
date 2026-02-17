# OpenClaw Workspace 使用指南

## 简介

OpenClaw Workspace 是一个用于管理与 OpenClaw 相关的代码版本，并与云端 OpenClaw 服务联动的工作空间工具。

## 主要功能

- **云服务集成**：连接并同步云端 OpenClaw 服务
- **版本管理**：跟踪和管理 OpenClaw 项目的代码版本
- **配置管理**：灵活的配置选项，支持不同环境
- **模块化架构**：清晰的关注点分离，服务导向设计

## 安装

```bash
npm install
```

## 配置

1. 复制示例环境文件：

```bash
cp config/example.env .env
```

2. 编辑 `.env` 文件，配置以下参数：

- `OPENCLAW_CLOUD_ENDPOINT`: OpenClaw 云服务端点地址
- `OPENCLAW_API_KEY`: 用于身份验证的 API 密钥
- `OPENCLAW_VERSION_FILE`: 版本跟踪文件位置（默认：`.openclaw-version`）

## 使用方法

### 命令行工具

直接运行工作空间：

```bash
npm start
```

或使用 Node.js：

```bash
node src/index.js
```

### 模块引用

```javascript
const OpenClawWorkspace = require('./src/index');

// 初始化工作空间
const workspace = new OpenClawWorkspace({
  cloudEndpoint: 'https://api.openclaw.cloud',
  apiKey: 'your-api-key'
});

// 连接并初始化
await workspace.initialize();

// 获取版本信息
const versionInfo = await workspace.getVersionInfo();
console.log('当前版本:', versionInfo);

// 与云端同步
await workspace.syncWithCloud();

// 完成后断开连接
await workspace.disconnect();
```

## 核心服务

### CloudService (云服务)

处理与云端 OpenClaw 服务的通信：

- `connect()`: 建立与云服务的连接
- `disconnect()`: 关闭与云服务的连接
- `sync()`: 与云端同步数据
- `sendData(data)`: 向云端发送数据
- `receiveData()`: 从云端接收数据
- `isConnected()`: 检查连接状态

### VersionManager (版本管理器)

管理 OpenClaw 项目的代码版本：

- `getCurrentVersion()`: 获取当前版本信息
- `updateVersion(versionInfo)`: 更新版本信息
- `getVersionHistory()`: 获取版本历史
- `compareVersions(v1, v2)`: 比较两个版本字符串
- `incrementVersion(type)`: 递增版本号（major, minor, 或 patch）

## 示例

查看 `examples/` 目录获取使用示例。

### 基本使用示例

```bash
node examples/basic-usage.js
```

### 版本管理示例

```bash
node examples/version-management.js
```

## 项目结构

```
openclaw-workspace/
├── src/                            # 源代码
│   ├── index.js                    # 主入口
│   └── services/                   # 服务模块
│       ├── cloud-service.js        # 云服务集成
│       └── version-manager.js      # 版本管理
├── config/                         # 配置文件
│   ├── default.json                # 默认配置
│   └── example.env                 # 环境变量示例
├── docs/                           # 文档
├── examples/                       # 使用示例
└── README.md                       # 说明文档
```

## 常见问题

### 如何配置云服务端点？

在 `.env` 文件中设置 `OPENCLAW_CLOUD_ENDPOINT` 变量。

### 如何管理版本？

使用 `VersionManager` 服务来管理版本信息。可以通过 `incrementVersion()` 方法递增版本号。

### 离线模式

如果没有配置云服务端点，系统将在离线模式下运行，仅提供本地版本管理功能。

## 许可证

MIT
