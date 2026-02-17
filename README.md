# OpenClaw Workspace

用于与连接在云端的openclaw服务联动，管理与openclaw相关的代码版本。

A workspace for managing openclaw-related code versions and interfacing with cloud-based openclaw services.

## Features

- **Cloud Service Integration**: Connect and sync with cloud-based openclaw services
- **Version Management**: Track and manage code versions for openclaw projects
- **Configuration Management**: Flexible configuration options for different environments
- **Modular Architecture**: Clean separation of concerns with service-oriented design

## Installation

```bash
npm install
```

## Configuration

Copy the example environment file and configure your settings:

```bash
cp config/example.env .env
```

Edit `.env` with your configuration:
- `OPENCLAW_CLOUD_ENDPOINT`: Your openclaw cloud service endpoint
- `OPENCLAW_API_KEY`: Your API key for authentication
- `OPENCLAW_VERSION_FILE`: Location of version tracking file (default: `.openclaw-version`)

## Usage

### Running Tests

Run the comprehensive test suite:

```bash
node examples/comprehensive-test.js
```

This will test:
- Offline mode functionality
- Online mode with cloud connection
- Version management
- Cloud synchronization (both online and offline)
- Graceful error handling

### As a CLI Tool

Run the workspace directly:

```bash
npm start
```

Or with Node.js:

```bash
node src/index.js
```

### As a Module

```javascript
const OpenClawWorkspace = require('./src/index');

// Initialize workspace
const workspace = new OpenClawWorkspace({
  cloudEndpoint: 'https://api.openclaw.cloud',
  apiKey: 'your-api-key'
});

// Connect and initialize
await workspace.initialize();

// Get version information
const versionInfo = await workspace.getVersionInfo();
console.log('Current version:', versionInfo);

// Sync with cloud
await workspace.syncWithCloud();

// Disconnect when done
await workspace.disconnect();
```

## Project Structure

```
openclaw-workspace/
├── src/
│   ├── index.js                    # Main entry point
│   └── services/
│       ├── cloud-service.js        # Cloud service integration
│       └── version-manager.js      # Version management
├── config/
│   ├── default.json                # Default configuration
│   └── example.env                 # Environment variables example
├── docs/                           # Documentation
├── examples/                       # Usage examples
├── package.json                    # Project metadata
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## Services

### CloudService

Handles communication with the cloud-based openclaw service:
- `connect()`: Establish connection to cloud service
- `disconnect()`: Close connection to cloud service
- `sync()`: Synchronize data with cloud
- `sendData(data)`: Send data to cloud
- `receiveData()`: Receive data from cloud
- `isConnected()`: Check connection status

### VersionManager

Manages code versions for openclaw projects:
- `getCurrentVersion()`: Get current version information
- `updateVersion(versionInfo)`: Update version information
- `getVersionHistory()`: Get version history
- `compareVersions(v1, v2)`: Compare two version strings
- `incrementVersion(type)`: Increment version (major, minor, or patch)

## Examples

See the `examples/` directory for usage examples:

- `basic-usage.js` - Basic workspace operations
- `version-management.js` - Version management features
- `comprehensive-test.js` - Full test suite demonstrating all features

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.