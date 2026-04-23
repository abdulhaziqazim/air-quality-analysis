CREATE SCHEMA IF NOT EXISTS staging;

DROP TABLE IF EXISTS staging.air_quality_cleaned;

CREATE TABLE staging.air_quality_cleaned AS
SELECT
    city,
    lon,
    lat,
    aqi,
    co,
    no,
    no2,
    o3,
    so2,
    pm2_5,
    pm10,
    nh3,
    time,
    DATE(time) AS day,
    EXTRACT(HOUR FROM time) AS hour,

    CASE 
        WHEN aqi = 1 THEN 'Good'
        WHEN aqi = 2 THEN 'Fair'
        WHEN aqi = 3 THEN 'Moderate'
        WHEN aqi = 4 THEN 'Poor'
        ELSE 'Very Poor'
    END AS aqi_category

FROM dev.raw_air_quality_data
WHERE aqi IS NOT NULL;