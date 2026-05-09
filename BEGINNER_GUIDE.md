# Flight Reliability App - Complete Beginner's Guide

## What is This Project?

Imagine you want to know which airlines are reliable - which ones arrive on time, which ones are often delayed, etc. This project automatically collects information about flights from the internet and saves it to a database so you can analyze it later.

Think of it like a robot that:
1. Goes to a website (Aviationstack API) **every 8 hours** (with one run right when it starts)
2. Asks "What flights are flying right now?"
3. Writes down flight information in a notebook (database), **skipping exact duplicates**
4. Repeats on that schedule until you stop it

## What is an API?

**API** stands for "Application Programming Interface." Think of it like a menu at a restaurant:
- You (the customer) = Your program
- The menu = The API
- The kitchen = The website's database

When you order from the menu (make an API request), the kitchen (API) gives you food (data). In this case, the "food" is flight information.

**Aviationstack** is a company that collects flight data and lets other programs access it through their API. You need an API key (like a password) to use it.

## What is a Database?

A **database** is like a digital filing cabinet. Instead of paper files, it stores information in an organized way that computers can quickly search and retrieve.

**PostgreSQL** is a specific type of database (like how "Microsoft Word" is a specific type of word processor). It's free, powerful, and commonly used.

Think of it like this:
- **Table** = A drawer in the filing cabinet
- **Row** = One file/folder in the drawer
- **Column** = A specific piece of information (like "name" or "date")

In this project, we have a table called "flights" where each row is one flight, and each column is a piece of information about that flight (airline name, departure time, etc.).

## What is Python?

**Python** is a programming language - a way to tell computers what to do. It's like giving instructions in a language the computer understands.

Think of it like this:
- **English** = How humans communicate
- **Python** = How to communicate with computers

Python is popular because it's relatively easy to read and write (compared to other programming languages).

## Understanding the Files

### 1. `requirements.txt` - The Shopping List
This file lists all the "tools" (libraries/packages) your project needs to work. It's like a shopping list before you start cooking.

**Example:** If you want to make cookies, you need flour, sugar, eggs. Similarly, this project needs:
- `requests` - Tool to talk to websites/APIs
- `python-dotenv` - Tool to read secret passwords from a file
- `pandas` - Tool to work with data (like Excel for Python)
- `sqlalchemy` - Tool to talk to databases
- etc.

**How to use:** Run `pip install -r requirements.txt` to automatically download and install all these tools.

### 2. `.env` File - The Secret Password File
This file (you need to create it) stores secret information like passwords and API keys. It's like a safe where you keep your house keys.

**Why it's separate:** You don't want to accidentally share your passwords when you share your code. The `.gitignore` file makes sure this file never gets uploaded to the internet.

**Example content:**
```
AVIATIONSTACK_API_KEY=your_secret_key_here
DB_PASSWORD=your_database_password
```

### 3. `src/config.py` - The Settings File
This file reads the secrets from `.env` and makes them available to your program. It's like a translator that reads your password file and tells the rest of the program what the settings are.

**What it does:**
- Reads your API key from `.env`
- Reads your database password from `.env`
- Sets up the database connection string (like an address to find your database)

### 4. `src/aviationstack_client.py` - The Website Talker
This file contains code that knows how to talk to the Aviationstack website. It's like having a friend who knows how to order from a specific restaurant.

**What it does:**
- Takes your API key
- Makes requests to the Aviationstack website
- Gets flight data back
- Handles errors (like if the website is down)

**The `AviationstackClient` class:** Think of a "class" as a blueprint. Like a blueprint for a house, a class is a blueprint for an object. In this case, it's a blueprint for something that can talk to the Aviationstack API.

### 5. `src/database.py` - The Database Connector
This file sets up the connection to your database. It's like installing a phone line to your database so your program can talk to it.

**What it does:**
- Creates a connection to PostgreSQL
- Sets up a "session" (like opening a conversation with the database)
- Provides tools for other files to use the database

### 6. `src/models.py` - The Data Structure
This file defines what information we want to store about each flight. It's like designing a form that you'll fill out for each flight.

**The `Flight` class:** This is like a template. For each flight, we create a "Flight" object that has:
- Flight number (like "UA123")
- Airline name
- Departure airport
- Arrival airport
- Scheduled times
- Actual times
- Delays
- etc.

**Why it's important:** This tells the database exactly what columns to create in the "flights" table.

### 7. `src/init_database.py` - The Table Creator
This file creates the actual table in your database. It's like building the filing cabinet drawer before you can put files in it.

**What it does:**
- Looks at your models (the Flight class)
- Creates a table in PostgreSQL with all the right columns
- Only needs to be run once (or when you change the structure)

### 8. `src/main.py` - The Main Worker
This is the "brain" of your program - it coordinates everything. It's like the conductor of an orchestra, telling everyone what to do.

**What it does step by step:**
1. Creates an AviationstackClient (the website talker)
2. Asks the API for flight data (gets 100 active flights)
3. For each flight, extracts the important information
4. Converts dates/times to the right format
5. Saves each flight to the database
6. Reports success or errors

**Functions:**
- `parse_flight_data()` - Converts date strings (like "2024-01-15T10:30:00Z") into Python date objects that the database can understand
- `save_flight_data()` - Takes flight data and saves it to the database
- `main()` - The main function that runs everything

### 9. `scheduler.py` - The Timer
This file runs the collector on startup, then automatically **every 8 hours**. It's like setting a long-interval alarm clock for data collection.

**What it does:**
- Uses the `schedule` library (a tool for scheduling tasks)
- Tells the program: "Run `main()` now, then again every 8 hours"
- Runs immediately when you start it
- Keeps running until you stop it (Ctrl+C)
- Handles errors gracefully (if one run fails, it keeps going)

## How Everything Works Together

Here's the flow in simple terms:

```
1. You run scheduler.py
   ↓
2. Scheduler runs `main` once, then sleeps until the next **8-hour** boundary
   ↓
3. main.py creates an AviationstackClient
   ↓
4. AviationstackClient uses config.py to get the API key
   ↓
5. AviationstackClient asks Aviationstack website for flight data
   ↓
6. Aviationstack website sends back flight data (JSON format)
   ↓
7. main.py reads the data and extracts important info
   ↓
8. main.py uses database.py to connect to PostgreSQL
   ↓
9. main.py fingerprints each observation and avoids saving exact duplicates (`content_hash`)
   ↓
10. New observations are inserted into PostgreSQL
    ↓
11. Scheduler waits until the next 8-hour run and repeats
```

## Key Concepts Explained Simply

### What is JSON?
**JSON** (JavaScript Object Notation) is a way to format data that both humans and computers can read. It's like a structured list.

**Example:**
```json
{
  "name": "John",
  "age": 30,
  "city": "New York"
}
```

The API sends flight data in JSON format, and Python can easily read it.

### What is SQLAlchemy?
**SQLAlchemy** is a tool that lets you work with databases using Python code instead of writing SQL (database language) directly. It's like a translator between Python and the database.

**Why it's useful:** Instead of writing complex database commands, you can write simple Python code like:
```python
flight = Flight(airline_iata="UA", flight_iata="UA123")
db.add(flight)
db.commit()
```

### What is a Session?
A **session** is like opening a conversation with the database. You:
1. Open a session (start talking)
2. Make changes (add, update, delete data)
3. Commit (save your changes)
4. Close the session (end the conversation)

### What is an ORM?
**ORM** (Object-Relational Mapping) is a fancy way of saying "turning database tables into Python objects." Instead of thinking about rows and columns, you think about objects with properties.

**Example:**
- **Database way:** "Insert a row into the flights table with column values..."
- **ORM way:** "Create a Flight object and save it"

## Common Terms

- **Module** - A Python file that contains code you can use in other files
- **Package** - A folder containing multiple modules (like the `src/` folder)
- **Import** - Bringing code from one file into another (like `from src.main import main`)
- **Function** - A block of code that does a specific task (like `def main():`)
- **Class** - A blueprint for creating objects
- **Object** - An instance of a class (like one specific flight)
- **Variable** - A name that stores a value (like `api_key = "abc123"`)
- **Parameter** - Information you pass to a function
- **Return** - What a function gives back after it runs

## Setting Up the Project (Step by Step)

### Step 1: Install Python
Make sure Python is installed on your computer. You can download it from python.org.

### Step 2: Install PostgreSQL
Download and install PostgreSQL (the database). During installation, remember the password you set for the "postgres" user.

### Step 3: Create a Database
Open PostgreSQL and create a new database (or use the default "postgres" database).

### Step 4: Install Project Tools
Open a terminal/command prompt in your project folder and run:
```bash
pip install -r requirements.txt
```
This installs all the tools your project needs.

### Step 5: Create .env File
Create a file named `.env` in your project root with:
```
AVIATIONSTACK_API_KEY=your_actual_api_key_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_database_password
```

### Step 6: Initialize Database
Run this once to create the tables:
```bash
python -m src.init_database
```

### Step 7: Test It
Run the main script once to make sure everything works:
```bash
python -m src.main
```

### Step 8: Start the Scheduler
Run the scheduler to collect data automatically:
```bash
python scheduler.py
```

## Troubleshooting Common Issues

### "Module not found" error
**Problem:** Python can't find a file you're trying to import.
**Solution:** Make sure you're running commands from the project root folder, and all files are in the right places.

### "API key not set" error
**Problem:** The program can't find your API key.
**Solution:** Make sure your `.env` file exists and has `AVIATIONSTACK_API_KEY=your_key_here`

### "Can't connect to database" error
**Problem:** The program can't reach PostgreSQL.
**Solution:** 
- Make sure PostgreSQL is running
- Check that your database credentials in `.env` are correct
- Make sure the database exists

### "Table doesn't exist" error
**Problem:** The database table hasn't been created yet.
**Solution:** Run `python -m src.init_database` first.

## What Happens Over Time?

As the scheduler runs every 8 hours:
- Your database accumulates **new or changed observations** — exact duplicates from the API are skipped
- You can see patterns (which airlines are often delayed, which routes have issues, etc.)
- You can analyze the data to make predictions
- You can build reports and visualizations

The more trustworthy rows you accumulate, the better insights you can get!

## Next Steps

Once you understand this project, you might want to:
1. Add more data fields to collect
2. Create reports analyzing the data
3. Build a website to display the data
4. Create predictions using machine learning
5. Add alerts for significant delays

But first, make sure you understand how the basic data collection works!

