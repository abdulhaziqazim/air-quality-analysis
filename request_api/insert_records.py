import psycopg2
#print(mock_fetch_data())

def connect_to_db():
    print("Connecting to PostgreSQL database")
    try:
        conn = psycopg2.connect(
            host = "db",
            port = 5432,
            dbname = "postgres_db",
            user = "db_user",
            password = "db_password" 
        )

        return conn
    except psycopg2.Error as e:
        print (f"Database connection failed: {e}")
        raise

def create_table(conn):
    print("Creating table if not exist...")
    try:
        cursor = conn.cursor()
        
        cursor.execute("CREATE SCHEMA IF NOT EXISTS dev;")
        conn.commit()  # commit schema first
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dev.raw_air_quality_data (
                id SERIAL PRIMARY KEY,
                city TEXT,
                lon FLOAT,
                lat FLOAT,
                aqi INTEGER,
                co FLOAT,
                no FLOAT,
                no2 FLOAT,
                o3 FLOAT,
                so2 FLOAT,
                pm2_5 FLOAT,
                pm10 FLOAT,
                nh3 FLOAT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                UNIQUE (city, time)
            );
        """)
        conn.commit()
        print("Table was created.")
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        conn.rollback()
        raise

def insert_data(conn, data):
    print("Inserting data...")
    try:
        cursor = conn.cursor()

        records_to_insert = []

        for record in data['list']:
            records_to_insert.append((
                "Kuala Lumpur",
                data['coord']['lon'],   
                data['coord']['lat'],   
                record['main']['aqi'],
                record['components']['co'],
                record['components']['no'],
                record['components']['no2'],
                record['components']['o3'],
                record['components']['so2'],
                record['components']['pm2_5'],
                record['components']['pm10'],
                record['components']['nh3'],
                record['dt']
            ))

        cursor.executemany("""
            INSERT INTO dev.raw_air_quality_data (
                city, lon, lat, aqi, co, no, no2, o3, so2,
                pm2_5, pm10, nh3, time, inserted_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TO_TIMESTAMP(%s), NOW())
            ON CONFLICT (city, time) DO NOTHING;
        """, records_to_insert)

        conn.commit()
        print(f"{len(records_to_insert)} records inserted successfully.")

    except psycopg2.Error as e:
        print(f"Failed to insert data: {e}")
        conn.rollback()
        raise

def main():
    print("Starting pipeline")
    from fetch_data import fetch_data
    try:
        data = fetch_data()
        conn = connect_to_db()
        create_table(conn)
        print("Create table")
        insert_data(conn, data)
        print("Insert data into tabel")
    except Exception as e:
        print(f"An error occured during execution: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed")

# data = mock_fetch_data()
# conn = connect_to_db()  
# create_table(conn)
# insert_data(conn, data)