import json
import os
from pathlib import Path

class ConfigService:
    def __init__(self):
        self.config_dir = Path.home() / '.resume-filler'
        self.config_file = self.config_dir / 'config.json'
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.save_config({})

    def load_config(self) -> dict:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}

    def save_config(self, config: dict):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def update_config(self, key: str, value: str):
        """Update a specific configuration value"""
        config = self.load_config()
        config[key] = value
        self.save_config(config)

config_service = ConfigService()
