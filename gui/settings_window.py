"""
Settings window for application configuration.
"""
import customtkinter as ctk
from typing import Callable
from utils.config import get_config
from utils.i18n import get_i18n, t


class SettingsWindow(ctk.CTkToplevel):
    """Settings dialog."""
    
    def __init__(self, parent, on_save: Callable):
        super().__init__(parent)
        
        self.on_save = on_save
        self.config = get_config()
        self.i18n = get_i18n()
        
        # Window setup
        self.title(t("settings.title"))
        self.geometry("600x500")
        
        # Center window
        self.transient(parent)
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 600) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 500) // 2
        self.geometry(f"+{x}+{y}")
        
        self._create_ui()
        self._load_settings()
    
    def _create_ui(self):
        """Create the UI."""
        # Main container
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            main_frame,
            text=t("settings.title"),
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(0, 20))
        
        # Settings content
        content = ctk.CTkScrollableFrame(main_frame)
        content.pack(fill="both", expand=True, pady=(0, 20))
        
        # General section
        self._create_section(content, t("settings.general"))
        
        # Language
        lang_frame = self._create_setting_row(content, t("settings.language"))
        self.language_var = ctk.StringVar(value=self.config.get("language", "hr"))
        
        languages = self.i18n.get_available_languages()
        ctk.CTkOptionMenu(
            lang_frame,
            variable=self.language_var,
            values=list(languages.values()),
            width=200
        ).pack(side="right")
        
        # Theme
        theme_frame = self._create_setting_row(content, t("settings.theme"))
        self.theme_var = ctk.StringVar(value=self.config.get("theme", "dark"))
        
        ctk.CTkOptionMenu(
            theme_frame,
            variable=self.theme_var,
            values=[t("settings.light"), t("settings.dark"), t("settings.system")],
            width=200
        ).pack(side="right")
        
        # Notifications section
        self._create_section(content, t("settings.notifications"))
        
        # Email notifications
        email_frame = self._create_setting_row(content, t("settings.email_notifications"))
        self.email_notif_var = ctk.BooleanVar(value=self.config.get("email_notifications", False))
        ctk.CTkSwitch(
            email_frame,
            text="",
            variable=self.email_notif_var
        ).pack(side="right")
        
        # Sound notifications
        sound_frame = self._create_setting_row(content, t("settings.sound_notifications"))
        self.sound_notif_var = ctk.BooleanVar(value=self.config.get("sound_notifications", True))
        ctk.CTkSwitch(
            sound_frame,
            text="",
            variable=self.sound_notif_var
        ).pack(side="right")
        
        # Startup section
        self._create_section(content, t("settings.startup"))
        
        # Start with Windows
        startup_frame = self._create_setting_row(content, t("settings.start_with_windows"))
        self.start_windows_var = ctk.BooleanVar(value=self.config.get("start_with_windows", False))
        ctk.CTkSwitch(
            startup_frame,
            text="",
            variable=self.start_windows_var
        ).pack(side="right")
        
        # Start minimized
        minimized_frame = self._create_setting_row(content, t("settings.start_minimized"))
        self.start_minimized_var = ctk.BooleanVar(value=self.config.get("start_minimized", False))
        ctk.CTkSwitch(
            minimized_frame,
            text="",
            variable=self.start_minimized_var
        ).pack(side="right")
        
        # Buttons
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        ctk.CTkButton(
            buttons_frame,
            text=t("common.cancel"),
            command=self.destroy,
            width=120,
            fg_color="gray",
            hover_color="#5a5a5a"
        ).pack(side="left")
        
        ctk.CTkButton(
            buttons_frame,
            text=t("settings.apply"),
            command=self._save_settings,
            width=120,
            fg_color="#27ae60",
            hover_color="#229954"
        ).pack(side="right")
    
    def _create_section(self, parent, title: str):
        """Create a section header."""
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", pady=(20, 10))
        
        ctk.CTkLabel(
            section_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")
        
        # Separator
        separator = ctk.CTkFrame(section_frame, height=2, fg_color="gray")
        separator.pack(fill="x", pady=(5, 0))
    
    def _create_setting_row(self, parent, label: str):
        """Create a setting row."""
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", pady=8)
        
        ctk.CTkLabel(
            row_frame,
            text=label,
            font=ctk.CTkFont(size=13)
        ).pack(side="left")
        
        return row_frame
    
    def _load_settings(self):
        """Load current settings."""
        # Settings are loaded via default values in _create_ui
        pass
    
    def _save_settings(self):
        """Save settings."""
        # Map display names back to codes
        lang_map = {v: k for k, v in self.i18n.get_available_languages().items()}
        theme_map = {
            t("settings.light"): "light",
            t("settings.dark"): "dark",
            t("settings.system"): "system"
        }
        
        language = lang_map.get(self.language_var.get(), "hr")
        theme = theme_map.get(self.theme_var.get(), "dark")
        
        self.config.update({
            "language": language,
            "theme": theme,
            "email_notifications": self.email_notif_var.get(),
            "sound_notifications": self.sound_notif_var.get(),
            "start_with_windows": self.start_windows_var.get(),
            "start_minimized": self.start_minimized_var.get()
        })
        
        if self.on_save:
            self.on_save()
        
        self.destroy()
