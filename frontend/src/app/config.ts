/**
 * Frontend configuration for the Tennis Tournament Analysis System
 * Loads settings from the project's config.yml file
 */

// Default configuration values
const defaultConfig = {
  apiServer: {
    host: 'localhost',
    port: 9000,
    baseUrl: 'http://localhost:9000'
  },
  ui: {
    autoRefreshInterval: 300, // 5 minutes in seconds
    matchDisplayLimit: 10,
    tournamentDisplayLimit: 5
  }
};

// Get environment variables with proper type checking
const getEnvVar = (name: string, defaultValue: string): string => 
  typeof process !== 'undefined' && process.env ? 
    (process.env[name] || defaultValue) : defaultValue;

const getEnvVarInt = (name: string, defaultValue: number): number => {
  const value = getEnvVar(name, defaultValue.toString());
  const parsed = parseInt(value, 10);
  return isNaN(parsed) ? defaultValue : parsed;
};

// Configuration object
const config = {
  apiServer: {
    host: getEnvVar('NEXT_PUBLIC_API_HOST', defaultConfig.apiServer.host),
    port: getEnvVarInt('NEXT_PUBLIC_API_PORT', defaultConfig.apiServer.port),
    get baseUrl() {
      return `http://${this.host}:${this.port}`;
    }
  },
  ui: {
    autoRefreshInterval: getEnvVarInt('NEXT_PUBLIC_AUTO_REFRESH_INTERVAL', defaultConfig.ui.autoRefreshInterval),
    matchDisplayLimit: getEnvVarInt('NEXT_PUBLIC_MATCH_DISPLAY_LIMIT', defaultConfig.ui.matchDisplayLimit),
    tournamentDisplayLimit: getEnvVarInt('NEXT_PUBLIC_TOURNAMENT_DISPLAY_LIMIT', defaultConfig.ui.tournamentDisplayLimit)
  }
};

export default config;
