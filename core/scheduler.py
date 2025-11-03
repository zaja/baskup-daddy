"""
Scheduler for automated backup execution.
"""
import schedule
import time
import threading
from datetime import datetime
from typing import Callable, Optional
from core.job_manager import JobManager, BackupJob
from core.backup_engine import BackupEngine
from utils.logger import get_logger


class BackupScheduler:
    """Manages scheduled backup execution."""
    
    def __init__(self, job_manager: JobManager):
        self.job_manager = job_manager
        self.backup_engine = BackupEngine()
        self.logger = get_logger()
        self.is_running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self.on_job_start: Optional[Callable[[BackupJob], None]] = None
        self.on_job_complete: Optional[Callable[[BackupJob, dict], None]] = None
        self.on_job_error: Optional[Callable[[BackupJob, Exception], None]] = None
    
    def _schedule_job(self, job: BackupJob):
        """Schedule a single job based on its schedule configuration."""
        schedule_config = job.schedule
        schedule_type = schedule_config.get("type", "manual")
        
        if schedule_type == "manual":
            return  # Manual jobs are not scheduled
        
        # Create the job execution function
        def execute_job():
            self._execute_backup_job(job)
        
        # Schedule based on type
        if schedule_type == "daily":
            time_str = schedule_config.get("time", "00:00")
            schedule.every().day.at(time_str).do(execute_job).tag(job.job_id)
            
        elif schedule_type == "weekly":
            day = schedule_config.get("day", "monday")
            time_str = schedule_config.get("time", "00:00")
            getattr(schedule.every(), day).at(time_str).do(execute_job).tag(job.job_id)
            
        elif schedule_type == "monthly":
            # Monthly scheduling - run on specific day of month
            day_of_month = schedule_config.get("day_of_month", 1)
            time_str = schedule_config.get("time", "00:00")
            
            def monthly_check():
                if datetime.now().day == day_of_month:
                    execute_job()
            
            schedule.every().day.at(time_str).do(monthly_check).tag(job.job_id)
            
        elif schedule_type == "interval":
            # Interval-based scheduling
            interval = schedule_config.get("interval", 1)
            unit = schedule_config.get("unit", "hours")  # minutes, hours, days
            
            if unit == "minutes":
                schedule.every(interval).minutes.do(execute_job).tag(job.job_id)
            elif unit == "hours":
                schedule.every(interval).hours.do(execute_job).tag(job.job_id)
            elif unit == "days":
                schedule.every(interval).days.do(execute_job).tag(job.job_id)
        
        self.logger.info(f"Scheduled job: {job.name} ({schedule_type})")
    
    def _execute_backup_job(self, job: BackupJob):
        """Execute a backup job."""
        try:
            self.logger.info(f"Starting backup job: {job.name}")
            
            # Update job status
            self.job_manager.update_job(job.job_id, status="running")
            
            # Notify listeners
            if self.on_job_start:
                self.on_job_start(job)
            
            # Perform backup
            result = self.backup_engine.perform_backup(
                source_paths=job.source_paths,
                destination_path=job.destination_path,
                backup_type=job.backup_type,
                filters=job.filters,
                compression=job.compression
            )
            
            # Update job status
            self.job_manager.update_job(
                job.job_id,
                status="completed",
                last_run=datetime.now().isoformat()
            )
            
            self.logger.info(f"Completed backup job: {job.name}")
            
            # Notify listeners
            if self.on_job_complete:
                self.on_job_complete(job, result)
                
        except Exception as e:
            self.logger.error(f"Backup job failed: {job.name} - {str(e)}", exc_info=True)
            
            # Update job status
            self.job_manager.update_job(job.job_id, status="failed")
            
            # Notify listeners
            if self.on_job_error:
                self.on_job_error(job, e)
    
    def start(self):
        """Start the scheduler."""
        if self.is_running:
            self.logger.warning("Scheduler is already running")
            return
        
        self.logger.info("Starting backup scheduler")
        self.is_running = True
        self._stop_event.clear()
        
        # Clear existing schedules
        schedule.clear()
        
        # Schedule all enabled jobs
        for job in self.job_manager.get_enabled_jobs():
            self._schedule_job(job)
        
        # Start scheduler thread
        self._thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._thread.start()
    
    def _run_scheduler(self):
        """Run the scheduler loop."""
        while self.is_running and not self._stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)
    
    def stop(self):
        """Stop the scheduler."""
        if not self.is_running:
            return
        
        self.logger.info("Stopping backup scheduler")
        self.is_running = False
        self._stop_event.set()
        
        if self._thread:
            self._thread.join(timeout=5)
        
        schedule.clear()
    
    def refresh_schedules(self):
        """Refresh all job schedules (call after job changes)."""
        if not self.is_running:
            return
        
        self.logger.info("Refreshing job schedules")
        
        # Clear and reschedule
        schedule.clear()
        for job in self.job_manager.get_enabled_jobs():
            self._schedule_job(job)
    
    def run_job_now(self, job_id: str):
        """Run a specific job immediately."""
        job = self.job_manager.get_job(job_id)
        if job:
            self.logger.info(f"Running job immediately: {job.name}")
            threading.Thread(
                target=self._execute_backup_job,
                args=(job,),
                daemon=True
            ).start()
        else:
            self.logger.error(f"Job not found: {job_id}")
    
    def get_next_run_time(self, job_id: str) -> Optional[datetime]:
        """Get the next scheduled run time for a job."""
        jobs = schedule.get_jobs(job_id)
        if jobs:
            return jobs[0].next_run
        return None
