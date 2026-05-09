# Project Structure Explanation

This document explains all files in the Flight Reliability & Availability Tracker project.

## Root Directory Files

### `tests/`
- **Purpose**: `pytest` coverage for parsing and hashing (no Postgres required)

### `.env.example`
- **Purpose**: Documents required env vars — copy to `.env` locally (never commit secrets)

### `pytest.ini`
- **Purpose**: Registers `tests/` and adds project root to `pythonpath`

### `README.md`
- **Purpose**: Project overview and setup instructions
- **Contents**: Describes the project goals, features, and basic setup steps
- **Status**: In progress (as noted in the file)

### `requirements.txt`
- **Purpose**: Python package dependencies
- **Contents**: Lists all required packages:
  - `requests` - HTTP library for API calls
  - `python-dotenv` - Environment variable management
  - `pandas` - Data analysis (for future analytics)
  - `scikit-learn` - Machine learning (for future predictions)
  - `fastapi` - Web API framework (for future API endpoints)
  - `uvicorn` - ASGI server (for FastAPI)
  - `sqlalchemy` - ORM for database operations
  - `psycopg2-binary` - PostgreSQL database adapter

### `.gitignore`
- **Purpose**: Specifies files/folders to exclude from version control
- **Contents**: 
  - Environment files (`.env`)
  - Python cache files
  - Virtual environments
  - Data files (CSV, JSON, Parquet)
  - IDE and OS files
  - Log files

### `scheduler.py`
- **Purpose**: Runs `src.main.main()` immediately, then **every 8 hours**
- **Contents**: Uses the `schedule` library to periodically collect flight data
- **Usage**: `python scheduler.py` or `pythonw scheduler.py` (background on Windows)

## Source Directory (`src/`)

### `src/__init__.py`
- **Purpose**: Makes `src` a Python package
- **Contents**: Currently empty (standard Python package marker)

### `src/config.py`
- **Purpose**: Centralized configuration management
- **Contents**:
  - Loads environment variables from `.env` file
  - Defines API configuration (Aviationstack API key and base URL)
  - Defines database configuration (PostgreSQL connection details)
  - Constructs SQLAlchemy database URL
- **Environment Variables Needed**:
  - `AVIATIONSTACK_API_KEY` - Your Aviationstack API key (required)
  - `AVIATIONSTACK_BASE_URL` - API base URL (optional, defaults to production)
  - `DB_HOST` - PostgreSQL host (defaults to localhost)
  - `DB_PORT` - PostgreSQL port (defaults to 5432)
  - `DB_NAME` - Database name (defaults to postgres)
  - `DB_USER` - Database user (defaults to postgres)
  - `DB_PASSWORD` - Database password (defaults to flight_reliability)

### `src/aviationstack_client.py`
- **Purpose**: API client wrapper for Aviationstack API
- **Contents**:
  - `AviationstackClient` class that handles API authentication
  - `_get()` method for making HTTP GET requests
  - `get_flights()` method specifically for fetching flight data
- **Features**:
  - Automatic API key injection
  - Error handling via `raise_for_status()`
  - 15-second timeout for requests
  - Clean parameter passing

### `src/database.py`
- **Purpose**: Database connection and session management
- **Contents**:
  - Creates SQLAlchemy engine from database URL
  - Defines `SessionLocal` for database sessions
  - Defines `Base` for declarative model definitions
- **Usage**: Imported by models and main.py for database operations

### `src/models.py`
- **Purpose**: SQLAlchemy ORM models (database schema)
- **Contents**:
  - `Flight` model representing the `flights` table
  - **Fields**:
    - `id` - Primary key
    - `flight_iata` - Flight code (e.g., "UA123")
    - `airline_iata` - Airline code (e.g., "UA")
    - `departure_airport` - Departure airport name
    - `departure_airport_iata` - Departure airport code
    - `arrival_airport` - Arrival airport name
    - `arrival_airport_iata` - Arrival airport code
    - `scheduled_departure` - Scheduled departure time
    - `scheduled_arrival` - Scheduled arrival time
    - `actual_departure` - Actual departure time
    - `actual_arrival` - Actual arrival time
    - `flight_status` - Current flight status
    - `airline_name` - Full airline name
    - `departure_delay` - Delay in minutes
    - `arrival_delay` - Delay in minutes
    - `departure_terminal` - Departure terminal
    - `arrival_terminal` - Arrival terminal
    - `departure_gate` - Departure gate
    - `arrival_gate` - Arrival gate
    - `ingested_at` - Timestamp when data was collected (UTC, timezone-aware)
    - `flight_date` - Provider flight date string (`YYYY-MM-DD`)
    - `content_hash` - SHA-256 fingerprint of canonical observation (deduplication)

### `src/flight_snapshot.py`
- **Purpose**: Builds a stable JSON projection of each API flight for hashing
- **Usage**: `observation_content_hash()` powers `INSERT ... ON CONFLICT DO NOTHING`

### `src/schema_upgrade.py`
- **Purpose**: Idempotent PostgreSQL patches (new columns, partial unique index, `ingested_at` tz)
- **Usage**: `python -m src.schema_upgrade` or invoked from `init_database`

### `src/api_main.py`
- **Purpose**: Small FastAPI app (`/health`, `/stats/observations`)

### `src/init_database.py`
- **Purpose**: Database initialization script
- **Contents**:
  - `init_database()` function that creates all database tables
  - Imports models to ensure they're registered with SQLAlchemy
- **Usage**: Run `python -m src.init_database` to create tables before first use

### `src/main.py`
- **Purpose**: Main data collection script
- **Contents**:
  - `parse_flight_data()` - Converts ISO datetime strings to Python datetime objects
  - `save_flight_data()` - Saves flight data from API to PostgreSQL database
  - `main()` - Orchestrates the data collection process:
    1. Creates AviationstackClient
    2. Fetches flight data (currently 100 active flights)
    3. Parses and saves data to database
- **Current Configuration**:
  - Fetches 100 flights with "active" status
  - Can be modified to filter by airline, airport, etc.

## Data Flow

1. **Scheduler** (`scheduler.py`) triggers data collection every 8 hours
2. **Main Script** (`src/main.py`) runs the collection process
3. **API Client** (`src/aviationstack_client.py`) fetches data from Aviationstack API
4. **Data Processing** (`src/main.py`) parses the JSON response
5. **Database** (`src/database.py` + `src/models.py`) stores the flight data in PostgreSQL
6. **Repeat** - The cycle continues every 8 hours

## Setup Checklist

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Create `.env` file with `AVIATIONSTACK_API_KEY` and database credentials
3. ✅ Set up PostgreSQL database
4. ✅ Initialize database: `python -m src.init_database`
5. ✅ Test single run: `python -m src.main`
6. ✅ Start scheduler: `python scheduler.py`

## Future Enhancements

- Analytics module for analyzing collected data
- FastAPI endpoints for querying flight reliability metrics
- Machine learning models for predicting delays
- Data visualization dashboards

