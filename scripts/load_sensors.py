import psycopg2
import os
import json
from dotenv import load_dotenv

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env.local"))

load_dotenv(ENV_PATH)


FOLDER_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "sensors")
)


TABLE = "weather.sensors"

DB_NAME = os.getenv("DB_NAME", "weatherdb")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "pass")


def insert_sensor(cursor, id, lon, lat, type, note, attached, install_date):
    insert_query = f"""
        INSERT INTO {TABLE}
        VALUES (%s, POINT(%s, %s), %s, %s, %s, %s )
    """
    cursor.execute(
        insert_query,
        (id, lon, lat, type, note, attached, install_date),
    )


def load_sensors():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
        )
        with conn:
            with conn.cursor() as cursor:
                for filename in os.listdir(FOLDER_PATH):
                    FILE_PATH = os.path.join(FOLDER_PATH, filename)
                    try:
                        with open(FILE_PATH, encoding="utf-8") as geojson_file:
                            data = json.load(geojson_file)
                            coords = data["geometry"]["coordinates"]

                            insert_sensor(
                                cursor,
                                data["id"],
                                coords[0],
                                coords[1],
                                data["properties"]["Tyyppi"],
                                data["properties"]["Huomiot"],
                                data["properties"]["Kiinnitystapa"],
                                data["properties"]["Asennettu_pvm"],
                            )

                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"Error processing file {filename}: {e}")
                print("Sensors loaded successfully")
    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")


if __name__ == "__main__":
    load_sensors()
