# Documentation for `analysis.ipynb`

This document provides a detailed explanation of the code within the `analysis.ipynb` Jupyter Notebook. Note that Jupyter Notebooks are structured as JSON files containing metadata, outputs, and source code. The line-by-line explanation below focuses on the actual Python code and Markdown text within the notebook's cells.

## Cell 1 (Markdown)
Provides the title and introduction to the analytical findings.
- **Line 1:** `# London Bicycles: Exploratory Data Analysis & Strategic Business Findings` - Header for the notebook.
- **Line 2:** Explains the connection to BigQuery and the use of pandas to execute analytical workloads for business insights.

## Cell 2 (Code)
Initializes libraries and the database connection.
- **Line 1:** `import pandas as pd` - Imports the pandas library for data manipulation.
- **Line 2:** `import matplotlib.pyplot as plt` - Imports matplotlib for plotting graphs.
- **Line 3:** `import seaborn as sns` - Imports seaborn for advanced data visualization.
- **Line 4:** `from sqlalchemy import create_engine` - Imports the database engine creator from SQLAlchemy.
- **Line 5:** `import warnings` - Imports the warnings module.
- **Line 6:** `warnings.filterwarnings('ignore')` - Suppresses runtime warnings to keep the notebook output clean.
- **Line 7:** Blank line.
- **Line 8:** `# Set visual style for executive-level charts` - Comment for styling section.
- **Line 9:** `plt.style.use('ggplot')` - Sets matplotlib to use the 'ggplot' aesthetic style.
- **Line 10:** `sns.set_palette("coolwarm")` - Sets the default color palette in seaborn.
- **Line 11:** Blank line.
- **Line 12:** `# Connect to BigQuery using SQLAlchemy` - Setup comment.
- **Line 13:** `PROJECT_ID = 'bigdatads2f'` - Defines the Google Cloud project ID.
- **Line 14:** `DATASET_ID = 'london_bikes'` - Defines the dataset ID.
- **Line 15:** `engine = create_engine(f'bigquery://{PROJECT_ID}/{DATASET_ID}')` - Creates a SQLAlchemy engine connected to BigQuery.
- **Line 16:** `print(...)` - Confirms a successful connection to the warehouse out to the console.

## Cell 3 (Markdown)
- **Lines 1-3:** Introduces "Finding 1: Revenue Is Dangerously Seasonal", explaining that trips are aggregated by month to identify seasonality.

## Cell 4 (Code)
Executes the seasonality query and plots the results.
- **Lines 1-8:** `query_seasonality = """..."""` - A SQL query that extracts the month from the start date, counts the total trips, and groups them sequentially by month.
- **Line 9:** `df_seasonality = pd.read_sql(query_seasonality, engine)` - Executes the SQL query and stores the output in a pandas DataFrame.
- **Line 10:** Blank line.
- **Line 11:** `plt.figure(figsize=(10, 5))` - Creates a plot canvas of 10x5 inches.
- **Line 12:** `sns.barplot(...)` - Generates a bar chart plotting total trips against the month.
- **Line 13:** `plt.title(...)` - Sets the chart title.
- **Line 14:** `plt.xlabel('Month of Year', fontsize=12)` - Labels the x-axis.
- **Line 15:** `plt.ylabel('Total Trips', fontsize=12)` - Labels the y-axis.
- **Line 16:** `plt.show()` - Renders the bar chart.

## Cell 5 (Markdown)
- **Lines 1-3:** Introduces "Finding 2: Revenue Opportunity Is Concentrated in Certain Hours of a Day", highlighting commuter pressures.

## Cell 6 (Code)
Executes the hourly demand query and plots it.
- **Lines 1-8:** `query_hourly = """..."""` - A SQL query extracting the hour of the day to count overall trips by hour.
- **Line 9:** `df_hourly = pd.read_sql(query_hourly, engine)` - Reads the SQL data into a DataFrame.
- **Line 10:** Blank line.
- **Line 11:** `plt.figure(figsize=(10, 5))` - Initializes the 10x5 plot.
- **Line 12:** `sns.lineplot(...)` - Plots a point-marked line graph of hourly volumes.
- **Line 13:** `plt.title(...)` - Sets the chart title.
- **Line 14:** `plt.xlabel(...)` - Sets the x-axis label.
- **Line 15:** `plt.ylabel(...)` - Sets the y-axis label.
- **Line 16:** `plt.grid(...)` - Applies a dashed grid to the background for readability.
- **Line 17:** `plt.xticks(range(0, 24))` - Sets the x-axis ticks to display every single hour.
- **Line 18:** `plt.fill_between(...)` - Subtly shades the area under the line plot line.
- **Line 19:** `plt.show()` - Displays the hour-by-hour line chart.

## Cell 7 (Markdown)
- **Lines 1-3:** Introduces "Finding 3: Demand Spikes Are Invisible Until It Is Too Late", referencing day-over-day volatility.

## Cell 8 (Code)
Evaluates volatility and day-over-day variance.
- **Lines 1-13:** `query_spikes = """..."""` - A SQL query utilizing a CTE to find daily volumes, followed by a window function (`LAG()`) to find the difference (variance) from the preceding day.
- **Line 14:** `df_spikes = pd.read_sql(query_spikes, engine)` - Fetches the data to a DataFrame.
- **Line 15:** Blank line.
- **Line 16:** `plt.figure(figsize=(12, 5))` - Creates a 12x5 plot.
- **Line 17:** `sns.lineplot(...)` - Plots the daily variance across the days of the year.
- **Line 18:** `plt.axhline(0, color='black', linestyle='--')` - Draws a solid baseline at zero variance.
- **Line 19:** `plt.title(...)` - Sets the chart title.
- **Line 20:** `plt.xlabel(...)` - Lables the x-axis (Day of Year).
- **Line 21:** `plt.ylabel(...)` - Labels the y-axis (Variance vs Previous Day).
- **Line 22:** `plt.show()` - Renders the volatility chart.

## Cell 9 (Markdown)
- **Lines 1-3:** Introduces "Finding 4: Key Volume Is Concentrated in Just a Few Stations", indicating a Pareto-style unequal distribution.

## Cell 10 (Code)
Analyzes station throughput and visualizes the top performers.
- **Lines 1-10:** `query_stations = """..."""` - A SQL query joining facts to dimensions to sum trips per station, ordering by volume descending and limiting to the top 10 rows.
- **Line 11:** `df_stations = pd.read_sql(query_stations, engine)` - Loads the top 10 station records into memory.
- **Line 12:** Blank line.
- **Line 13:** `plt.figure(figsize=(10, 6))` - Initializes a 10x6 plot figure.
- **Line 14:** `sns.barplot(...)` - Charts a horizontal bar plot mapping top stations to their trip volume in descending order.
- **Line 15:** `plt.title(...)` - Titles the plot "Top 10 High Volume Hubs".
- **Line 16:** `plt.xlabel(...)` - Lables the cumulative trips.
- **Line 17:** `plt.ylabel(...)` - Labels the station names.
- **Line 18:** `plt.show()` - Displays the final visualization.
