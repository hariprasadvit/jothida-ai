const { withAndroidManifest } = require('@expo/config-plugins');

module.exports = function withAndroidNetworkConfig(config) {
  return withAndroidManifest(config, async (config) => {
    const androidManifest = config.modResults;
    const application = androidManifest.manifest.application[0];

    // Enable cleartext traffic
    application.$['android:usesCleartextTraffic'] = 'true';

    return config;
  });
};
