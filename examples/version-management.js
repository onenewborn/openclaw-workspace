/**
 * Example: Version Management
 * 
 * This example demonstrates version management features
 */

const VersionManager = require('../src/services/version-manager');

async function versionExample() {
  console.log('=== OpenClaw Version Management Example ===\n');

  // Create version manager
  const versionManager = new VersionManager({
    versionFile: '.openclaw-version-example'
  });

  // Get current version
  console.log('Current Version:');
  const currentVersion = versionManager.getCurrentVersion();
  console.log(JSON.stringify(currentVersion, null, 2));
  console.log();

  // Increment patch version
  console.log('Incrementing patch version...');
  const patchVersion = versionManager.incrementVersion('patch');
  console.log('New Version:', patchVersion.version);
  console.log();

  // Increment minor version
  console.log('Incrementing minor version...');
  const minorVersion = versionManager.incrementVersion('minor');
  console.log('New Version:', minorVersion.version);
  console.log();

  // Compare versions
  console.log('Comparing versions:');
  const comparison = versionManager.compareVersions('1.0.0', '2.0.0');
  console.log('1.0.0 vs 2.0.0:', comparison < 0 ? '1.0.0 is older' : '1.0.0 is newer');
  console.log();

  // Get version history
  console.log('Version History:');
  const history = versionManager.getVersionHistory();
  console.log(JSON.stringify(history, null, 2));
}

// Run the example
if (require.main === module) {
  versionExample();
}

module.exports = versionExample;
