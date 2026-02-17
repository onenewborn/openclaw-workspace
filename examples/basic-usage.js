/**
 * Example: Basic Usage
 * 
 * This example demonstrates basic usage of the OpenClaw Workspace
 */

const OpenClawWorkspace = require('../src/index');

async function basicExample() {
  console.log('=== OpenClaw Workspace Basic Example ===\n');

  // Create workspace instance
  const workspace = new OpenClawWorkspace({
    cloudEndpoint: 'https://api.openclaw.cloud',
    apiKey: 'example-api-key'
  });

  try {
    // Initialize and connect
    await workspace.initialize();
    console.log('✓ Workspace initialized\n');

    // Get version information
    const versionInfo = await workspace.getVersionInfo();
    console.log('Version Information:');
    console.log(JSON.stringify(versionInfo, null, 2));
    console.log();

    // Sync with cloud
    const syncResult = await workspace.syncWithCloud();
    console.log('Sync Result:');
    console.log(JSON.stringify(syncResult, null, 2));
    console.log();

    // Disconnect
    await workspace.disconnect();
    console.log('✓ Disconnected from cloud service');

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

// Run the example
if (require.main === module) {
  basicExample();
}

module.exports = basicExample;
