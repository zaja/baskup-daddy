"""
Job manager for handling backup job configurations.
"""
import json
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class BackupJob:
    """Represents a single backup job configuration."""
    
    def __init__(
        self,
        job_id: str = None,
        name: str = "",
        description: str = "",
        source_paths: List[str] = None,
        destination_path: str = "",
        backup_type: str = "full",  # full, incremental, differential
        enabled: bool = True,
        schedule: Dict[str, Any] = None,
        filters: Dict[str, Any] = None,
        compression: bool = True,
        encryption: bool = False,
        created_at: str = None,
        modified_at: str = None,
        last_run: str = None,
        next_run: str = None,
        status: str = "scheduled",  # scheduled, running, completed, failed, paused
    ):
        self.job_id = job_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.source_paths = source_paths or []
        self.destination_path = destination_path
        self.backup_type = backup_type
        self.enabled = enabled
        self.schedule = schedule or {"type": "manual"}
        self.filters = filters or {
            "include_extensions": [],
            "exclude_extensions": [],
            "min_size_mb": 0,
            "max_size_mb": 0,
            "exclude_patterns": []
        }
        self.compression = compression
        self.encryption = encryption
        self.created_at = created_at or datetime.now().isoformat()
        self.modified_at = modified_at or datetime.now().isoformat()
        self.last_run = last_run
        self.next_run = next_run
        self.status = status
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job to dictionary."""
        return {
            "job_id": self.job_id,
            "name": self.name,
            "description": self.description,
            "source_paths": self.source_paths,
            "destination_path": self.destination_path,
            "backup_type": self.backup_type,
            "enabled": self.enabled,
            "schedule": self.schedule,
            "filters": self.filters,
            "compression": self.compression,
            "encryption": self.encryption,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "last_run": self.last_run,
            "next_run": self.next_run,
            "status": self.status,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackupJob':
        """Create job from dictionary."""
        return cls(**data)
    
    def update(self, **kwargs):
        """Update job properties."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.modified_at = datetime.now().isoformat()


class JobManager:
    """Manages all backup jobs."""
    
    def __init__(self, jobs_file: str = None):
        if jobs_file is None:
            data_dir = Path(__file__).parent.parent / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            self.jobs_file = data_dir / "jobs.json"
        else:
            self.jobs_file = Path(jobs_file)
        
        self.jobs: Dict[str, BackupJob] = {}
        self._load_jobs()
    
    def _load_jobs(self):
        """Load jobs from file."""
        if self.jobs_file.exists():
            try:
                with open(self.jobs_file, "r", encoding="utf-8") as f:
                    jobs_data = json.load(f)
                    self.jobs = {
                        job_id: BackupJob.from_dict(job_data)
                        for job_id, job_data in jobs_data.items()
                    }
            except Exception as e:
                print(f"Error loading jobs: {e}")
                self.jobs = {}
        else:
            self.jobs = {}
    
    def save_jobs(self):
        """Save all jobs to file."""
        try:
            jobs_data = {
                job_id: job.to_dict()
                for job_id, job in self.jobs.items()
            }
            with open(self.jobs_file, "w", encoding="utf-8") as f:
                json.dump(jobs_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving jobs: {e}")
    
    def create_job(self, job: BackupJob) -> str:
        """Create a new job."""
        self.jobs[job.job_id] = job
        self.save_jobs()
        return job.job_id
    
    def get_job(self, job_id: str) -> Optional[BackupJob]:
        """Get a job by ID."""
        return self.jobs.get(job_id)
    
    def get_all_jobs(self) -> List[BackupJob]:
        """Get all jobs."""
        return list(self.jobs.values())
    
    def get_enabled_jobs(self) -> List[BackupJob]:
        """Get all enabled jobs."""
        return [job for job in self.jobs.values() if job.enabled]
    
    def update_job(self, job_id: str, **kwargs) -> bool:
        """Update a job."""
        job = self.jobs.get(job_id)
        if job:
            job.update(**kwargs)
            self.save_jobs()
            return True
        return False
    
    def delete_job(self, job_id: str) -> bool:
        """Delete a job."""
        if job_id in self.jobs:
            del self.jobs[job_id]
            self.save_jobs()
            return True
        return False
    
    def get_jobs_by_status(self, status: str) -> List[BackupJob]:
        """Get jobs by status."""
        return [job for job in self.jobs.values() if job.status == status]


# Global job manager instance
_job_manager_instance = None


def get_job_manager() -> JobManager:
    """Get or create the global job manager instance."""
    global _job_manager_instance
    if _job_manager_instance is None:
        _job_manager_instance = JobManager()
    return _job_manager_instance
