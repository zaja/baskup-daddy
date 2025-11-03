"""
Job editor window for creating and editing backup jobs.
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Optional, Callable
from core.job_manager import BackupJob, get_job_manager
from utils.i18n import t
from pathlib import Path


class JobEditorWindow(ctk.CTkToplevel):
    """Job editor dialog."""
    
    def __init__(self, parent, job: Optional[BackupJob], on_save: Callable):
        super().__init__(parent)
        
        self.job = job
        self.on_save = on_save
        self.job_manager = get_job_manager()
        
        # Window setup
        title = t("job_editor.create_title") if job is None else t("job_editor.title")
        self.title(title)
        self.geometry("800x840")
        self.minsize(700, 700)
        
        # Center window
        self.transient(parent)
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 800) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 840) // 2
        self.geometry(f"+{x}+{y}")
        
        # Current step
        self.current_step = 0
        self.steps = ["basic", "schedule", "filters", "advanced"]
        
        # Data storage
        self.source_paths = []
        if job:
            self.source_paths = job.source_paths.copy()
        
        # Step data storage (to preserve data when switching steps)
        self.step_data = {
            "name": job.name if job else "",
            "description": job.description if job else "",
            "destination": job.destination_path if job else "",
            "backup_type": job.backup_type if job else "full",
            "schedule_type": job.schedule.get("type", "manual") if job else "manual",
            "schedule_time": job.schedule.get("time", "00:00") if job else "00:00",
            "include_ext": ",".join(job.filters.get("include_extensions", [])) if job else "",
            "exclude_ext": ",".join(job.filters.get("exclude_extensions", [])) if job else "",
            "min_size": str(job.filters.get("min_size_mb", 0)) if job else "0",
            "max_size": str(job.filters.get("max_size_mb", 0)) if job else "0",
            "compression": job.compression if job else True,
            "encryption": job.encryption if job else False,
            "enabled": job.enabled if job else True,
        }
        
        # Create UI
        self._create_ui()
        self._load_job_data()
        self._show_step(0)
    
    def _create_ui(self):
        """Create the UI."""
        # Main container
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Steps indicator
        steps_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        steps_frame.pack(fill="x", pady=(0, 20))
        
        self.step_labels = []
        step_names = [
            t("job_editor.step_basic"),
            t("job_editor.step_schedule"),
            t("job_editor.step_filters"),
            t("job_editor.step_advanced")
        ]
        
        for i, step_name in enumerate(step_names):
            label = ctk.CTkLabel(
                steps_frame,
                text=f"{i+1}. {step_name}",
                font=ctk.CTkFont(size=12)
            )
            label.pack(side="left", padx=20)
            self.step_labels.append(label)
        
        # Content area
        self.content_frame = ctk.CTkFrame(main_frame)
        self.content_frame.pack(fill="both", expand=True, pady=(0, 20), padx=5)
        
        # Add internal padding to content
        self.content_frame.configure(fg_color="transparent")
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        nav_frame.pack(fill="x")
        
        self.prev_button = ctk.CTkButton(
            nav_frame,
            text=f"← {t('job_editor.previous')}",
            command=self._previous_step,
            width=120
        )
        self.prev_button.pack(side="left")
        
        ctk.CTkButton(
            nav_frame,
            text=t("job_editor.cancel"),
            command=self.destroy,
            width=120,
            fg_color="gray",
            hover_color="#5a5a5a"
        ).pack(side="left", padx=10)
        
        self.next_button = ctk.CTkButton(
            nav_frame,
            text=f"{t('job_editor.next')} →",
            command=self._next_step,
            width=120
        )
        self.next_button.pack(side="right")
        
        self.finish_button = ctk.CTkButton(
            nav_frame,
            text=t("job_editor.finish"),
            command=self._save_job,
            width=120,
            fg_color="#27ae60",
            hover_color="#229954"
        )
    
    def _show_step(self, step: int):
        """Show a specific step."""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Update step indicator
        for i, label in enumerate(self.step_labels):
            if i == step:
                label.configure(font=ctk.CTkFont(size=12, weight="bold"))
            else:
                label.configure(font=ctk.CTkFont(size=12))
        
        # Show step content
        if step == 0:
            self._create_basic_step()
        elif step == 1:
            self._create_schedule_step()
        elif step == 2:
            self._create_filters_step()
        elif step == 3:
            self._create_advanced_step()
        
        # Update navigation buttons
        if step > 0:
            self.prev_button.pack(side="left")
        else:
            self.prev_button.pack_forget()
        
        if step < len(self.steps) - 1:
            self.next_button.pack(side="right")
            self.finish_button.pack_forget()
        else:
            self.next_button.pack_forget()
            self.finish_button.pack(side="right")
    
    def _create_basic_step(self):
        """Create basic settings step."""
        # Job Name
        ctk.CTkLabel(
            self.content_frame,
            text=t("job_editor.job_name"),
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(15, 5), padx=15)
        
        self.name_entry = ctk.CTkEntry(self.content_frame, height=35)
        self.name_entry.insert(0, self.step_data["name"])
        self.name_entry.pack(fill="x", pady=(0, 15), padx=15)
        
        # Description
        ctk.CTkLabel(
            self.content_frame,
            text=t("job_editor.description"),
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(10, 5), padx=15)
        
        self.description_entry = ctk.CTkTextbox(self.content_frame, height=80)
        self.description_entry.insert("1.0", self.step_data["description"])
        self.description_entry.pack(fill="x", pady=(0, 15), padx=15)
        
        # Source Folders
        ctk.CTkLabel(
            self.content_frame,
            text=t("job_editor.source_folders"),
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(10, 5), padx=15)
        
        self.sources_frame = ctk.CTkScrollableFrame(self.content_frame, height=150)
        self.sources_frame.pack(fill="x", pady=(0, 10), padx=15)
        
        self._refresh_sources()
        
        ctk.CTkButton(
            self.content_frame,
            text=f"+ {t('job_editor.add_source')}",
            command=self._add_source,
            height=35
        ).pack(fill="x", pady=(0, 15), padx=15)
        
        # Destination
        ctk.CTkLabel(
            self.content_frame,
            text=t("job_editor.destination"),
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(10, 5), padx=15)
        
        dest_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        dest_frame.pack(fill="x", pady=(0, 15), padx=15)
        
        self.destination_entry = ctk.CTkEntry(dest_frame, height=35)
        self.destination_entry.insert(0, self.step_data["destination"])
        self.destination_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(
            dest_frame,
            text=t("job_editor.browse"),
            command=self._browse_destination,
            width=100,
            height=35
        ).pack(side="right")
        
        # Backup Type
        ctk.CTkLabel(
            self.content_frame,
            text=t("job_editor.backup_type"),
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(10, 5), padx=15)
        
        self.backup_type_var = ctk.StringVar(value=self.step_data["backup_type"])
        
        types_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        types_frame.pack(fill="x", padx=15)
        
        ctk.CTkRadioButton(
            types_frame,
            text=t("job_editor.full"),
            variable=self.backup_type_var,
            value="full"
        ).pack(side="left", padx=20)
        
        ctk.CTkRadioButton(
            types_frame,
            text=t("job_editor.incremental"),
            variable=self.backup_type_var,
            value="incremental"
        ).pack(side="left", padx=20)
        
        ctk.CTkRadioButton(
            types_frame,
            text=t("job_editor.differential"),
            variable=self.backup_type_var,
            value="differential"
        ).pack(side="left", padx=20)
    
    def _create_schedule_step(self):
        """Create schedule settings step."""
        ctk.CTkLabel(
            self.content_frame,
            text="Schedule Configuration",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=20, padx=15)
        
        # Schedule type
        self.schedule_type_var = ctk.StringVar(value=self.step_data["schedule_type"])
        
        ctk.CTkRadioButton(
            self.content_frame,
            text="Manual (Run manually only)",
            variable=self.schedule_type_var,
            value="manual"
        ).pack(anchor="w", pady=5, padx=15)
        
        ctk.CTkRadioButton(
            self.content_frame,
            text="Daily",
            variable=self.schedule_type_var,
            value="daily"
        ).pack(anchor="w", pady=5, padx=15)
        
        # Time picker for daily
        time_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        time_frame.pack(fill="x", pady=10, padx=15)
        
        ctk.CTkLabel(time_frame, text="Time:").pack(side="left", padx=10)
        self.time_entry = ctk.CTkEntry(time_frame, width=100, placeholder_text="00:00")
        self.time_entry.insert(0, self.step_data["schedule_time"])
        self.time_entry.pack(side="left")
        
        ctk.CTkRadioButton(
            self.content_frame,
            text="Weekly",
            variable=self.schedule_type_var,
            value="weekly"
        ).pack(anchor="w", pady=5, padx=15)
        
        ctk.CTkRadioButton(
            self.content_frame,
            text="Monthly",
            variable=self.schedule_type_var,
            value="monthly"
        ).pack(anchor="w", pady=5, padx=15)
    
    def _create_filters_step(self):
        """Create filters step."""
        ctk.CTkLabel(
            self.content_frame,
            text="File Filters",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=20, padx=15)
        
        # Include extensions
        ctk.CTkLabel(
            self.content_frame,
            text="Include Extensions (comma-separated, e.g., pdf,docx,xlsx):",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", pady=(10, 5), padx=15)
        
        self.include_ext_entry = ctk.CTkEntry(self.content_frame, height=35)
        self.include_ext_entry.insert(0, self.step_data["include_ext"])
        self.include_ext_entry.pack(fill="x", pady=(0, 15), padx=15)
        
        # Exclude extensions
        ctk.CTkLabel(
            self.content_frame,
            text="Exclude Extensions (comma-separated, e.g., tmp,log,cache):",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", pady=(10, 5), padx=15)
        
        self.exclude_ext_entry = ctk.CTkEntry(self.content_frame, height=35)
        self.exclude_ext_entry.insert(0, self.step_data["exclude_ext"])
        self.exclude_ext_entry.pack(fill="x", pady=(0, 15), padx=15)
        
        # Size filters
        size_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        size_frame.pack(fill="x", pady=10, padx=15)
        
        ctk.CTkLabel(size_frame, text="Min Size (MB):").pack(side="left", padx=5)
        self.min_size_entry = ctk.CTkEntry(size_frame, width=100, placeholder_text="0")
        self.min_size_entry.insert(0, self.step_data["min_size"])
        self.min_size_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(size_frame, text="Max Size (MB):").pack(side="left", padx=5)
        self.max_size_entry = ctk.CTkEntry(size_frame, width=100, placeholder_text="0")
        self.max_size_entry.insert(0, self.step_data["max_size"])
        self.max_size_entry.pack(side="left", padx=5)
    
    def _create_advanced_step(self):
        """Create advanced settings step."""
        ctk.CTkLabel(
            self.content_frame,
            text="Advanced Options",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=20, padx=15)
        
        # Compression
        self.compression_var = ctk.BooleanVar(value=self.step_data["compression"])
        ctk.CTkCheckBox(
            self.content_frame,
            text="Enable Compression (ZIP)",
            variable=self.compression_var
        ).pack(anchor="w", pady=10, padx=15)
        
        # Encryption
        self.encryption_var = ctk.BooleanVar(value=self.step_data["encryption"])
        ctk.CTkCheckBox(
            self.content_frame,
            text="Enable Encryption (Coming soon)",
            variable=self.encryption_var,
            state="disabled"
        ).pack(anchor="w", pady=10, padx=15)
        
        # Enabled
        self.enabled_var = ctk.BooleanVar(value=self.step_data["enabled"])
        ctk.CTkCheckBox(
            self.content_frame,
            text="Job Enabled",
            variable=self.enabled_var
        ).pack(anchor="w", pady=10, padx=15)
    
    def _refresh_sources(self):
        """Refresh source paths list."""
        for widget in self.sources_frame.winfo_children():
            widget.destroy()
        
        for i, path in enumerate(self.source_paths):
            source_frame = ctk.CTkFrame(self.sources_frame, fg_color="transparent")
            source_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                source_frame,
                text=f"📁 {path}",
                font=ctk.CTkFont(size=12)
            ).pack(side="left", fill="x", expand=True)
            
            ctk.CTkButton(
                source_frame,
                text="×",
                width=30,
                command=lambda idx=i: self._remove_source(idx),
                fg_color="#e74c3c",
                hover_color="#c0392b"
            ).pack(side="right")
    
    def _add_source(self):
        """Add source path."""
        path = filedialog.askdirectory(title=t("job_editor.source_folders"))
        if path:
            self.source_paths.append(path)
            self._refresh_sources()
    
    def _remove_source(self, index: int):
        """Remove source path."""
        if 0 <= index < len(self.source_paths):
            self.source_paths.pop(index)
            self._refresh_sources()
    
    def _browse_destination(self):
        """Browse for destination."""
        path = filedialog.askdirectory(title=t("job_editor.destination"))
        if path:
            self.destination_entry.delete(0, "end")
            self.destination_entry.insert(0, path)
    
    def _load_job_data(self):
        """Load existing job data."""
        # Data is already loaded in step_data dictionary
        pass
    
    def _save_step_data(self, step: int):
        """Save data from current step before switching."""
        try:
            if step == 0:  # Basic step
                if hasattr(self, 'name_entry'):
                    self.step_data["name"] = self.name_entry.get()
                if hasattr(self, 'description_entry'):
                    self.step_data["description"] = self.description_entry.get("1.0", "end").strip()
                if hasattr(self, 'destination_entry'):
                    self.step_data["destination"] = self.destination_entry.get()
                if hasattr(self, 'backup_type_var'):
                    self.step_data["backup_type"] = self.backup_type_var.get()
            
            elif step == 1:  # Schedule step
                if hasattr(self, 'schedule_type_var'):
                    self.step_data["schedule_type"] = self.schedule_type_var.get()
                if hasattr(self, 'time_entry'):
                    self.step_data["schedule_time"] = self.time_entry.get()
            
            elif step == 2:  # Filters step
                if hasattr(self, 'include_ext_entry'):
                    self.step_data["include_ext"] = self.include_ext_entry.get()
                if hasattr(self, 'exclude_ext_entry'):
                    self.step_data["exclude_ext"] = self.exclude_ext_entry.get()
                if hasattr(self, 'min_size_entry'):
                    self.step_data["min_size"] = self.min_size_entry.get()
                if hasattr(self, 'max_size_entry'):
                    self.step_data["max_size"] = self.max_size_entry.get()
            
            elif step == 3:  # Advanced step
                if hasattr(self, 'compression_var'):
                    self.step_data["compression"] = self.compression_var.get()
                if hasattr(self, 'encryption_var'):
                    self.step_data["encryption"] = self.encryption_var.get()
                if hasattr(self, 'enabled_var'):
                    self.step_data["enabled"] = self.enabled_var.get()
        except Exception as e:
            print(f"Error saving step data: {e}")
    
    def _previous_step(self):
        """Go to previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            self._show_step(self.current_step)
    
    def _next_step(self):
        """Go to next step."""
        if self.current_step < len(self.steps) - 1:
            # Validate current step
            if not self._validate_step(self.current_step):
                return
            
            # Save current step data
            self._save_step_data(self.current_step)
            
            self.current_step += 1
            self._show_step(self.current_step)
    
    def _validate_step(self, step: int) -> bool:
        """Validate current step."""
        if step == 0:
            if not self.name_entry.get().strip():
                messagebox.showerror("Error", "Job name is required")
                return False
            
            if not self.source_paths:
                messagebox.showerror("Error", "At least one source path is required")
                return False
            
            if not self.destination_entry.get().strip():
                messagebox.showerror("Error", "Destination path is required")
                return False
        
        return True
    
    def _save_job(self):
        """Save the job."""
        if not self._validate_step(self.current_step):
            return
        
        # Save current step data first
        self._save_step_data(self.current_step)
        
        # Collect data from step_data
        schedule_config = {
            "type": self.step_data["schedule_type"],
            "time": self.step_data["schedule_time"] if self.step_data["schedule_type"] != "manual" else None
        }
        
        filters = {
            "include_extensions": [ext.strip() for ext in self.step_data["include_ext"].split(",") if ext.strip()],
            "exclude_extensions": [ext.strip() for ext in self.step_data["exclude_ext"].split(",") if ext.strip()],
            "min_size_mb": float(self.step_data["min_size"] or 0),
            "max_size_mb": float(self.step_data["max_size"] or 0),
            "exclude_patterns": []
        }
        
        if self.job:
            # Update existing job
            self.job_manager.update_job(
                self.job.job_id,
                name=self.step_data["name"],
                description=self.step_data["description"],
                source_paths=self.source_paths,
                destination_path=self.step_data["destination"],
                backup_type=self.step_data["backup_type"],
                schedule=schedule_config,
                filters=filters,
                compression=self.step_data["compression"],
                encryption=self.step_data["encryption"],
                enabled=self.step_data["enabled"]
            )
        else:
            # Create new job
            new_job = BackupJob(
                name=self.step_data["name"],
                description=self.step_data["description"],
                source_paths=self.source_paths,
                destination_path=self.step_data["destination"],
                backup_type=self.step_data["backup_type"],
                schedule=schedule_config,
                filters=filters,
                compression=self.step_data["compression"],
                encryption=self.step_data["encryption"],
                enabled=self.step_data["enabled"]
            )
            self.job_manager.create_job(new_job)
        
        # Callback and close
        if self.on_save:
            self.on_save()
        
        self.destroy()
