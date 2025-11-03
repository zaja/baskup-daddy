"""
Main application window with dashboard.
"""
import customtkinter as ctk
from typing import Optional
from utils.i18n import get_i18n, t
from utils.theme_manager import get_theme_manager
from utils.config import get_config
from core.job_manager import get_job_manager, BackupJob
from core.scheduler import BackupScheduler
from gui.job_editor import JobEditorWindow
from gui.settings_window import SettingsWindow
import tkinter as tk
from tkinter import messagebox


class DashboardCard(ctk.CTkFrame):
    """Dashboard statistics card."""
    
    def __init__(self, parent, title: str, value: str, icon: str = "📊"):
        super().__init__(parent, corner_radius=10)
        
        self.icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=ctk.CTkFont(size=32)
        )
        self.icon_label.pack(pady=(15, 5))
        
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.value_label.pack(pady=5)
        
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.title_label.pack(pady=(5, 15))
    
    def update_value(self, value: str):
        """Update card value."""
        self.value_label.configure(text=value)


class JobRow(ctk.CTkFrame):
    """Single job row in the jobs table."""
    
    def __init__(self, parent, job: BackupJob, on_run, on_edit, on_delete):
        super().__init__(parent, corner_radius=5, fg_color="transparent")
        
        self.job = job
        self.on_run = on_run
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        # Configure grid
        self.grid_columnconfigure(0, weight=2)  # Name
        self.grid_columnconfigure(1, weight=1)  # Status
        self.grid_columnconfigure(2, weight=1)  # Last Run
        self.grid_columnconfigure(3, weight=1)  # Next Run
        self.grid_columnconfigure(4, weight=1)  # Actions
        
        # Name with icon
        icon = "📁"
        name_frame = ctk.CTkFrame(self, fg_color="transparent")
        name_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        ctk.CTkLabel(
            name_frame,
            text=f"{icon} {job.name}",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left")
        
        # Status
        status_color = self._get_status_color(job.status)
        status_text = t(f"status.{job.status}")
        
        status_label = ctk.CTkLabel(
            self,
            text=f"● {status_text}",
            text_color=status_color,
            font=ctk.CTkFont(size=12)
        )
        status_label.grid(row=0, column=1, padx=10, pady=5)
        
        # Last Run
        last_run = job.last_run if job.last_run else "-"
        if job.last_run:
            from datetime import datetime
            try:
                dt = datetime.fromisoformat(job.last_run)
                last_run = dt.strftime("%d.%m. %H:%M")
            except:
                pass
        
        ctk.CTkLabel(
            self,
            text=last_run,
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=2, padx=10, pady=5)
        
        # Next Run
        next_run = job.next_run if job.next_run else "-"
        ctk.CTkLabel(
            self,
            text=next_run,
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=3, padx=10, pady=5)
        
        # Actions
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=0, column=4, padx=10, pady=5)
        
        ctk.CTkButton(
            actions_frame,
            text="▶",
            width=30,
            command=lambda: self.on_run(job.job_id)
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            actions_frame,
            text="✏",
            width=30,
            command=lambda: self.on_edit(job.job_id)
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            actions_frame,
            text="🗑",
            width=30,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=lambda: self.on_delete(job.job_id)
        ).pack(side="left", padx=2)
    
    def _get_status_color(self, status: str) -> str:
        """Get color for status."""
        colors = {
            "ok": "#27ae60",
            "running": "#3498db",
            "paused": "#95a5a6",
            "failed": "#e74c3c",
            "warning": "#f39c12",
            "completed": "#27ae60",
            "scheduled": "#9b59b6",
        }
        return colors.get(status, "#95a5a6")


class MainWindow(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize managers
        self.i18n = get_i18n()
        self.theme_manager = get_theme_manager()
        self.app_config = get_config()
        self.job_manager = get_job_manager()
        self.scheduler = BackupScheduler(self.job_manager)
        
        # Apply saved settings
        self.i18n.set_language(self.app_config.get("language", "hr"))
        self.theme_manager.set_theme(self.app_config.get("theme", "dark"))
        
        # Window setup
        self.title(t("app_title"))
        self.geometry("1200x700")
        
        # Setup UI
        self._create_menu()
        self._create_dashboard()
        
        # Start scheduler
        self.scheduler.start()
        
        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=t("menu.file"), menu=file_menu)
        file_menu.add_command(label=t("menu.settings"), command=self._open_settings)
        file_menu.add_separator()
        file_menu.add_command(label=t("menu.exit"), command=self._on_closing)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=t("menu.view"), menu=view_menu)
        view_menu.add_command(label=t("history.title"), command=self._show_history)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=t("menu.help"), menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_dashboard(self):
        """Create dashboard UI."""
        # Main container
        main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text=t("dashboard.title"),
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Statistics cards
        cards_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.jobs_card = DashboardCard(
            cards_frame,
            t("dashboard.jobs"),
            "0",
            "📋"
        )
        self.jobs_card.grid(row=0, column=0, padx=10, sticky="ew")
        
        self.active_card = DashboardCard(
            cards_frame,
            t("dashboard.active"),
            "0",
            "⏱️"
        )
        self.active_card.grid(row=0, column=1, padx=10, sticky="ew")
        
        self.storage_card = DashboardCard(
            cards_frame,
            t("dashboard.storage"),
            "0 GB",
            "💾"
        )
        self.storage_card.grid(row=0, column=2, padx=10, sticky="ew")
        
        # Jobs section
        jobs_header = ctk.CTkFrame(main_frame, fg_color="transparent")
        jobs_header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            jobs_header,
            text=t("dashboard.backup_jobs"),
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            jobs_header,
            text=f"+ {t('dashboard.new_job')}",
            command=self._create_new_job,
            fg_color="#27ae60",
            hover_color="#229954"
        ).pack(side="right")
        
        # Jobs table header
        table_header = ctk.CTkFrame(main_frame, corner_radius=5)
        table_header.pack(fill="x", pady=(0, 5))
        
        table_header.grid_columnconfigure(0, weight=2)
        table_header.grid_columnconfigure(1, weight=1)
        table_header.grid_columnconfigure(2, weight=1)
        table_header.grid_columnconfigure(3, weight=1)
        table_header.grid_columnconfigure(4, weight=1)
        
        headers = [
            t("job_editor.job_name"),
            t("dashboard.status"),
            t("dashboard.last_run"),
            t("dashboard.next_run"),
            t("dashboard.actions")
        ]
        
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                table_header,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold")
            ).grid(row=0, column=i, padx=10, pady=10)
        
        # Jobs list (scrollable)
        self.jobs_container = ctk.CTkScrollableFrame(main_frame, height=300)
        self.jobs_container.pack(fill="both", expand=True)
        
        # Load jobs
        self._refresh_jobs()
        
        # Update statistics
        self._update_statistics()
    
    def _refresh_jobs(self):
        """Refresh jobs list."""
        # Clear existing
        for widget in self.jobs_container.winfo_children():
            widget.destroy()
        
        # Load jobs
        jobs = self.job_manager.get_all_jobs()
        
        if not jobs:
            no_jobs_label = ctk.CTkLabel(
                self.jobs_container,
                text=t("messages.no_jobs"),
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_jobs_label.pack(pady=50)
        else:
            for job in jobs:
                job_row = JobRow(
                    self.jobs_container,
                    job,
                    self._run_job,
                    self._edit_job,
                    self._delete_job
                )
                job_row.pack(fill="x", pady=2)
    
    def _update_statistics(self):
        """Update dashboard statistics."""
        jobs = self.job_manager.get_all_jobs()
        running_jobs = self.job_manager.get_jobs_by_status("running")
        
        self.jobs_card.update_value(str(len(jobs)))
        self.active_card.update_value(str(len(running_jobs)))
        
        # Schedule next update
        self.after(5000, self._update_statistics)
    
    def _create_new_job(self):
        """Open job editor for new job."""
        editor = JobEditorWindow(self, None, self._on_job_saved)
        editor.grab_set()
    
    def _edit_job(self, job_id: str):
        """Edit existing job."""
        job = self.job_manager.get_job(job_id)
        if job:
            editor = JobEditorWindow(self, job, self._on_job_saved)
            editor.grab_set()
    
    def _on_job_saved(self):
        """Callback when job is saved."""
        self._refresh_jobs()
        self._update_statistics()
        self.scheduler.refresh_schedules()
    
    def _run_job(self, job_id: str):
        """Run a job immediately."""
        job = self.job_manager.get_job(job_id)
        if not job:
            return
        
        # Import progress dialog
        from gui.progress_dialog import ProgressDialog
        from core.backup_engine import BackupEngine
        import threading
        
        # Create progress dialog
        progress_dialog = ProgressDialog(self, job.name)
        progress_dialog.grab_set()
        
        # Run backup in thread
        def run_backup():
            try:
                engine = BackupEngine()
                
                # Progress callback
                def update_progress(progress):
                    if progress_dialog.is_cancelled:
                        engine.cancel_backup()
                        return
                    
                    if progress_dialog.is_paused:
                        engine.pause_backup()
                    else:
                        engine.resume_backup()
                    
                    # Update UI in main thread
                    self.after(0, lambda: progress_dialog.update_progress(progress))
                
                # Perform backup
                result = engine.perform_backup(
                    source_paths=job.source_paths,
                    destination_path=job.destination_path,
                    backup_type=job.backup_type,
                    filters=job.filters,
                    compression=job.compression,
                    progress_callback=update_progress,
                    job_name=job.name
                )
                
                # Update job
                from datetime import datetime
                self.job_manager.update_job(
                    job_id,
                    status="completed",
                    last_run=datetime.now().isoformat()
                )
                
                # Show completion
                self.after(0, lambda: progress_dialog.show_completion(True, ""))
                self.after(100, self._refresh_jobs)
                
            except Exception as e:
                # Update job status
                self.job_manager.update_job(job_id, status="failed")
                
                # Show error
                self.after(0, lambda: progress_dialog.show_completion(False, str(e)))
                self.after(100, self._refresh_jobs)
        
        # Start backup thread
        backup_thread = threading.Thread(target=run_backup, daemon=True)
        backup_thread.start()
    
    def _delete_job(self, job_id: str):
        """Delete a job."""
        if messagebox.askyesno(
            t("app_title"),
            t("messages.confirm_delete")
        ):
            self.job_manager.delete_job(job_id)
            self._refresh_jobs()
            self._update_statistics()
            self.scheduler.refresh_schedules()
    
    def _open_settings(self):
        """Open settings window."""
        settings = SettingsWindow(self, self._on_settings_changed)
        settings.grab_set()
    
    def _on_settings_changed(self):
        """Callback when settings are changed."""
        # Reload settings
        self.i18n.set_language(self.app_config.get("language", "hr"))
        self.theme_manager.set_theme(self.app_config.get("theme", "dark"))
        
        # Recreate UI to apply changes
        # In a production app, you'd want to update existing widgets
        messagebox.showinfo(
            t("app_title"),
            "Please restart the application for all changes to take effect."
        )
    
    def _show_history(self):
        """Show backup history."""
        messagebox.showinfo(t("app_title"), "History view - Coming soon!")
    
    def _show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About",
            "Backup Daddy v1.0.0\n\nTvoj pouzdani pomoćnik za backup."
        )
    
    def _on_closing(self):
        """Handle window closing."""
        self.scheduler.stop()
        self.destroy()


def run_gui():
    """Run the GUI application."""
    ctk.set_default_color_theme("blue")
    app = MainWindow()
    app.mainloop()
