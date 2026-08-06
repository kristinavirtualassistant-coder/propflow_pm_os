import os
import sys
import time
import subprocess
import logging
from datetime import datetime, timezone
import urllib.request
import json

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("backup_monitor.log")
    ]
)
logger = logging.getLogger("propflow_cron")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_TOOLS_PATH = os.path.join(BASE_DIR, "backend", "db_tools.py")
BACKEND_HEALTH_URL = "http://127.0.0.1:8000/health"

def check_system_health() -> bool:
    """Verifies that the PropFlow backend service is operational."""
    try:
        req = urllib.request.Request(BACKEND_HEALTH_URL, headers={"User-Agent": "PropFlow-Monitor/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                logger.info("✅ System Health Check PASSED: FastAPI Backend is online.")
                return True
    except Exception as e:
        logger.error(f"❌ System Health Check FAILED: Could not connect to {BACKEND_HEALTH_URL}. Error: {e}")
        return False
    return False

def execute_nightly_backups():
    """Runs automated JSON and SQL exports via backend/db_tools.py."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    logger.info(f"🚀 Starting PropFlow Nightly Backup Job at {timestamp}...")

    # 1. Health Verification
    is_healthy = check_system_health()
    if not is_healthy:
        logger.warning("⚠️ Warning: Proceeding with database snapshot while backend health check flagged an issue.")

    # 2. JSON Backup Export
    try:
        logger.info("📦 Generating JSON database snapshot...")
        result_json = subprocess.run(
            ["python3", DB_TOOLS_PATH, "json"],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"✅ JSON Snapshot Success: {result_json.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ JSON Snapshot Error: {e.stderr.strip()}")

    # 3. SQL Dump Export
    try:
        logger.info("💾 Generating SQL database dump...")
        result_sql = subprocess.run(
            ["python3", DB_TOOLS_PATH, "sql"],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"✅ SQL Dump Success: {result_sql.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ SQL Dump Error: {e.stderr.strip()}")

    logger.info("🎉 Nightly Backup & Monitoring Task Completed Successfully.")

if __name__ == "__main__":
    if "--daemon" in sys.argv:
        try:
            from apscheduler.schedulers.blocking import BlockingScheduler
            scheduler = BlockingScheduler()
            # Scheduled to run every night at 00:00 UTC (midnight)
            scheduler.add_job(execute_nightly_backups, 'cron', hour=0, minute=0, id='nightly_backup_job')
            logger.info("⏰ PropFlow Cron Backup Daemon Initialized. Running in background (Interval: Nightly @ 00:00 UTC)...")
            execute_nightly_backups()  # Run initial backup on daemon startup
            scheduler.start()
        except ImportError:
            logger.error("❌ 'apscheduler' not installed. Running single backup pass instead.")
            execute_nightly_backups()
    else:
        # Run single manual execution pass
        execute_nightly_backups()
