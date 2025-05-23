import pandas as pd
import requests
import gzip
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup


BASE_URL_VALLILA = "https://bri3.fvh.io/opendata/makelankatu/"
BASE_URL_LAAJASALO_KOIVUKYLA = "https://bri3.fvh.io/opendata/r4c/"


def fetch_csv(url):
    """
    Downloads and parses a compressed CSV (.csv.gz) file from the given URL into a pandas DataFrame.
    """
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        print(f"[INFO] CSV downloaded: {url}")
        return pd.read_csv(gzip.open(BytesIO(response.content), 'rt'), parse_dates=["time"])
    except Exception as e:
        print(f"[ERROR] Failed to download CSV: {url} | Error: {e}")
        return None


def get_sensor_metadata(locations):
    """
    Fetch specific sensor metadata based on the provided locations and pre-defined sensor IDs.
    - Vallila: A fixed set of Vallila sensor IDs.
    - Laajasalo, Koivukylä: A fixed set of sensor IDs for these districts.
    """
    print(f"[INFO] Fetching sensor metadata for locations: {locations}")
    if isinstance(locations, str):
        locations = [locations]

    # Predefined sensor IDs for each district
    vallila_sensors = [
        "24E124136E106616", "24E124136E106617", "24E124136E106618", "24E124136E106619",
        "24E124136E106635", "24E124136E106636", "24E124136E106637", "24E124136E106638",
        "24E124136E106643", "24E124136E106661", "24E124136E106674", "24E124136E106686"
    ]
    
    laajasalo_koivukylä_sensors = [
        "24E124136E140271", "24E124136E140283", "24E124136E140287", "24E124136E146069",
        "24E124136E146080", "24E124136E146083", "24E124136E146087", "24E124136E146118",
        "24E124136E146126", "24E124136E146128", "24E124136E146155", "24E124136E146157",
        "24E124136E146167", "24E124136E146186", "24E124136E146190", "24E124136E146198",
        "24E124136E146218", "24E124136E146224", "24E124136E146235", "24E124136E146237"
    ]
    
    metadata = []

    # Fetch Vallila sensors (if Vallila is in the requested locations)
    if "Vallila" in locations:
        for sensor_id in vallila_sensors:
            try:
                url = f"{BASE_URL_VALLILA}{sensor_id}.geojson"
                r = requests.get(url, timeout=10)
                r.raise_for_status()
                data = r.json()
                props = data.get("properties", {})
                coords = data.get("geometry", {}).get("coordinates", [None, None])

                metadata.append({
                    "device_id": data.get("id"),
                    "district": "Vallila",
                    "name": None,
                    "street": None,
                    "lat": coords[1],
                    "lon": coords[0],
                    "tyyppi": props.get("Tyyppi", ""),
                    "huomiot": props.get("Huomiot", ""),
                    "kiinnitystapa": props.get("Kiinnitystapa", ""),
                    "asennettu_pvm": props.get("Asennettu_pvm", ""),
                    "sensori": props.get("Sensori", ""),
                    "fid": props.get("fid", "")
                })
            except Exception as e:
                print(f"[ERROR] Failed to fetch metadata for Vallila sensor {sensor_id}: {e}")

    # Fetch Laajasalo and Koivukylä sensors (if any of them are in the requested locations)
    if any(loc in locations for loc in ["Laajasalo", "Koivukylä"]):
        for sensor_id in laajasalo_koivukylä_sensors:
            try:
                url = f"{BASE_URL_LAAJASALO_KOIVUKYLA}{sensor_id}.geojson"
                r = requests.get(url, timeout=10)
                r.raise_for_status()
                data = r.json()
                props = data.get("properties", {})
                district = props.get("district", "").strip()

                # Manually assign Koivukylä for sensor 24E124136E140283 if no district is provided
                if not district and sensor_id == "24E124136E140283":
                    district = "Koivukylä"
                    print(f"[INFO] Sensor {sensor_id} manually assigned to district: Koivukylä")

                # Only include sensors if they match the requested locations
                if district in locations:
                    coords = data.get("geometry", {}).get("coordinates", [None, None])
                    metadata.append({
                        "device_id": data.get("id"),
                        "district": district,
                        "name": props.get("name", ""),
                        "street": props.get("street", ""),
                        "lat": coords[1],
                        "lon": coords[0],
                        "date_installed": props.get("Date_installed", ""),
                        "sensor_number": props.get("Sensor_number", ""),
                        "estimated_height_m": props.get("Estimated height from the ground level (m)", ""),
                        "pole_surroundings": props.get("Pole surroundings", ""),
                        "lc_zoning": props.get("WUDAPT Local Climate Zone Classification", ""),
                        "fid": props.get("fid", ""),
                        "field_1": props.get("field_1", ""),
                        "field_2": props.get("field_2", ""),
                        "field_3": props.get("field_3", ""),
                        "field_4": props.get("field_4", "")
                    })
            except Exception as e:
                print(f"[ERROR] Failed to fetch metadata for sensor {sensor_id}: {e}")

    print(f"[INFO] Total sensor metadata rows: {len(metadata)}")
    
    # Convert to DataFrame and return
    df_meta = pd.DataFrame(metadata)
    return df_meta



def load_sensor_data(start_date, end_date, locations=None):
    """
    Loads and combines sensor measurement data and metadata for selected locations and date range.
    Returns a unified DataFrame with time series and sensor info.
    """
    if isinstance(locations, str):
        locations = [locations]

    start_year = pd.to_datetime(start_date).year
    end_year = pd.to_datetime(end_date).year
    years_needed = range(start_year, end_year + 1)

    urls = []
    added_urls = set()

    for year in years_needed:
        if not locations or "Vallila" in locations:
            url = f"{BASE_URL_VALLILA}makelankatu-{year}.csv.gz"
            if url not in added_urls:
                urls.append(url)
                added_urls.add(url)
        if not locations or any(loc in locations for loc in ["Laajasalo", "Koivukylä"]):
            url = f"{BASE_URL_LAAJASALO_KOIVUKYLA}r4c_all-{year}.csv.gz"
            if url not in added_urls:
                urls.append(url)
                added_urls.add(url)

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_csv, urls))

    df = pd.concat([r for r in results if r is not None], ignore_index=True)
    df["time"] = pd.to_datetime(df["time"], utc=True)

    if "dev-id" in df.columns:
        df.rename(columns={"dev-id": "device_id"}, inplace=True)

    start_dt = pd.to_datetime(start_date).tz_localize("UTC")
    end_dt = pd.to_datetime(end_date).tz_localize("UTC")
    df = df[(df["time"] >= start_dt) & (df["time"] <= end_dt)]

    meta = get_sensor_metadata(locations)
    known_ids = meta["device_id"].tolist()
    df = df[df["device_id"].isin(known_ids)]
    df = df.merge(meta, how="left", on="device_id")

    print(f"[INFO] Data loaded and merged: {len(df)} rows.")
    return df


def test_data_loading():
    """
    Simple test function to load data and display basic structure and statistics.
    """
    df = load_sensor_data("2024-01-01", "2025-03-27", ["Koivukylä", "Vallila"])
    print("\n[INFO] Columns:")
    print(df.columns.tolist())
    print("\n[INFO] First rows:")
    print(df.head())
    print("\n[INFO] Row count per district:")
    print(df["district"].value_counts())

if __name__ == "__main__":
    test_data_loading()
