# Skill Assignment Project

This repository contains scripts for analyzing an `online_retail` database using Python.

## Project Structure

- `821160-dbanalysis.py` - script connecting to SQL Server using SQLAlchemy and extracting data with pandas.
- `821160-sqldbanalysis.py` - Correct Workable script (possibly for SQL queries or analysis).
- `dbconnect.py` - (if present) helper for database connection.
- `requirements.txt` - Python dependencies list.


## Setup Instructions

1. **Create a virtual environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   pip install sqlalchemy
   ```

3. **Configure database credentials:**
   Edit the script (e.g. `821160-dbanalysis.py`) and set `server`, `database`, `username`, and `password` variables appropriately.

4. **Run the application:**
   ```powershell
   .\.venv\Scripts\python.exe 821160-dbanalysis.py
   ```

## Notes

- The scripts use `pyodbc` and require an ODBC driver for SQL Server (e.g. ODBC Driver 17 for SQL Server).
- Ensure the SQL Server instance (`.\SQLEXPRESS` by default) is running and accessible.

## License

This project is provided for demonstration purposes.