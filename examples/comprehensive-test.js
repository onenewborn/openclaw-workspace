/**
 * Comprehensive Test
 * 
 * Tests all features of the OpenClaw Workspace
 */

const OpenClawWorkspace = require('../src/index');

async function comprehensiveTest() {
  console.log('=== OpenClaw Workspace Comprehensive Test ===\n');

  // Test 1: Offline Mode
  console.log('Test 1: Offline Mode');
  const offlineWorkspace = new OpenClawWorkspace({});
  try {
    await offlineWorkspace.initialize();
    console.log('✓ Offline mode works correctly\n');
  } catch (error) {
    console.error('✗ Offline mode failed:', error.message);
    process.exit(1);
  }

  // Test 2: Online Mode
  console.log('Test 2: Online Mode');
  const onlineWorkspace = new OpenClawWorkspace({
    cloudEndpoint: 'https://api.openclaw.cloud',
    apiKey: 'test-key'
  });
  
  try {
    await onlineWorkspace.initialize();
    console.log('✓ Online mode initialized\n');
  } catch (error) {
    console.error('✗ Online mode failed:', error.message);
    process.exit(1);
  }

  // Test 3: Version Management
  console.log('Test 3: Version Management');
  try {
    const version = await onlineWorkspace.getVersionInfo();
    if (version && version.version) {
      console.log('✓ Version info retrieved:', version.version, '\n');
    } else {
      throw new Error('Invalid version info');
    }
  } catch (error) {
    console.error('✗ Version management failed:', error.message);
    process.exit(1);
  }

  // Test 4: Cloud Sync (Online)
  console.log('Test 4: Cloud Sync (Online)');
  try {
    const syncResult = await onlineWorkspace.syncWithCloud();
    if (syncResult && syncResult.success) {
      console.log('✓ Cloud sync successful\n');
    } else {
      throw new Error('Sync failed');
    }
  } catch (error) {
    console.error('✗ Cloud sync failed:', error.message);
    process.exit(1);
  }

  // Test 5: Cloud Sync (Offline)
  console.log('Test 5: Cloud Sync (Offline - should handle gracefully)');
  try {
    const syncResult = await offlineWorkspace.syncWithCloud();
    if (!syncResult.success && syncResult.error === 'Not connected') {
      console.log('✓ Offline sync handled gracefully\n');
    } else {
      throw new Error('Offline sync should fail gracefully');
    }
  } catch (error) {
    console.error('✗ Offline sync handling failed:', error.message);
    process.exit(1);
  }

  // Test 6: Disconnect
  console.log('Test 6: Disconnect');
  try {
    await onlineWorkspace.disconnect();
    console.log('✓ Disconnected successfully\n');
  } catch (error) {
    console.error('✗ Disconnect failed:', error.message);
    process.exit(1);
  }

  console.log('=== All Tests Passed! ===');
}

// Run tests
if (require.main === module) {
  comprehensiveTest().catch(error => {
    console.error('Test suite failed:', error);
    process.exit(1);
  });
}

module.exports = comprehensiveTest;
