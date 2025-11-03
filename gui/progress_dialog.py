"""
Progress dialog for backup operations.
"""
import customtkinter as ctk
from typing import Optional
from core.backup_engine import BackupProgress
from utils.i18n import t
import threading


class ProgressDialog(ctk.CTkToplevel):
    """Progress dialog for showing backup progress."""
    
    def __init__(self, parent, job_name: str):
        super().__init__(parent)
        
        self.job_name = job_name
        self.is_cancelled = False
        self.is_paused = False
        
        # Window setup
        self.title(f"{t('progress.title')} - {job_name}")
        self.geometry("700x550")
        self.minsize(600, 500)
        
        # Center window
        self.transient(parent)
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 700) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 550) // 2
        self.geometry(f"+{x}+{y}")
        
        # Prevent closing during backup
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI."""
        # Main container
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Overall Progress
        ctk.CTkLabel(
            main_frame,
            text=t("progress.overall_progress"),
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.overall_progress = ctk.CTkProgressBar(main_frame, height=25)
        self.overall_progress.pack(fill="x", pady=(0, 5))
        self.overall_progress.set(0)
        
        self.overall_label = ctk.CTkLabel(
            main_frame,
            text="0% (0 / 0 files)",
            font=ctk.CTkFont(size=12)
        )
        self.overall_label.pack(anchor="w", pady=(0, 20))
        
        # Current File
        ctk.CTkLabel(
            main_frame,
            text=t("progress.current_file"),
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.current_file_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=11),
            wraplength=640,
            anchor="w",
            justify="left"
        )
        self.current_file_label.pack(anchor="w", pady=(0, 10))
        
        self.file_progress = ctk.CTkProgressBar(main_frame, height=20)
        self.file_progress.pack(fill="x", pady=(0, 20))
        self.file_progress.set(0)
        
        # Statistics
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Left column
        left_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.speed_label = ctk.CTkLabel(
            left_frame,
            text=f"{t('progress.speed')}: 0 MB/s",
            font=ctk.CTkFont(size=12)
        )
        self.speed_label.pack(anchor="w", pady=2)
        
        self.elapsed_label = ctk.CTkLabel(
            left_frame,
            text=f"{t('progress.elapsed')}: 00:00:00",
            font=ctk.CTkFont(size=12)
        )
        self.elapsed_label.pack(anchor="w", pady=2)
        
        # Right column
        right_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        self.remaining_label = ctk.CTkLabel(
            right_frame,
            text=f"{t('progress.remaining')}: ~00:00:00",
            font=ctk.CTkFont(size=12)
        )
        self.remaining_label.pack(anchor="w", pady=2)
        
        self.processed_label = ctk.CTkLabel(
            right_frame,
            text=f"{t('progress.processed')}: 0 B / 0 B",
            font=ctk.CTkFont(size=12)
        )
        self.processed_label.pack(anchor="w", pady=2)
        
        # Recent Files
        ctk.CTkLabel(
            main_frame,
            text=t("progress.recent_files"),
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.recent_files_box = ctk.CTkTextbox(main_frame, height=100)
        self.recent_files_box.pack(fill="both", expand=True, pady=(0, 20))
        self.recent_files_box.configure(state="disabled")
        
        # Buttons
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        self.pause_button = ctk.CTkButton(
            buttons_frame,
            text=f"⏸ {t('progress.pause')}",
            command=self._toggle_pause,
            width=120
        )
        self.pause_button.pack(side="left", padx=5)
        
        self.stop_button = ctk.CTkButton(
            buttons_frame,
            text=f"⏹ {t('progress.stop')}",
            command=self._stop_backup,
            width=120,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.stop_button.pack(side="left", padx=5)
        
        self.minimize_button = ctk.CTkButton(
            buttons_frame,
            text=t("progress.minimize"),
            command=self._minimize,
            width=120
        )
        self.minimize_button.pack(side="right", padx=5)
    
    def update_progress(self, progress: BackupProgress):
        """Update progress display."""
        try:
            # Overall progress
            percent = progress.get_progress_percent()
            self.overall_progress.set(percent / 100)
            self.overall_label.configure(
                text=f"{percent:.1f}% ({progress.processed_files} / {progress.total_files} files)"
            )
            
            # Current file
            if progress.current_file:
                # Shorten path if too long
                file_path = progress.current_file
                if len(file_path) > 80:
                    file_path = "..." + file_path[-77:]
                self.current_file_label.configure(text=file_path)
                
                # File progress (if available)
                if progress.current_file_size > 0:
                    file_percent = (progress.current_file_processed / progress.current_file_size) * 100
                    self.file_progress.set(file_percent / 100)
                else:
                    self.file_progress.set(0)
            
            # Statistics
            speed = progress.get_speed_mbps()
            self.speed_label.configure(text=f"{t('progress.speed')}: {speed:.2f} MB/s")
            
            if progress.start_time:
                from datetime import datetime
                elapsed = (datetime.now() - progress.start_time).total_seconds()
                hours, remainder = divmod(int(elapsed), 3600)
                minutes, seconds = divmod(remainder, 60)
                self.elapsed_label.configure(
                    text=f"{t('progress.elapsed')}: {hours:02d}:{minutes:02d}:{seconds:02d}"
                )
            
            eta = progress.get_eta_seconds()
            hours, remainder = divmod(eta, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.remaining_label.configure(
                text=f"{t('progress.remaining')}: ~{hours:02d}:{minutes:02d}:{seconds:02d}"
            )
            
            processed_mb = progress.processed_size / (1024 * 1024)
            total_mb = progress.total_size / (1024 * 1024)
            self.processed_label.configure(
                text=f"{t('progress.processed')}: {processed_mb:.1f} MB / {total_mb:.1f} MB"
            )
            
            # Recent files (show last 5)
            if progress.current_file:
                self.recent_files_box.configure(state="normal")
                
                # Get current content
                content = self.recent_files_box.get("1.0", "end").strip().split("\n")
                
                # Add new file
                file_name = progress.current_file.split("\\")[-1]
                status = "✓" if progress.current_file_processed == progress.current_file_size else "⏳"
                new_line = f"{status} {file_name}"
                
                # Keep only last 5 lines
                if len(content) >= 5:
                    content = content[-4:]
                
                content.append(new_line)
                
                # Update textbox
                self.recent_files_box.delete("1.0", "end")
                self.recent_files_box.insert("1.0", "\n".join(content))
                self.recent_files_box.configure(state="disabled")
            
            # Update window
            self.update()
            
        except Exception as e:
            print(f"Error updating progress: {e}")
    
    def _toggle_pause(self):
        """Toggle pause state."""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.configure(text=f"▶ Resume")
        else:
            self.pause_button.configure(text=f"⏸ {t('progress.pause')}")
    
    def _stop_backup(self):
        """Stop the backup."""
        from tkinter import messagebox
        if messagebox.askyesno(
            t("app_title"),
            t("messages.confirm_stop")
        ):
            self.is_cancelled = True
            self.destroy()
    
    def _minimize(self):
        """Minimize window."""
        self.iconify()
    
    def _on_closing(self):
        """Handle window close."""
        self._stop_backup()
    
    def show_completion(self, success: bool, message: str):
        """Show completion message."""
        from tkinter import messagebox
        
        if success:
            messagebox.showinfo(
                t("app_title"),
                t("messages.backup_completed")
            )
        else:
            messagebox.showerror(
                t("app_title"),
                t("messages.backup_failed") + f"\n\n{message}"
            )
        
        self.destroy()
