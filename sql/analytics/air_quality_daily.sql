CREATE SCHEMA IF NOT EXISTS analytics;

DROP TABLE IF EXISTS analytics.air_quality_daily_summary;

CREATE TABLE analytics.air_quality_daily_summary AS
SELECT
    city,
    day,
    COUNT(*) AS record_count,
    AVG(aqi) AS avg_aqi,
    MAX(aqi) AS max_aqi,
    MIN(aqi) AS min_aqi,
    AVG(pm2_5) AS avg_pm2_5,
    AVG(pm10) AS avg_pm10,
    MAX(pm2_5) AS peak_pm2_5,
    MAX(pm10) AS peak_pm10
FROM staging.air_quality_cleaned
GROUP BY city, day
ORDER BY city, day;