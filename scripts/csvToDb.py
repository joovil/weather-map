import os
import psycopg2
import csv
from io import StringIO
from dotenv import load_dotenv

# Load environment variables from .env file
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env.local"))
load_dotenv(ENV_PATH)

# Database connection parameters
DB_NAME = os.getenv("DB_NAME", "weatherdb")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASS", "pass")
TABLE_NAME = "weather.sensordata"  # Change this to your table name

CSV_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "makelankatu-2024.csv")
)  # Change this to your CSV file path

# Establish connection to the database
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
cursor = conn.cursor()

# Create a temporary table
cursor.execute(
    """
    CREATE TEMP TABLE temp_sensordata (
        id SERIAL PRIMARY KEY,
        time TIMESTAMP,
        humidity FLOAT,
        temperature FLOAT,
        sensor TEXT
    )
"""
)

# Read CSV and insert data into the temporary table
with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Read the first row as headers

    headers = [
        (
            "time"
            if col == "time"
            else (
                "humidity"
                if col == "humidity"
                else (
                    "temperature"
                    if col == "temperature"
                    else "sensor" if col == "dev-id" else col
                )
            )
        )
        for col in headers
    ]

    output = StringIO()
    csv_writer = csv.writer(output)

    for row in reader:
        csv_writer.writerow(row)

    output.seek(0)
    cursor.copy_expert(
        f"COPY temp_sensordata ({', '.join(headers)}) FROM STDIN WITH CSV", output
    )

# Insert data from the temporary table into the main table, avoiding duplicates
cursor.execute(
    f"""
    INSERT INTO {TABLE_NAME} (time, humidity, temperature, sensor)
    SELECT time, humidity, temperature, sensor
    FROM temp_sensordata
    ON CONFLICT (sensor, time) DO NOTHING
"""
)

# Commit and close connection
conn.commit()
cursor.close()
conn.close()

print("CSV data inserted successfully!")
