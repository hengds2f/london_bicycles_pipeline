import os
from google.cloud import bigquery
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURATION ---
# Replace these with your actual GCP Project ID and BigQuery Dataset ID
PROJECT_ID = 'bigdatads2f'
DATASET_ID = 'london_bikes'
# ---------------------

def ingest_data():
    logging.info("Starting data ingestion from BigQuery Public to Personal BigQuery Dataset.")
    
    if PROJECT_ID == 'your_project_id' or DATASET_ID == 'your_dataset_id':
        logging.error("Please configure PROJECT_ID and DATASET_ID in ingestion.py")
        raise ValueError("Missing GCP Project Configuration")

    client = bigquery.Client(project=PROJECT_ID)
    
    try:
        # 1. Create target dataset if it doesn't exist
        dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US" # Change location if needed
        dataset = client.create_dataset(dataset, exists_ok=True)
        logging.info(f"Dataset {dataset_ref} is ready.")

        # 2. Copy Stations Data
        target_stations_table = f"{PROJECT_ID}.{DATASET_ID}.raw_cycle_stations"
        stations_query = f"""
            CREATE OR REPLACE TABLE `{target_stations_table}` AS
            SELECT id, name, bikes_count, docks_count, install_date, latitude, longitude 
            FROM `bigquery-public-data.london_bicycles.cycle_stations`
        """
        logging.info(f"Copying stations data to {target_stations_table}...")
        job = client.query(stations_query)
        job.result() # Wait for job to complete
        logging.info("Stations data copied successfully.")

        # 3. Copy Trips Data (Sample of 100k)
        target_trips_table = f"{PROJECT_ID}.{DATASET_ID}.raw_cycle_hire"
        trips_query = f"""
            CREATE OR REPLACE TABLE `{target_trips_table}` AS
            SELECT rental_id, duration, bike_id, end_date, end_station_id, start_date, start_station_id 
            FROM `bigquery-public-data.london_bicycles.cycle_hire`
            LIMIT 100000
        """
        logging.info(f"Copying trips data to {target_trips_table}...")
        job = client.query(trips_query)
        job.result() # Wait for job to complete
        logging.info("Trips data copied successfully.")

    except Exception as e:
        logging.error(f"Error during BigQuery ingestion: {e}")
        raise e

if __name__ == "__main__":
    ingest_data()
