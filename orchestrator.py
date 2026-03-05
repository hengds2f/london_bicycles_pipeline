import schedule
import time
import logging
from ingestion import ingest_data
from elt_pipeline import run_elt
from analysis import analyze_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    logging.info("Starting London Bicycles Data Pipeline...")
    
    try:
        logging.info("Step 1: Ingestion")
        ingest_data('data_warehouse.duckdb')
        
        logging.info("Step 2: ELT & DQ")
        run_elt('data_warehouse.duckdb')
        
        logging.info("Step 3: Analysis")
        analyze_data('data_warehouse.duckdb', 'analysis_output')
        
        logging.info("Pipeline Execution Complete!")
        
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    # Run once immediately
    run_pipeline()
    
    # Schedule regular runs
    logging.info("Scheduling pipeline to run every day at midnight...")
    schedule.every().day.at("00:00").do(run_pipeline)
    
    # NOTE: Uncomment the following to run the scheduler continuously
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)
