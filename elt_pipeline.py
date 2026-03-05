from google.cloud import bigquery
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURATION ---
# Replace these with your actual GCP Project ID and BigQuery Dataset ID
PROJECT_ID = 'bigdatads2f'
DATASET_ID = 'london_bikes'
# ---------------------

def run_elt():
    logging.info("Starting ELT process using BigQuery natively.")
    
    if PROJECT_ID == 'your_project_id' or DATASET_ID == 'your_dataset_id':
        logging.error("Please configure PROJECT_ID and DATASET_ID in elt_pipeline.py")
        raise ValueError("Missing GCP Project Configuration")
        
    client = bigquery.Client(project=PROJECT_ID)
    
    try:
        # 1. Transformations and Star Schema Design
        logging.info("Building Dimension: dim_stations")
        dim_stations_query = f"""
            CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.dim_stations` AS
            SELECT 
                id AS station_id,
                name AS station_name,
                bikes_count,
                docks_count,
                latitude,
                longitude,
                install_date
            FROM `{PROJECT_ID}.{DATASET_ID}.raw_cycle_stations`
            WHERE id IS NOT NULL
        """
        client.query(dim_stations_query).result()
        
        logging.info("Building Fact: fact_trips (with derived columns and cleaning)")
        fact_trips_query = f"""
            CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.fact_trips` AS
            SELECT 
                rental_id AS trip_id,
                duration AS duration_sec,
                duration / 60.0 AS duration_min, -- Derived column
                bike_id,
                start_date,
                start_station_id,
                end_date,
                end_station_id
            FROM `{PROJECT_ID}.{DATASET_ID}.raw_cycle_hire`
            WHERE rental_id IS NOT NULL 
              AND start_station_id IS NOT NULL
              AND end_station_id IS NOT NULL
              AND duration > 0 -- Data cleaning
        """
        client.query(fact_trips_query).result()
        
        logging.info("ELT transformations complete.")
        
        # 2. Data Quality Testing
        logging.info("Starting Data Quality Tests...")
        
        # Test 1: Null values in PK
        null_test_trips_query = f"SELECT COUNT(*) as cnt FROM `{PROJECT_ID}.{DATASET_ID}.fact_trips` WHERE trip_id IS NULL"
        null_test_trips = list(client.query(null_test_trips_query).result())[0].cnt
        assert null_test_trips == 0, f"DQ Test Failed: Found {null_test_trips} null trip_ids!"
        
        null_test_stations_query = f"SELECT COUNT(*) as cnt FROM `{PROJECT_ID}.{DATASET_ID}.dim_stations` WHERE station_id IS NULL"
        null_test_stations = list(client.query(null_test_stations_query).result())[0].cnt
        assert null_test_stations == 0, f"DQ Test Failed: Found {null_test_stations} null station_ids!"
        
        # Test 2: Duplicates
        duplicate_trips_query = f"""
            SELECT trip_id, COUNT(*) as cnt
            FROM `{PROJECT_ID}.{DATASET_ID}.fact_trips`
            GROUP BY trip_id 
            HAVING COUNT(*) > 1
        """
        duplicate_trips = list(client.query(duplicate_trips_query).result())
        assert len(duplicate_trips) == 0, f"DQ Test Failed: Found {len(duplicate_trips)} duplicate trip_ids!"
        
        duplicate_stations_query = f"""
            SELECT station_id, COUNT(*) as cnt
            FROM `{PROJECT_ID}.{DATASET_ID}.dim_stations`
            GROUP BY station_id 
            HAVING COUNT(*) > 1
        """
        duplicate_stations = list(client.query(duplicate_stations_query).result())
        assert len(duplicate_stations) == 0, f"DQ Test Failed: Found {len(duplicate_stations)} duplicate station_ids!"
        
        # Test 3: Referential Integrity
        missing_start_stations_query = f"""
            SELECT COUNT(*) as cnt
            FROM `{PROJECT_ID}.{DATASET_ID}.fact_trips` f
            LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.dim_stations` s ON f.start_station_id = s.station_id
            WHERE s.station_id IS NULL
        """
        missing_start_stations = list(client.query(missing_start_stations_query).result())[0].cnt
        if missing_start_stations > 0:
            logging.warning(f"DQ Warning: {missing_start_stations} trips have unknown start_station_id.")
            
        logging.info("Data Quality Tests Passed successfully.")
        
    except Exception as e:
        logging.error(f"ELT/DQ Process failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_elt()
