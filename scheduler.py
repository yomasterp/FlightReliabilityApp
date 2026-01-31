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
import traceback
from datetime import datetime

# Add src to path so we can import the main module
sys.path.insert(0, '.')

try:
    from src.main import main
except ImportError as e:
    print(f"Error importing main module: {e}")
    print("Make sure you're running from the project root directory.")
    sys.exit(1)


def run_data_collection():
    """Wrapper function to run main() with error handling and logging."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] Starting flight data collection...")
    
    try:
        main()
        print(f"[{timestamp}] Flight data collection completed successfully.")
    except Exception as e:
        print(f"[{timestamp}] ERROR during flight data collection:")
        print(f"  {type(e).__name__}: {e}")
        traceback.print_exc()
        # Continue running even if one collection fails
        print(f"[{timestamp}] Scheduler will continue running...")


def main_scheduler():
    """Main scheduler loop."""
    print("=" * 60)
    print("Flight Data Collection Scheduler")
    print("=" * 60)
    print("Scheduled to run every 30 minutes")
    print("Press Ctrl+C to stop the scheduler")
    print("=" * 60)
    
    # Schedule the job to run every 30 minutes
    schedule.every(30).minutes.do(run_data_collection)
    
    # Run once immediately on startup
    print("\nRunning initial data collection...")
    run_data_collection()
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user.")
        print("Final data collection completed.")


if __name__ == "__main__":
    main_scheduler()

