from google.cloud import bigquery
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURATION ---
PROJECT_ID = 'bigdatads2f'
# ---------------------

def ingest_data():
    """ 
    Since the raw data already exists in your dataset per the project requirements, 
    this script acts as a Pre-Flight validation check to ensure the connection 
    is established and the source tables are available before the ELT runs.
    """
    logging.info("Validating connection to BigQuery and presence of raw dataset tables.")
    
    try:
        client = bigquery.Client(project=PROJECT_ID)
        
        # Check tables in london_bikes
        tables = [table.table_id for table in client.list_tables('london_bikes')]
        
        if 'cycle_hire' not in tables or 'cycle_stations' not in tables:
            logging.error(f"Missing one or more required raw tables in dataset {PROJECT_ID}.london_bikes")
            logging.error(f"Found tables: {tables}")
            sys.exit(1)
            
        logging.info("Validation successful: 'cycle_hire' and 'cycle_stations' are present and queryable.")

    except Exception as e:
        logging.error(f"Error during BigQuery source validation: {e}")
        raise e

if __name__ == "__main__":
    ingest_data()
