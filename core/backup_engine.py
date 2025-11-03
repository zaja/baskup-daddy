"""
Core backup engine for performing backup operations.
"""
import os
import shutil
import hashlib
import zipfile
from pathlib import Path
from typing import Callable, Optional, List, Dict, Any
from datetime import datetime
import threading


class BackupProgress:
    """Tracks backup progress."""
    
    def __init__(self):
        self.total_files = 0
        self.processed_files = 0
        self.total_size = 0
        self.processed_size = 0
        self.current_file = ""
        self.current_file_size = 0
        self.current_file_processed = 0
        self.errors = []
        self.skipped_files = []
        self.start_time = None
        self.end_time = None
        self.is_cancelled = False
        self.is_paused = False
    
    def get_progress_percent(self) -> float:
        """Get overall progress percentage."""
        if self.total_files == 0:
            return 0.0
        return (self.processed_files / self.total_files) * 100
    
    def get_speed_mbps(self) -> float:
        """Get current transfer speed in MB/s."""
        if not self.start_time:
            return 0.0
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if elapsed == 0:
            return 0.0
        return (self.processed_size / (1024 * 1024)) / elapsed
    
    def get_eta_seconds(self) -> int:
        """Get estimated time remaining in seconds."""
        speed = self.get_speed_mbps()
        if speed == 0:
            return 0
        remaining_mb = (self.total_size - self.processed_size) / (1024 * 1024)
        return int(remaining_mb / speed)


class BackupEngine:
    """Core backup engine."""
    
    def __init__(self):
        self.progress = BackupProgress()
        self._lock = threading.Lock()
    
    def calculate_backup_size(self, source_paths: List[str], filters: Dict[str, Any]) -> tuple:
        """
        Calculate total size and file count for backup.
        
        Returns:
            Tuple of (total_size_bytes, total_files)
        """
        total_size = 0
        total_files = 0
        
        for source_path in source_paths:
            source = Path(source_path)
            if not source.exists():
                continue
            
            if source.is_file():
                if self._should_include_file(source, filters):
                    total_size += source.stat().st_size
                    total_files += 1
            else:
                for root, dirs, files in os.walk(source):
                    for file in files:
                        file_path = Path(root) / file
                        if self._should_include_file(file_path, filters):
                            try:
                                total_size += file_path.stat().st_size
                                total_files += 1
                            except (OSError, PermissionError):
                                pass
        
        return total_size, total_files
    
    def _should_include_file(self, file_path: Path, filters: Dict[str, Any]) -> bool:
        """Check if file should be included based on filters."""
        # Check extension filters
        include_ext = filters.get("include_extensions", [])
        exclude_ext = filters.get("exclude_extensions", [])
        
        if include_ext and file_path.suffix.lower() not in [f".{ext.lower()}" for ext in include_ext]:
            return False
        
        if exclude_ext and file_path.suffix.lower() in [f".{ext.lower()}" for ext in exclude_ext]:
            return False
        
        # Check size filters
        try:
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            min_size = filters.get("min_size_mb", 0)
            max_size = filters.get("max_size_mb", 0)
            
            if min_size > 0 and file_size_mb < min_size:
                return False
            
            if max_size > 0 and file_size_mb > max_size:
                return False
        except (OSError, PermissionError):
            return False
        
        # Check exclude patterns
        exclude_patterns = filters.get("exclude_patterns", [])
        for pattern in exclude_patterns:
            if pattern in str(file_path):
                return False
        
        return True
    
    def perform_backup(
        self,
        source_paths: List[str],
        destination_path: str,
        backup_type: str = "full",
        filters: Dict[str, Any] = None,
        compression: bool = True,
        progress_callback: Optional[Callable[[BackupProgress], None]] = None,
        job_name: str = None
    ) -> Dict[str, Any]:
        """
        Perform backup operation.
        
        Args:
            source_paths: List of source paths to backup
            destination_path: Destination directory
            backup_type: Type of backup (full, incremental, differential)
            filters: File filters
            compression: Whether to compress the backup
            progress_callback: Optional callback for progress updates
            job_name: Optional job name for folder organization
            
        Returns:
            Dictionary with backup results
        """
        if filters is None:
            filters = {}
        
        # Initialize progress
        self.progress = BackupProgress()
        self.progress.start_time = datetime.now()
        
        # Calculate total size
        total_size, total_files = self.calculate_backup_size(source_paths, filters)
        self.progress.total_size = total_size
        self.progress.total_files = total_files
        
        # Create job-specific folder structure
        dest = Path(destination_path)
        
        # Use job name or first source folder name for organization
        if job_name:
            # Sanitize job name for folder
            folder_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in job_name)
            folder_name = folder_name.strip().replace(' ', '_')
        else:
            # Use first source folder name
            first_source = Path(source_paths[0])
            folder_name = first_source.name if first_source.is_dir() else first_source.stem
        
        # Create job folder
        job_folder = dest / folder_name
        job_folder.mkdir(parents=True, exist_ok=True)
        
        # Create timestamped backup folder/file inside job folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = job_folder / f"backup_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Perform backup
        try:
            if compression:
                archive_path = backup_dir.parent / f"backup_{timestamp}.zip"
                self._backup_with_compression(source_paths, archive_path, filters, progress_callback)
                backup_path = str(archive_path)
            else:
                self._backup_without_compression(source_paths, backup_dir, filters, progress_callback)
                backup_path = str(backup_dir)
            
            self.progress.end_time = datetime.now()
            
            # Generate checksum
            checksum = self._calculate_checksum(backup_path)
            
            # Save metadata
            metadata = {
                "timestamp": timestamp,
                "backup_type": backup_type,
                "source_paths": source_paths,
                "destination": backup_path,
                "total_files": self.progress.processed_files,
                "total_size": self.progress.processed_size,
                "compression": compression,
                "checksum": checksum,
                "errors": self.progress.errors,
                "skipped_files": self.progress.skipped_files,
                "duration_seconds": (self.progress.end_time - self.progress.start_time).total_seconds(),
            }
            
            # Save metadata file
            metadata_file = Path(backup_path).parent / f"backup_{timestamp}_metadata.json"
            import json
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return metadata
            
        except Exception as e:
            self.progress.errors.append(f"Backup failed: {str(e)}")
            raise
    
    def _backup_with_compression(
        self,
        source_paths: List[str],
        archive_path: Path,
        filters: Dict[str, Any],
        progress_callback: Optional[Callable[[BackupProgress], None]]
    ):
        """Perform backup with compression."""
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for source_path in source_paths:
                source = Path(source_path)
                if not source.exists():
                    self.progress.errors.append(f"Source not found: {source_path}")
                    continue
                
                if source.is_file():
                    if self._should_include_file(source, filters):
                        self._add_file_to_zip(zipf, source, source.parent, progress_callback)
                else:
                    for root, dirs, files in os.walk(source):
                        for file in files:
                            if self.progress.is_cancelled:
                                return
                            
                            while self.progress.is_paused:
                                threading.Event().wait(0.1)
                            
                            file_path = Path(root) / file
                            if self._should_include_file(file_path, filters):
                                self._add_file_to_zip(zipf, file_path, source, progress_callback)
    
    def _add_file_to_zip(
        self,
        zipf: zipfile.ZipFile,
        file_path: Path,
        base_path: Path,
        progress_callback: Optional[Callable[[BackupProgress], None]]
    ):
        """Add a single file to zip archive."""
        try:
            arcname = str(file_path.relative_to(base_path))
            self.progress.current_file = str(file_path)
            self.progress.current_file_size = file_path.stat().st_size
            
            zipf.write(file_path, arcname)
            
            self.progress.processed_files += 1
            self.progress.processed_size += self.progress.current_file_size
            
            if progress_callback:
                progress_callback(self.progress)
                
        except Exception as e:
            self.progress.errors.append(f"Error adding {file_path}: {str(e)}")
    
    def _backup_without_compression(
        self,
        source_paths: List[str],
        backup_dir: Path,
        filters: Dict[str, Any],
        progress_callback: Optional[Callable[[BackupProgress], None]]
    ):
        """Perform backup without compression."""
        for source_path in source_paths:
            source = Path(source_path)
            if not source.exists():
                self.progress.errors.append(f"Source not found: {source_path}")
                continue
            
            if source.is_file():
                if self._should_include_file(source, filters):
                    dest_file = backup_dir / source.name
                    self._copy_file(source, dest_file, progress_callback)
            else:
                for root, dirs, files in os.walk(source):
                    for file in files:
                        if self.progress.is_cancelled:
                            return
                        
                        while self.progress.is_paused:
                            threading.Event().wait(0.1)
                        
                        file_path = Path(root) / file
                        if self._should_include_file(file_path, filters):
                            rel_path = file_path.relative_to(source)
                            dest_file = backup_dir / source.name / rel_path
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            self._copy_file(file_path, dest_file, progress_callback)
    
    def _copy_file(
        self,
        src: Path,
        dest: Path,
        progress_callback: Optional[Callable[[BackupProgress], None]]
    ):
        """Copy a single file with progress tracking."""
        try:
            self.progress.current_file = str(src)
            self.progress.current_file_size = src.stat().st_size
            
            shutil.copy2(src, dest)
            
            self.progress.processed_files += 1
            self.progress.processed_size += self.progress.current_file_size
            
            if progress_callback:
                progress_callback(self.progress)
                
        except Exception as e:
            self.progress.errors.append(f"Error copying {src}: {str(e)}")
    
    def _calculate_checksum(self, path: str) -> str:
        """Calculate SHA-256 checksum of backup."""
        sha256 = hashlib.sha256()
        path_obj = Path(path)
        
        if path_obj.is_file():
            with open(path_obj, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
        else:
            # For directories, hash all file contents
            for file_path in sorted(path_obj.rglob("*")):
                if file_path.is_file():
                    with open(file_path, 'rb') as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            sha256.update(chunk)
        
        return sha256.hexdigest()
    
    def cancel_backup(self):
        """Cancel the current backup operation."""
        self.progress.is_cancelled = True
    
    def pause_backup(self):
        """Pause the current backup operation."""
        self.progress.is_paused = True
    
    def resume_backup(self):
        """Resume the paused backup operation."""
        self.progress.is_paused = False
