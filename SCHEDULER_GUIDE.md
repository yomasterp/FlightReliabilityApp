# Scheduler Guide - Running Data Collection Every 30 Minutes

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
- Then run every 30 minutes automatically
- Continue running until you press `Ctrl+C`

### 3. Run in Background (Windows)
To run the scheduler in the background without a console window:
```bash
pythonw scheduler.py
```

## How It Works

The `scheduler.py` script:
1. Uses the `schedule` library to set up a recurring job
2. Runs `src.main.main()` every 30 minutes
3. Includes error handling - if one collection fails, it continues
4. Logs timestamps for each collection run
5. Runs immediately on startup, then every 30 minutes

## Customization

### Change the Interval
Edit `scheduler.py` and modify line 45:
```python
# Every 30 minutes (current)
schedule.every(30).minutes.do(run_data_collection)

# Every hour
schedule.every().hour.do(run_data_collection)

# Every 15 minutes
schedule.every(15).minutes.do(run_data_collection)

# Every day at specific time
schedule.every().day.at("10:30").do(run_data_collection)
```

### Disable Initial Run
If you don't want it to run immediately on startup, comment out lines 48-49 in `scheduler.py`:
```python
# Run once immediately on startup
# print("\nRunning initial data collection...")
# run_data_collection()
```

## Alternative: Windows Task Scheduler

For production use on Windows, you can also use Windows Task Scheduler:

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: "Daily" or "When computer starts"
4. Set action: "Start a program"
5. Program: `pythonw`
6. Arguments: `scheduler.py`
7. Start in: `C:\Users\smrit\FlightReliabilityApp`

## Alternative: Cron (Linux/Mac)

On Linux or Mac, you can use cron:
```bash
# Edit crontab
crontab -e

# Add this line to run every 30 minutes
*/30 * * * * cd /path/to/FlightReliabilityApp && python scheduler.py
```

## Monitoring

The scheduler prints logs to the console:
- Timestamp of each collection run
- Success/failure messages
- Error details if something goes wrong

For production, you might want to redirect output to a log file:
```bash
python scheduler.py >> scheduler.log 2>&1
```

## Stopping the Scheduler

- **Interactive mode**: Press `Ctrl+C`
- **Background mode**: Find the process and kill it:
  ```bash
  # Windows PowerShell
  Get-Process pythonw | Where-Object {$_.Path -like "*FlightReliabilityApp*"} | Stop-Process
  ```

