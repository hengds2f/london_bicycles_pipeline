# London Bicycles End-to-End Data Pipeline

This repository contains an end-to-end Data Engineering pipeline that processes the `london_bicycles` dataset from Google BigQuery Public Data. It performs Data Ingestion, ELT Transformations, Data Quality Testing, and Exploratory Data Analysis entirely within Google BigQuery using Python.

## Pipeline Architecture
1. **Source Data**: `bigquery-public-data.london_bicycles`
2. **Data Warehouse**: Google BigQuery (Personal Dataset: `london_bikes` in Project: `bigdatads2f`)
3. **Ingestion**: Python copies raw public data directly into the personal BigQuery dataset.
4. **ELT & Data Quality**: Python executes native BigQuery SQL (DDL and DML) to transform the raw tables into a Star Schema (`dim_stations`, `fact_trips`). It immediately runs Data Quality validation queries (checks for nulls, duplicates, and referential integrity).
5. **Analysis**: Python queries the Star Schema, pulling aggregate metrics down to Pandas DataFrames for generating Seaborn/Matplotlib visualizations.
6. **Orchestration**: A sleek python `schedule` script sequentially orchestrates the entire flow.

## Prerequisites
1. **Python 3.8+** installed on your system.
2. **Google Cloud Account** with a project (`bigdatads2f`) and billing enabled.
3. **Application Default Credentials**: You must be authenticated to your GCP project.
   - Install the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
   - Authenticate by running the following in your terminal:
     ```bash
     gcloud auth application-default login
     ```

## Setup Instructions

1. **Clone or Navigate to the Repository:**
   ```bash
   cd c:\Users\user\Documents\Module2\london_bicycles_pipeline
   ```

2. **(Optional) Create a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Pipeline

The pipeline is fully orchestrated and scheduled by a single script. To run the data ingestion, transformations, tests, and analysis all sequentially, simply execute:

```bash
python orchestrator.py
```

This will run the pipeline once immediately, and then keep the process alive to schedule runs every day at midnight. (You can exit the script safely with `Ctrl+C` after the first run completes if you do not want it running permanently).

## Generating Documentation

A script is provided to automatically generate a PDF executive report containing your Data Architecture, Technical Justifications, and the Visualizations synthesized during the Analysis phase.

```bash
python generate_docs.py
```
This will output `london_bicycles_report.pdf` into the repository.

You can also find the Data Architecture mapping stored in `pipeline_architecture.drawio`

## Repository Structure
- `ingestion.py`: Executes data extraction from BigQuery Public Data to Personal BigQuery raw tables.
- `elt_pipeline.py`: Executes Star Schema DDL/DML and Data Quality Validation queries.
- `analysis.py`: Performs Exploratory Data Analysis and generates `.png` charts.
- `orchestrator.py`: Invokes the entire pipeline seamlessly.
- `requirements.txt`: Project package dependencies.
- `analysis_output/`: Directory where generated charts are saved.
