# API Documentation

## OpenClawWorkspace

The main class for managing the openclaw workspace.

### Constructor

```javascript
new OpenClawWorkspace(config)
```

**Parameters:**
- `config` (Object): Configuration options
  - `cloudEndpoint` (String): Cloud service endpoint URL
  - `apiKey` (String): API key for authentication
  - `versionFile` (String): Path to version file (optional)

**Example:**
```javascript
const workspace = new OpenClawWorkspace({
  cloudEndpoint: 'https://api.openclaw.cloud',
  apiKey: 'your-api-key'
});
```

### Methods

#### initialize()

Initialize the workspace and connect to cloud service.

**Returns:** `Promise<Boolean>` - True if initialization successful

**Example:**
```javascript
await workspace.initialize();
```

#### getVersionInfo()

Get current version information.

**Returns:** `Promise<Object>` - Version information object

**Example:**
```javascript
const versionInfo = await workspace.getVersionInfo();
// { version: '1.0.0', timestamp: '...', branch: 'main', commit: null }
```

#### syncWithCloud()

Synchronize with cloud service.

**Returns:** `Promise<Object>` - Sync result object

**Example:**
```javascript
const result = await workspace.syncWithCloud();
// { success: true, timestamp: '...' }
```

#### disconnect()

Disconnect from cloud service.

**Returns:** `Promise<void>`

**Example:**
```javascript
await workspace.disconnect();
```

---

## CloudService

Handles communication with cloud-based openclaw service.

### Constructor

```javascript
new CloudService(config)
```

**Parameters:**
- `config` (Object): Configuration options
  - `cloudEndpoint` (String): Cloud service endpoint URL
  - `apiKey` (String): API key for authentication

### Methods

#### connect()

Connect to the cloud service.

**Returns:** `Promise<Boolean>` - True if connection successful

#### disconnect()

Disconnect from the cloud service.

**Returns:** `Promise<void>`

#### sync()

Sync data with cloud service.

**Returns:** `Promise<Object>` - Sync result

**Throws:** Error if not connected

#### sendData(data)

Send data to cloud service.

**Parameters:**
- `data` (Any): Data to send

**Returns:** `Promise<Object>` - Send result

**Throws:** Error if not connected

#### receiveData()

Receive data from cloud service.

**Returns:** `Promise<Object>` - Received data

**Throws:** Error if not connected

#### isConnected()

Check connection status.

**Returns:** `Boolean` - True if connected

---

## VersionManager

Manages code versions for openclaw projects.

### Constructor

```javascript
new VersionManager(config)
```

**Parameters:**
- `config` (Object): Configuration options
  - `versionFile` (String): Path to version file

### Methods

#### getCurrentVersion()

Get current version information.

**Returns:** `Object` - Version information
- `version` (String): Version string (semver format)
- `timestamp` (String): ISO timestamp
- `branch` (String): Git branch name
- `commit` (String): Git commit hash (optional)

#### updateVersion(versionInfo)

Update version information.

**Parameters:**
- `versionInfo` (Object): Version information to update

**Returns:** `Object` - Updated version information

**Throws:** Error if unable to write file

#### getVersionHistory()

Get version history.

**Returns:** `Array<Object>` - Array of version information objects

#### compareVersions(version1, version2)

Compare two version strings.

**Parameters:**
- `version1` (String): First version (semver format)
- `version2` (String): Second version (semver format)

**Returns:** `Number` - -1 if v1 < v2, 0 if v1 == v2, 1 if v1 > v2

#### incrementVersion(type)

Increment version number.

**Parameters:**
- `type` (String): Version increment type ('major', 'minor', or 'patch')

**Returns:** `Object` - Updated version information
