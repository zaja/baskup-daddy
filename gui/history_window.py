"""
History window for viewing backup history and restore operations.
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from pathlib import Path
from datetime import datetime
import json
from typing import Optional, List, Dict, Any
from utils.i18n import t


class HistoryWindow(ctk.CTkToplevel):
    """History window for backup management."""
    
    def __init__(self, parent, job_name: str, destination_path: str):
        super().__init__(parent)
        
        self.job_name = job_name
        self.destination_path = destination_path
        self.backups = []
        
        # Window setup
        self.title(f"{t('history.title')} - {job_name}")
        self.geometry("900x600")
        self.minsize(800, 500)
        
        # Center window
        self.transient(parent)
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 900) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 600) // 2
        self.geometry(f"+{x}+{y}")
        
        self._create_ui()
        self._load_backups()
    
    def _create_ui(self):
        """Create the UI."""
        # Main container
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        ctk.CTkLabel(
            main_frame,
            text=f"{t('history.backup_history')} - {self.job_name}",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(0, 20))
        
        # Info frame
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            info_frame,
            text=f"{t('history.destination')}: {self.destination_path}",
            font=ctk.CTkFont(size=12)
        ).pack(padx=15, pady=10, anchor="w")
        
        # Backups list
        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Headers
        headers_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        headers_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        headers = [
            (t("history.date"), 0.25),
            (t("history.type"), 0.15),
            (t("history.files"), 0.15),
            (t("history.size"), 0.15),
            (t("history.status"), 0.15),
            (t("history.actions"), 0.15)
        ]
        
        for header, weight in headers:
            ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(side="left", expand=True, fill="x", padx=5)
        
        # Scrollable frame for backups
        self.backups_frame = ctk.CTkScrollableFrame(list_frame, height=300)
        self.backups_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Buttons
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        ctk.CTkButton(
            buttons_frame,
            text=t("history.refresh"),
            command=self._load_backups,
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text=t("history.open_folder"),
            command=self._open_destination_folder,
            width=150
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text=t("common.close"),
            command=self.destroy,
            width=120
        ).pack(side="right", padx=5)
    
    def _load_backups(self):
        """Load backup history."""
        # Clear existing
        for widget in self.backups_frame.winfo_children():
            widget.destroy()
        
        self.backups = []
        
        # Get job folder
        dest = Path(self.destination_path)
        
        # Sanitize job name
        folder_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in self.job_name)
        folder_name = folder_name.strip().replace(' ', '_')
        
        job_folder = dest / folder_name
        
        if not job_folder.exists():
            ctk.CTkLabel(
                self.backups_frame,
                text=t("history.no_backups"),
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
            return
        
        # Find all backup files and metadata
        backup_files = []
        
        # Find ZIP files
        for zip_file in job_folder.glob("backup_*.zip"):
            timestamp = zip_file.stem.replace("backup_", "")
            metadata_file = job_folder / f"backup_{timestamp}_metadata.json"
            
            metadata = {}
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                except:
                    pass
            
            backup_files.append({
                "path": str(zip_file),
                "timestamp": timestamp,
                "metadata": metadata,
                "type": "ZIP"
            })
        
        # Find backup folders
        for backup_dir in job_folder.glob("backup_*"):
            if backup_dir.is_dir():
                timestamp = backup_dir.name.replace("backup_", "")
                metadata_file = job_folder / f"backup_{timestamp}_metadata.json"
                
                metadata = {}
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                    except:
                        pass
                
                backup_files.append({
                    "path": str(backup_dir),
                    "timestamp": timestamp,
                    "metadata": metadata,
                    "type": "Folder"
                })
        
        # Sort by timestamp (newest first)
        backup_files.sort(key=lambda x: x["timestamp"], reverse=True)
        self.backups = backup_files
        
        if not backup_files:
            ctk.CTkLabel(
                self.backups_frame,
                text=t("history.no_backups"),
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
            return
        
        # Display backups
        for backup in backup_files:
            self._create_backup_row(backup)
    
    def _create_backup_row(self, backup: Dict[str, Any]):
        """Create a row for a backup."""
        row_frame = ctk.CTkFrame(self.backups_frame)
        row_frame.pack(fill="x", pady=2, padx=5)
        
        # Parse timestamp
        try:
            dt = datetime.strptime(backup["timestamp"], "%Y%m%d_%H%M%S")
            date_str = dt.strftime("%d.%m.%Y %H:%M")
        except:
            date_str = backup["timestamp"]
        
        # Get metadata
        metadata = backup.get("metadata", {})
        files_count = metadata.get("total_files", "?")
        size_mb = metadata.get("total_size", 0) / (1024 * 1024)
        
        # Date
        ctk.CTkLabel(
            row_frame,
            text=date_str,
            font=ctk.CTkFont(size=11)
        ).pack(side="left", expand=True, fill="x", padx=5)
        
        # Type
        ctk.CTkLabel(
            row_frame,
            text=backup["type"],
            font=ctk.CTkFont(size=11)
        ).pack(side="left", expand=True, fill="x", padx=5)
        
        # Files
        ctk.CTkLabel(
            row_frame,
            text=str(files_count),
            font=ctk.CTkFont(size=11)
        ).pack(side="left", expand=True, fill="x", padx=5)
        
        # Size
        ctk.CTkLabel(
            row_frame,
            text=f"{size_mb:.1f} MB",
            font=ctk.CTkFont(size=11)
        ).pack(side="left", expand=True, fill="x", padx=5)
        
        # Status
        status = "✓ OK" if Path(backup["path"]).exists() else "✗ Missing"
        ctk.CTkLabel(
            row_frame,
            text=status,
            font=ctk.CTkFont(size=11),
            text_color="green" if "✓" in status else "red"
        ).pack(side="left", expand=True, fill="x", padx=5)
        
        # Actions
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.pack(side="left", expand=True, fill="x", padx=5)
        
        ctk.CTkButton(
            actions_frame,
            text="📂",
            command=lambda: self._open_backup(backup["path"]),
            width=40,
            height=28
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            actions_frame,
            text="↻",
            command=lambda: self._restore_backup(backup),
            width=40,
            height=28
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            actions_frame,
            text="🗑",
            command=lambda: self._delete_backup(backup),
            width=40,
            height=28,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", padx=2)
    
    def _open_backup(self, path: str):
        """Open backup location."""
        import subprocess
        backup_path = Path(path)
        
        if backup_path.exists():
            if backup_path.is_file():
                # Open parent folder and select file
                subprocess.run(['explorer', '/select,', str(backup_path)])
            else:
                # Open folder
                subprocess.run(['explorer', str(backup_path)])
        else:
            messagebox.showerror(
                t("app_title"),
                t("history.backup_not_found")
            )
    
    def _restore_backup(self, backup: Dict[str, Any]):
        """Restore backup to a location."""
        # Ask for restore location
        restore_path = filedialog.askdirectory(
            title=t("history.select_restore_location")
        )
        
        if not restore_path:
            return
        
        # Confirm
        if not messagebox.askyesno(
            t("app_title"),
            t("history.confirm_restore")
        ):
            return
        
        # TODO: Implement restore functionality
        messagebox.showinfo(
            t("app_title"),
            t("history.restore_not_implemented")
        )
    
    def _delete_backup(self, backup: Dict[str, Any]):
        """Delete a backup."""
        if not messagebox.askyesno(
            t("app_title"),
            t("history.confirm_delete")
        ):
            return
        
        try:
            backup_path = Path(backup["path"])
            
            # Delete backup file/folder
            if backup_path.is_file():
                backup_path.unlink()
            elif backup_path.is_dir():
                import shutil
                shutil.rmtree(backup_path)
            
            # Delete metadata file
            timestamp = backup["timestamp"]
            job_folder = backup_path.parent
            metadata_file = job_folder / f"backup_{timestamp}_metadata.json"
            if metadata_file.exists():
                metadata_file.unlink()
            
            messagebox.showinfo(
                t("app_title"),
                t("history.delete_success")
            )
            
            # Refresh list
            self._load_backups()
            
        except Exception as e:
            messagebox.showerror(
                t("app_title"),
                f"{t('history.delete_failed')}\n\n{str(e)}"
            )
    
    def _open_destination_folder(self):
        """Open destination folder."""
        import subprocess
        dest = Path(self.destination_path)
        
        # Sanitize job name
        folder_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in self.job_name)
        folder_name = folder_name.strip().replace(' ', '_')
        
        job_folder = dest / folder_name
        
        if job_folder.exists():
            subprocess.run(['explorer', str(job_folder)])
        else:
            subprocess.run(['explorer', str(dest)])
