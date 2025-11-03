"""
Configuration management for the backup application.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict


class Config:
    """Manages application configuration."""
    
    DEFAULT_CONFIG = {
        "language": "hr",
        "theme": "dark",
        "start_with_windows": False,
        "start_minimized": False,
        "email_notifications": False,
        "sound_notifications": True,
        "notification_email": "",
        "smtp_server": "",
        "smtp_port": 587,
        "smtp_username": "",
        "smtp_password": "",
        "log_level": "INFO",
        "max_log_size_mb": 10,
        "backup_retention_days": 30,
    }
    
    def __init__(self, config_file: str = None):
        if config_file is None:
            self.config_dir = Path(__file__).parent.parent / "data"
            self.config_file = self.config_dir / "config.json"
        else:
            self.config_file = Path(config_file)
            self.config_dir = self.config_file.parent
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.settings = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**self.DEFAULT_CONFIG, **loaded}
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save()
            return self.DEFAULT_CONFIG.copy()
    
    def save(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a configuration value and save."""
        self.settings[key] = value
        self.save()
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple configuration values at once."""
        self.settings.update(updates)
        self.save()


# Global config instance
_config_instance = None


def get_config() -> Config:
    """Get or create the global config instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
