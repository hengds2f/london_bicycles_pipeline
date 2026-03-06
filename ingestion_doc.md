# Documentation for `ingestion.py`

This document provides a line-by-line explanation of the `ingestion.py` script.

- **Line 1:** `from google.cloud import bigquery` - Imports the BigQuery client library to interact with Google BigQuery.
- **Line 2:** `import logging` - Imports the standard Python logging library to log execution events, errors, and information.
- **Line 3:** `import sys` - Imports the sys module to interact with the Python interpreter, allowing the script to terminate on error.
- **Line 4:** Blank line for readability.
- **Line 5:** `# Configure logging` - A comment indicating the next line will set up the logging configuration.
- **Line 6:** `logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')` - Configures the root logger to capture messages at standard INFO level or above, including timestamps, log level, and the message output.
- **Line 7:** Blank line.
- **Line 8:** `# --- CONFIGURATION ---` - A comment section divider.
- **Line 9:** `PROJECT_ID = 'bigdatads2f'` - Defines the Google Cloud Project ID constant that will be used.
- **Line 10:** `# ---------------------` - A comment section divider.
- **Line 11:** Blank line.
- **Line 12:** `def ingest_data():` - Defines a function named `ingest_data` to encapsulate the validation logic.
- **Lines 13-17:** A multiline docstring explaining that the script acts as a pre-flight validation check to make sure connections exist and tables are available before the ELT runs.
- **Line 18:** `logging.info("Validating connection to BigQuery and presence of raw dataset tables.")` - Logs an informational message indicating the validation check is starting.
- **Line 19:** Blank line.
- **Line 20:** `try:` - Starts a try-except block to catch potential errors during the connection or validation phase.
- **Line 21:** `client = bigquery.Client(project=PROJECT_ID)` - Initializes a BigQuery client using the specified `PROJECT_ID`.
- **Line 22:** Blank line.
- **Line 23:** `# Check tables in london_bikes` - Comment indicating the following lines will check for table existence.
- **Line 24:** `tables = [table.table_id for table in client.list_tables('london_bikes')]` - Fetches the list of tables inside the 'london_bikes' dataset and uses list comprehension to extract just their table IDs.
- **Line 25:** Blank line.
- **Line 26:** `if 'cycle_hire' not in tables or 'cycle_stations' not in tables:` - Checks if either of the two required tables (`cycle_hire` or `cycle_stations`) is missing from the list.
- **Line 27:** `logging.error(...)` - If missing, logs an error specifying that a required raw table was not found.
- **Line 28:** `logging.error(f"Found tables: {tables}")` - Logs the tables that *were* found for debugging purposes.
- **Line 29:** `sys.exit(1)` - Terminates the script with an exit code of 1, signaling a failure.
- **Line 30:** Blank line.
- **Line 31:** `logging.info(...)` - If tables exist, logs a success message confirming the tables are available.
- **Line 32:** Blank line.
- **Line 33:** `except Exception as e:` - Catches any unexpected exception that occurred during the `try` block.
- **Line 34:** `logging.error(...)` - Logs the specific error message caught by the exception.
- **Line 35:** `raise e` - Re-raises the exception to ensure the failure propagates up.
- **Line 36:** Blank line.
- **Line 37:** `if __name__ == "__main__":` - A standard Python idiom; confirms the script is being run directly.
- **Line 38:** `ingest_data()` - Calls the main `ingest_data` function if the script executes directly.
- **Line 39:** Blank line at the end of the file.
