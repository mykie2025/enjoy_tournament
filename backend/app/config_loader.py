"""
Configuration loader for the Tennis Tournament Analysis System.
Loads settings from config.yml file.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent


class ConfigLoader:
    """
    Loads and provides access to application configuration settings.
    """
    
    _instance = None
    _config = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one instance of ConfigLoader exists."""
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from config.yml file."""
        config_path = os.path.join(PROJECT_ROOT, 'config.yml')
        
        try:
            with open(config_path, 'r') as config_file:
                self._config = yaml.safe_load(config_file)
            print(f"Configuration loaded from {config_path}")
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            # Set default configuration
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration if config file cannot be loaded."""
        return {
            "server": {
                "api": {
                    "host": "localhost",
                    "port": 9000,
                    "debug": True,
                    "reload": True
                },
                "frontend": {
                    "host": "localhost",
                    "port": 9099,
                    "dev_mode": True
                }
            },
            "data_sources": {
                "sportradar": {
                    "base_url": "https://api.sportradar.com/tennis/production/v3",
                    "cache_duration_seconds": 21600
                },
                "local_db": {
                    "enabled": True,
                    "connection_string": "sqlite:///./tennis_tournament.db"
                }
            }
        }
    
    def get_config(self) -> Dict[str, Any]:
        """Return the entire configuration dictionary."""
        return self._config
    
    def get_api_config(self) -> Dict[str, Any]:
        """Return the API server configuration."""
        return self._config.get("server", {}).get("api", {})
    
    def get_frontend_config(self) -> Dict[str, Any]:
        """Return the frontend server configuration."""
        return self._config.get("server", {}).get("frontend", {})
    
    def get_data_source_config(self, source_name: str) -> Dict[str, Any]:
        """Return configuration for a specific data source."""
        return self._config.get("data_sources", {}).get(source_name, {})
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Return configuration for a specific agent."""
        return self._config.get("agents", {}).get(agent_name, {})
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Return the UI configuration."""
        return self._config.get("ui", {})


# Create a singleton instance
config = ConfigLoader()

# Export commonly used configurations
API_HOST = config.get_api_config().get("host", "localhost")
API_PORT = config.get_api_config().get("port", 9000)
API_DEBUG = config.get_api_config().get("debug", True)
API_RELOAD = config.get_api_config().get("reload", True)

FRONTEND_HOST = config.get_frontend_config().get("host", "localhost")
FRONTEND_PORT = config.get_frontend_config().get("port", 9099)

# Export the config instance for direct access
__all__ = ["config", "API_HOST", "API_PORT", "API_DEBUG", "API_RELOAD", 
           "FRONTEND_HOST", "FRONTEND_PORT"]
