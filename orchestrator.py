import schedule
import time
import logging
from ingestion import ingest_data
from elt_pipeline import run_elt

# Configure logging to display step execution
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def orchestrate_pipeline():
    """ Runs the end-to-end data pipeline targeting BigQuery sequentially. """
    logging.info("--- Starting London Bikes Daily Pipeline Execution ---")
    
    try:
        # Step 1: Ingestion
        logging.info("Step 1: Ingestion (BigQuery Public -> Personal Dataset)")
        ingest_data()
        
        # Step 2: ELT & DQ Tests
        logging.info("Step 2: ELT Transformations & Data Quality Validation on BigQuery")
        run_elt()
        
        logging.info("--- Pipeline Execution Complete! Downstream BI and Jupyter Notebook ready. ---")
        
    except Exception as e:
        logging.error(f"Pipeline execution halted due to error: {e}")

if __name__ == "__main__":
    # Execute immediately
    orchestrate_pipeline()
    
    # Schedule the pipeline to run daily at midnight
    logging.info("Scheduling pipeline to run daily at 00:00. Waiting...")
    schedule.every().day.at("00:00").do(orchestrate_pipeline)
    
    # Keep script alive to run the scheduled jobs (can exit via Ctrl+C)
    # Uncomment the while loop below if a continuous process is required on a dedicated server
    """
    while True:
        schedule.run_pending()
        time.sleep(60)
    """
