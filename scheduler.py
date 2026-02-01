"""
Scheduler script to run main.py every 30 minutes to collect flight data.

This script uses Python's schedule library to run the data collection
at regular intervals. It includes error handling and logging.

Usage:
    python scheduler.py

To run in the background on Windows:
    pythonw scheduler.py
"""

import schedule
import time
import sys
import logging

logger = logging.getLogger("scheduler")
logger.setLevel(logging.INFO)

# Prevent duplicate logging
logger.propagate = False

# File handler
file_handler = logging.FileHandler("scheduler.log")
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Add src to path so we can import the main module
sys.path.insert(0, '.')

try:
    from src.main import main
except ImportError as e:
    logger.exception("Error importing main module. Make sure you're running from the project root directory.")
    sys.exit(1)


def run_data_collection():
    """Wrapper function to run main() with error handling and logging."""
    logger.info("Starting flight data collection...")
    
    try:
        main()
        logger.info("Flight data collection completed successfully.")
    except Exception as e:
        logger.error("ERROR during flight data collection")
        logger.exception("Unhandled exception during flight data collection")
        # Continue running even if one collection fails
        logger.info("Scheduler will continue running...")


def main_scheduler():
    """Main scheduler loop."""
    logger.info("=" * 60)
    logger.info("Flight Data Collection Scheduler")
    logger.info("Scheduled to run every 30 minutes")
    logger.info("Press Ctrl+C to stop the scheduler")
    logger.info("=" * 60)

    
    # Schedule the job to run every 30 minutes
    schedule.every(8).hour.do(run_data_collection)
    
    # Run once immediately on startup
    logger.info("Running initial data collection...")
    run_data_collection()
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")
        logger.info("Final data collection completed.")


if __name__ == "__main__":
    main_scheduler()

