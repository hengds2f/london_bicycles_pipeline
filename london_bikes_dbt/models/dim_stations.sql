{{ config(materialized='table') }}

SELECT 
    id AS station_id,
    name AS station_name,
    bikes_count,
    docks_count,
    latitude,
    longitude,
    install_date
FROM `bigdatads2f.london_bikes.raw_cycle_stations`
WHERE id IS NOT NULL
