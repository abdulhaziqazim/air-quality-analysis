import pandas as pd

def transform_from_db(conn):
    print("Reading raw data from Postgres...")

    query = """
        SELECT *
        FROM dev.raw_air_quality_data
    """

    df = pd.read_sql(query, conn)

    print(f"Fetched {len(df)} rows")

    # --- Cleaning ---
    df = df.dropna(subset=['aqi'])

    pollutant_cols = ['co','no','no2','o3','so2','pm2_5','pm10','nh3']
    df[pollutant_cols] = df[pollutant_cols].fillna(0)

    # --- Feature Engineering ---
    df['time'] = pd.to_datetime(df['time'])

    aqi_map = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }

    df['aqi_category'] = df['aqi'].map(aqi_map)
    df['hour'] = df['time'].dt.hour
    df['day'] = df['time'].dt.date

    # Optional: remove duplicates
    df = df.drop_duplicates(subset=['time'])

    final_df = df[[
        'city','lon','lat','aqi','aqi_category',
        'co','no','no2','o3','so2',
        'pm2_5','pm10','nh3',
        'time','hour','day'
    ]]

    print(f"Transformed {len(final_df)} rows")

    return final_df.to_dict(orient='records')