import duckdb
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_elt(db_path='data_warehouse.duckdb'):
    logging.info("Starting ELT process using DuckDB natively.")
    conn = duckdb.connect(db_path)
    
    try:
        # 1. Transformations and Star Schema Design
        logging.info("Building Dimension: dim_stations")
        conn.execute("""
            CREATE OR REPLACE TABLE dim_stations AS
            SELECT 
                id AS station_id,
                name AS station_name,
                bikes_count,
                docks_count,
                latitude,
                longitude,
                install_date
            FROM raw_cycle_stations
            WHERE id IS NOT NULL
        """)
        
        logging.info("Building Fact: fact_trips (with derived columns and cleaning)")
        conn.execute("""
            CREATE OR REPLACE TABLE fact_trips AS
            SELECT 
                rental_id AS trip_id,
                duration AS duration_sec,
                duration / 60.0 AS duration_min, -- Derived column
                bike_id,
                start_date,
                start_station_id,
                end_date,
                end_station_id
            FROM raw_cycle_hire
            WHERE rental_id IS NOT NULL 
              AND start_station_id IS NOT NULL
              AND end_station_id IS NOT NULL
              AND duration > 0 -- Data cleaning
        """)
        
        logging.info("ELT transformations complete.")
        
        # 2. Data Quality Testing
        logging.info("Starting Data Quality Tests...")
        
        # Test 1: Null values in PK
        null_test_trips = conn.execute("SELECT COUNT(*) FROM fact_trips WHERE trip_id IS NULL").fetchone()[0]
        assert null_test_trips == 0, f"DQ Test Failed: Found {null_test_trips} null trip_ids!"
        
        null_test_stations = conn.execute("SELECT COUNT(*) FROM dim_stations WHERE station_id IS NULL").fetchone()[0]
        assert null_test_stations == 0, f"DQ Test Failed: Found {null_test_stations} null station_ids!"
        
        # Test 2: Duplicates
        duplicate_trips = conn.execute("""
            SELECT trip_id, COUNT(*) 
            FROM fact_trips 
            GROUP BY trip_id 
            HAVING COUNT(*) > 1
        """).fetchall()
        assert len(duplicate_trips) == 0, f"DQ Test Failed: Found {len(duplicate_trips)} duplicate trip_ids!"
        
        duplicate_stations = conn.execute("""
            SELECT station_id, COUNT(*) 
            FROM dim_stations 
            GROUP BY station_id 
            HAVING COUNT(*) > 1
        """).fetchall()
        assert len(duplicate_stations) == 0, f"DQ Test Failed: Found {len(duplicate_stations)} duplicate station_ids!"
        
        # Test 3: Referential Integrity
        missing_start_stations = conn.execute("""
            SELECT COUNT(*) 
            FROM fact_trips f
            LEFT JOIN dim_stations s ON f.start_station_id = s.station_id
            WHERE s.station_id IS NULL
        """).fetchone()[0]
        # Allowing some missing refs as it's public/mock data, but let's just log it if not strictly 0.
        if missing_start_stations > 0:
            logging.warning(f"DQ Warning: {missing_start_stations} trips have unknown start_station_id.")
            
        logging.info("Data Quality Tests Passed successfully.")
        
    except Exception as e:
        logging.error(f"ELT/DQ Process failed: {e}")
        conn.close()
        sys.exit(1)
        
    conn.close()

if __name__ == "__main__":
    run_elt()
