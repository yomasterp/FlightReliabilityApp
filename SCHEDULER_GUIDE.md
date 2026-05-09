# Scheduler Guide — Data Collection Every 8 Hours

## Quick Start

### 1. Install the Schedule Library
```bash
pip install schedule
```
Or install all requirements:
```bash
pip install -r requirements.txt
```

### 2. Run the Scheduler
```bash
python scheduler.py
```

The scheduler will:
- Run data collection immediately
- Then run every 8 hours automatically
- Continue running until you press `Ctrl+C`

### 3. Run in Background (Windows)
To run the scheduler in the background without a console window:
```bash
pythonw scheduler.py
```

## How It Works

The `scheduler.py` script:
1. Uses the `schedule` library to set up a recurring job
2. Runs `src.main.main()` every 8 hours
3. Includes error handling - if one collection fails, it continues
4. Logs to both the console and `scheduler.log` (with timestamps)
5. Runs immediately on startup, then every 8 hours

## Customization

### Change the Interval
Edit `scheduler.py` and modify the `schedule.every(...)` line in `main_scheduler()`:
```python
# Every 8 hours (current)
schedule.every(8).hours.do(run_data_collection)

# Every hour
schedule.every().hour.do(run_data_collection)

# Every 15 minutes
schedule.every(15).minutes.do(run_data_collection)

# Every day at specific time
schedule.every().day.at("10:30").do(run_data_collection)
```

### Disable Initial Run
If you don't want it to run immediately on startup, comment out the initial run block in `main_scheduler()`:
```python
# Run once immediately on startup
# logger.info("Running initial data collection...")
# run_data_collection()
```

## Monitoring

The scheduler logs to both the console and `scheduler.log` in the project root:
- Timestamp of each collection run
- Success/failure messages
- Error details (including full tracebacks) if something goes wrong

To keep only a file copy (e.g. when running in background), you can still redirect:
```bash
python scheduler.py >> scheduler_console.log 2>&1
```

## Stopping the Scheduler

- **Interactive mode**: Press `Ctrl+C`
- **Background mode**: Find the process and kill it:
  ```bash
  # Windows PowerShell
  Get-Process pythonw | Where-Object {$_.Path -like "*FlightReliabilityApp*"} | Stop-Process
  ```

