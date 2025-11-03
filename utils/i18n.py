"""
Internationalization (i18n) module for multi-language support.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any


class I18n:
    """Manages translations and language switching."""
    
    def __init__(self, default_language: str = "hr"):
        self.current_language = default_language
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.locales_dir = Path(__file__).parent.parent / "locales"
        self._load_translations()
    
    def _load_translations(self):
        """Load all available translation files."""
        if not self.locales_dir.exists():
            print(f"Warning: Locales directory not found: {self.locales_dir}")
            return
        
        for locale_file in self.locales_dir.glob("*.json"):
            lang_code = locale_file.stem
            try:
                with open(locale_file, "r", encoding="utf-8") as f:
                    self.translations[lang_code] = json.load(f)
            except Exception as e:
                print(f"Error loading translation file {locale_file}: {e}")
    
    def set_language(self, language: str):
        """Change the current language."""
        if language in self.translations:
            self.current_language = language
        else:
            print(f"Warning: Language '{language}' not available. Using '{self.current_language}'.")
    
    def get(self, key: str, default: str = "") -> str:
        """
        Get translated text for a key using dot notation.
        
        Args:
            key: Translation key in dot notation (e.g., "dashboard.title")
            default: Default value if key not found
            
        Returns:
            Translated string or default value
        """
        keys = key.split(".")
        value = self.translations.get(self.current_language, {})
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default or key
        
        return value if isinstance(value, str) else default or key
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get list of available languages with their display names."""
        return {
            "hr": "Hrvatski",
            "en": "English"
        }
    
    def __call__(self, key: str, default: str = "") -> str:
        """Shorthand for get() method."""
        return self.get(key, default)


# Global i18n instance
_i18n_instance = None


def get_i18n() -> I18n:
    """Get or create the global i18n instance."""
    global _i18n_instance
    if _i18n_instance is None:
        _i18n_instance = I18n()
    return _i18n_instance


def t(key: str, default: str = "") -> str:
    """
    Shorthand translation function.
    
    Usage:
        from utils.i18n import t
        print(t("dashboard.title"))
    """
    return get_i18n().get(key, default)
