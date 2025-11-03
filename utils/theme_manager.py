"""
Theme manager for dark/light mode support.
"""
import customtkinter as ctk
from typing import Literal, Dict, Tuple


class ThemeManager:
    """Manages application themes and color schemes."""
    
    # Color schemes
    COLORS = {
        "dark": {
            "bg_primary": "#1a1a1a",
            "bg_secondary": "#2b2b2b",
            "bg_tertiary": "#3a3a3a",
            "fg_primary": "#ffffff",
            "fg_secondary": "#b0b0b0",
            "accent": "#1f6aa5",
            "accent_hover": "#2980b9",
            "success": "#27ae60",
            "warning": "#f39c12",
            "error": "#e74c3c",
            "border": "#404040",
        },
        "light": {
            "bg_primary": "#f0f0f0",
            "bg_secondary": "#ffffff",
            "bg_tertiary": "#e8e8e8",
            "fg_primary": "#1a1a1a",
            "fg_secondary": "#5a5a5a",
            "accent": "#2980b9",
            "accent_hover": "#3498db",
            "success": "#27ae60",
            "warning": "#f39c12",
            "error": "#e74c3c",
            "border": "#d0d0d0",
        }
    }
    
    # Status colors (same for both themes)
    STATUS_COLORS = {
        "ok": "#27ae60",
        "running": "#3498db",
        "paused": "#95a5a6",
        "failed": "#e74c3c",
        "warning": "#f39c12",
        "completed": "#27ae60",
        "scheduled": "#9b59b6",
    }
    
    def __init__(self, default_theme: Literal["dark", "light", "system"] = "dark"):
        self.current_theme = default_theme
        self._apply_theme(default_theme)
    
    def _apply_theme(self, theme: Literal["dark", "light", "system"]):
        """Apply the selected theme to CustomTkinter."""
        if theme == "system":
            ctk.set_appearance_mode("system")
        elif theme == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    
    def set_theme(self, theme: Literal["dark", "light", "system"]):
        """Change the current theme."""
        self.current_theme = theme
        self._apply_theme(theme)
    
    def get_color(self, color_key: str) -> str:
        """
        Get color value for the current theme.
        
        Args:
            color_key: Color key (e.g., "bg_primary", "accent")
            
        Returns:
            Hex color code
        """
        # Determine actual theme (resolve "system")
        if self.current_theme == "system":
            actual_theme = ctk.get_appearance_mode().lower()
        else:
            actual_theme = self.current_theme
        
        return self.COLORS.get(actual_theme, self.COLORS["dark"]).get(
            color_key, "#000000"
        )
    
    def get_status_color(self, status: str) -> str:
        """Get color for a status indicator."""
        return self.STATUS_COLORS.get(status.lower(), "#95a5a6")
    
    def get_colors(self) -> Dict[str, str]:
        """Get all colors for the current theme."""
        if self.current_theme == "system":
            actual_theme = ctk.get_appearance_mode().lower()
        else:
            actual_theme = self.current_theme
        
        return self.COLORS.get(actual_theme, self.COLORS["dark"])


# Global theme manager instance
_theme_manager_instance = None


def get_theme_manager() -> ThemeManager:
    """Get or create the global theme manager instance."""
    global _theme_manager_instance
    if _theme_manager_instance is None:
        _theme_manager_instance = ThemeManager()
    return _theme_manager_instance
