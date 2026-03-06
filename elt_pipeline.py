import os
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
    logging.info("Starting ELT process using BigQuery.")
    client = bigquery.Client(project=PROJECT_ID)
    
    try:
        # Phase B: ELT Pipeline Transformations
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
            FROM `{PROJECT_ID}.{DATASET_ID}.cycle_stations`
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
            FROM `{PROJECT_ID}.{DATASET_ID}.cycle_hire`
            WHERE rental_id IS NOT NULL 
              AND start_station_id IS NOT NULL
              AND end_station_id IS NOT NULL
              AND duration > 0 -- Data cleaning
        """
        client.query(fact_trips_query).result()
        
        logging.info("ELT transformations complete.")
        
        # Phase C: Data Quality Testing
        logging.info("Starting Data Quality Tests...")
        import great_expectations as gx
        
        # Create an ephemeral data context
        context = gx.get_context(mode="ephemeral")
        
        logging.info("Connecting Great Expectations to BigQuery...")
        # configure datasource
        datasource = context.sources.add_sql(
            name="bq_datasource", 
            connection_string=f"bigquery://{PROJECT_ID}/{DATASET_ID}"
        )
        
        # Add assets
        asset_trips = datasource.add_table_asset(name="fact_trips_asset", table_name="fact_trips")
        asset_stations = datasource.add_table_asset(name="dim_stations_asset", table_name="dim_stations")
        
        # Get validators
        context.add_or_update_expectation_suite(expectation_suite_name="trips_suite")
        batch_request_trips = asset_trips.build_batch_request()
        validator_trips = context.get_validator(batch_request=batch_request_trips, expectation_suite_name="trips_suite")
        
        context.add_or_update_expectation_suite(expectation_suite_name="stations_suite")
        batch_request_stations = asset_stations.build_batch_request()
        validator_stations = context.get_validator(batch_request=batch_request_stations, expectation_suite_name="stations_suite")
        
        # C.2 Test 1: Null values
        res_null_trips = validator_trips.expect_column_values_to_not_be_null("trip_id")
        assert res_null_trips.success, "DQ Test Failed: Found null trip_ids!"
        
        res_null_stations = validator_stations.expect_column_values_to_not_be_null("station_id")
        assert res_null_stations.success, "DQ Test Failed: Found null station_ids!"
        
        # C.2 Test 2: Duplicates
        res_dup_trips = validator_trips.expect_column_values_to_be_unique("trip_id")
        assert res_dup_trips.success, "DQ Test Failed: Found duplicates in fact_trips!"
        
        res_dup_stations = validator_stations.expect_column_values_to_be_unique("station_id")
        assert res_dup_stations.success, "DQ Test Failed: Found duplicates in dim_stations!"
        
        # C.2 Test 3: Referential Integrity
        # Query stations to pass as a set
        stations = [row.station_id for row in client.query(f"SELECT station_id FROM `{PROJECT_ID}.{DATASET_ID}.dim_stations`").result()]
        res_ref_integrity = validator_trips.expect_column_values_to_be_in_set("start_station_id", value_set=stations)
        if not res_ref_integrity.success:
            logging.warning("DQ Warning: trips have missing referential start_station_id.")
            
        logging.info("Data Quality Tests Passed successfully.")
        
    except Exception as e:
        logging.error(f"ELT/DQ Process failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_elt()
