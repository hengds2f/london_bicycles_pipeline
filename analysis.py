import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_data(db_path='data_warehouse.db', output_dir='analysis_output'):
    logging.info("Starting exploratory data analysis.")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    conn = duckdb.connect(db_path)
    
    # 1. Total Trips and Key Metrics
    try:
        metrics_df = conn.execute("SELECT count(*) as total_trips, avg(duration_sec) as avg_duration_sec FROM fact_trips").df()
        logging.info(f"Total Trips: {metrics_df['total_trips'][0]}")
        logging.info(f"Average Duration: {metrics_df['avg_duration_sec'][0]:.2f} seconds")
    except Exception as e:
        logging.error(f"Could not calculate metrics: {e}")
        
    # 2. Top 10 Start Stations
    try:
        top_stations_query = """
        SELECT s.name as station_name, count(t.trip_id) as trip_count
        FROM fact_trips t
        JOIN dim_stations s ON t.start_station_id = s.station_id
        GROUP BY s.name
        ORDER BY trip_count DESC
        LIMIT 10
        """
        top_stations_df = conn.execute(top_stations_query).df()
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=top_stations_df, x='trip_count', y='station_name', palette='viridis')
        plt.title('Top 10 Busiest Start Stations')
        plt.xlabel('Number of Trips')
        plt.ylabel('Station Name')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'top_10_start_stations.png'))
        plt.close()
        logging.info("Saved top 10 start stations plot.")
        
    except Exception as e:
        logging.error(f"Could not generate top stations plot: {e}")
        
    # 3. Trips by Hour
    try:
        hourly_query = """
        SELECT hour(start_date) as start_hour, count(trip_id) as trip_count
        FROM fact_trips
        GROUP BY 1
        ORDER BY 1
        """
        hourly_df = conn.execute(hourly_query).df()
        
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=hourly_df, x='start_hour', y='trip_count', marker='o', color='b')
        plt.title('Trips by Hour of Day')
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Trips')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'trips_by_hour.png'))
        plt.close()
        logging.info("Saved trips by hour plot.")
        
    except Exception as e:
        logging.error(f"Could not generate hourly trips plot: {e}")

    conn.close()
    logging.info("Exploratory data analysis complete.")

if __name__ == "__main__":
    analyze_data()
