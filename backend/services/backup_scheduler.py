import os
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backup_scheduler")

def run_automated_backups():
    """Triggers both JSON and SQL exports via backend/db_tools.py"""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_tools_path = os.path.join(base_dir, "backend", "db_tools.py")
        
        # Run JSON backup
        subprocess.run(["python3", db_tools_path, "json"], check=True)
        # Run SQL backup
        subprocess.run(["python3", db_tools_path, "sql"], check=True)
        
        logger.info("✅ Scheduled Database Backup Completed Successfully (JSON + SQL)")
    except Exception as e:
        logger.error(f"❌ Scheduled Database Backup Failed: {e}")

def start_scheduler():
    """Starts the background scheduler loop."""
    scheduler = BackgroundScheduler()
    # Runs automated backups every 6 hours
    scheduler.add_job(run_automated_backups, 'interval', hours=6, id='db_backup_job', replace_existing=True)
    scheduler.start()
    logger.info("🚀 Database Backup Scheduler Initialized (Interval: 6 Hours)")
    return scheduler
