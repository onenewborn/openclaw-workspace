/**
 * Version Manager
 * 
 * Manages code versions for openclaw-related projects
 */

const fs = require('fs');
const path = require('path');

class VersionManager {
  constructor(config) {
    this.config = config;
    this.versionFile = config.versionFile || '.openclaw-version';
  }

  /**
   * Get current version information
   */
  getCurrentVersion() {
    try {
      if (fs.existsSync(this.versionFile)) {
        const content = fs.readFileSync(this.versionFile, 'utf8');
        return JSON.parse(content);
      }
    } catch (error) {
      console.warn('Unable to read version file:', error.message);
    }

    // Return default version info
    return {
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      branch: 'main',
      commit: null
    };
  }

  /**
   * Update version information
   */
  updateVersion(versionInfo) {
    const currentVersion = this.getCurrentVersion();
    const newVersion = {
      ...currentVersion,
      ...versionInfo,
      timestamp: new Date().toISOString()
    };

    try {
      fs.writeFileSync(
        this.versionFile,
        JSON.stringify(newVersion, null, 2),
        'utf8'
      );
      console.log('Version information updated successfully');
      return newVersion;
    } catch (error) {
      console.error('Failed to update version information:', error.message);
      throw error;
    }
  }

  /**
   * Get version history
   */
  getVersionHistory() {
    // In a real implementation, this would track version history
    // For now, return current version as a single-item history
    return [this.getCurrentVersion()];
  }

  /**
   * Compare versions
   */
  compareVersions(version1, version2) {
    const v1Parts = version1.split('.').map(Number);
    const v2Parts = version2.split('.').map(Number);

    for (let i = 0; i < Math.max(v1Parts.length, v2Parts.length); i++) {
      const v1 = v1Parts[i] || 0;
      const v2 = v2Parts[i] || 0;

      if (v1 > v2) return 1;
      if (v1 < v2) return -1;
    }

    return 0;
  }

  /**
   * Increment version
   */
  incrementVersion(type = 'patch') {
    const current = this.getCurrentVersion();
    const parts = current.version.split('.').map(Number);

    switch (type) {
      case 'major':
        parts[0]++;
        parts[1] = 0;
        parts[2] = 0;
        break;
      case 'minor':
        parts[1]++;
        parts[2] = 0;
        break;
      case 'patch':
      default:
        parts[2]++;
        break;
    }

    const newVersion = parts.join('.');
    return this.updateVersion({ version: newVersion });
  }
}

module.exports = VersionManager;
