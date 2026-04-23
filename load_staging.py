import psycopg2

def create_staging_table(conn):
    print("Creating staging table...")

    cursor = conn.cursor()
    cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS staging;

        CREATE TABLE IF NOT EXISTS staging.air_quality_cleaned (
            id SERIAL PRIMARY KEY,
            city TEXT,
            lon FLOAT,
            lat FLOAT,
            aqi INTEGER,
            aqi_category TEXT,
            co FLOAT,
            no FLOAT,
            no2 FLOAT,
            o3 FLOAT,
            so2 FLOAT,
            pm2_5 FLOAT,
            pm10 FLOAT,
            nh3 FLOAT,
            time TIMESTAMP,
            hour INTEGER,
            day DATE,
            inserted_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    print("Staging table ready.")


def load_staging_data(conn, transformed_data):
    print("Loading data into staging...")

    cursor = conn.cursor()

    for row in transformed_data:
        cursor.execute("""
            INSERT INTO staging.air_quality_cleaned (
                city, lon, lat, aqi, aqi_category,
                co, no, no2, o3, so2,
                pm2_5, pm10, nh3,
                time, hour, day
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row["city"],
            row["lon"],
            row["lat"],
            row["aqi"],
            row["aqi_category"],
            row["co"],
            row["no"],
            row["no2"],
            row["o3"],
            row["so2"],
            row["pm2_5"],
            row["pm10"],
            row["nh3"],
            row["time"],
            row["hour"],
            row["day"]
        ))

    conn.commit()
    print("Staging load complete.")