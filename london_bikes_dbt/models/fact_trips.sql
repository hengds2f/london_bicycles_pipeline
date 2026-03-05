{{ config(materialized='table') }}

SELECT 
    rental_id AS trip_id,
    duration AS duration_sec,
    duration / 60.0 AS duration_min, -- Derived column
    bike_id,
    start_date,
    start_station_id,
    end_date,
    end_station_id
FROM `bigdatads2f.london_bikes.cycle_hire`
WHERE rental_id IS NOT NULL 
  AND start_station_id IS NOT NULL
  AND end_station_id IS NOT NULL
  AND duration > 0 -- Data cleaning
