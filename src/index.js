/**
 * OpenClaw Workspace - Main Entry Point
 * 
 * This workspace is used to manage code versions related to openclaw
 * and interface with cloud-based openclaw services.
 */

const CloudService = require('./services/cloud-service');
const VersionManager = require('./services/version-manager');

class OpenClawWorkspace {
  constructor(config = {}) {
    this.config = {
      cloudEndpoint: config.cloudEndpoint || process.env.OPENCLAW_CLOUD_ENDPOINT,
      apiKey: config.apiKey || process.env.OPENCLAW_API_KEY,
      ...config
    };
    
    this.cloudService = new CloudService(this.config);
    this.versionManager = new VersionManager(this.config);
  }

  /**
   * Initialize the workspace
   */
  async initialize() {
    console.log('Initializing OpenClaw Workspace...');
    
    // Connect to cloud service
    const connected = await this.cloudService.connect();
    if (!connected) {
      throw new Error('Failed to connect to OpenClaw cloud service');
    }
    
    console.log('OpenClaw Workspace initialized successfully');
    return true;
  }

  /**
   * Get version information
   */
  async getVersionInfo() {
    return this.versionManager.getCurrentVersion();
  }

  /**
   * Sync with cloud service
   */
  async syncWithCloud() {
    return this.cloudService.sync();
  }

  /**
   * Disconnect from cloud service
   */
  async disconnect() {
    await this.cloudService.disconnect();
    console.log('Disconnected from OpenClaw cloud service');
  }
}

module.exports = OpenClawWorkspace;

// CLI usage
if (require.main === module) {
  const workspace = new OpenClawWorkspace();
  
  workspace.initialize()
    .then(() => {
      console.log('Workspace ready for use');
      return workspace.getVersionInfo();
    })
    .then(versionInfo => {
      console.log('Current version:', versionInfo);
    })
    .catch(error => {
      console.error('Error:', error.message);
      process.exit(1);
    });
}
