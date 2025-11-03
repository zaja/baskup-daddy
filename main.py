"""
Main entry point for Backup Daddy.
"""
import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_gui_mode():
    """Run the application in GUI mode."""
    from gui.main_window import run_gui
    run_gui()


def run_service_mode():
    """Run the application in service mode (background scheduler)."""
    from core.scheduler import BackupScheduler
    from core.job_manager import get_job_manager
    from utils.logger import get_logger
    import time
    
    logger = get_logger()
    logger.info("Starting Backup Service in background mode")
    
    job_manager = get_job_manager()
    scheduler = BackupScheduler(job_manager)
    
    try:
        scheduler.start()
        logger.info("Backup Service started successfully")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        scheduler.stop()
        logger.info("Backup Service stopped")
    except Exception as e:
        logger.error(f"Service error: {str(e)}", exc_info=True)
        scheduler.stop()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Backup Daddy - Your reliable backup assistant"
    )
    parser.add_argument(
        "--service",
        action="store_true",
        help="Run in service mode (background scheduler only)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Backup Daddy v1.0.0"
    )
    
    args = parser.parse_args()
    
    if args.service:
        run_service_mode()
    else:
        run_gui_mode()


if __name__ == "__main__":
    main()
