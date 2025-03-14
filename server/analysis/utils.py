import pandas as pd
import requests

SENSORS = [
    "24E124136E106616",
    "24E124136E106617",
    "24E124136E106618",
    "24E124136E106619",
    "24E124136E106635",
    "24E124136E106636",
    "24E124136E106637",
    "24E124136E106638",
    "24E124136E106643",
    "24E124136E106661",
    "24E124136E106674",
    "24E124136E106686",
]

SENSOR_SUN = [
    "24E124136E106637",
    "24E124136E106638",
    "24E124136E106619",
    "24E124136E106661",
]

SENSOR_SHADE = [
    "24E124136E106616",
    "24E124136E106617",
    "24E124136E106618",
    "24E124136E106635",
    "24E124136E106636",
    "24E124136E106643",
    "24E124136E106674",
    "24E124136E106686",
]

BASE_URL = "https://bri3.fvh.io/opendata/makelankatu/"

def get_csv(year=None):
    """Load sensor data for a specific year or all available years."""
    available_years = [2024, 2025]  # Update this when new data is available

    if year is None:
        dfs = [fetch_csv(y) for y in available_years]
        df = pd.concat(dfs, ignore_index=True)
    elif year in available_years:
        df = fetch_csv(year)
    else:
        raise ValueError(f"Invalid year. Choose from {available_years} or None for all years.")

    print("CSV loading complete.")
    return df


def fetch_csv(year):
    """Fetch and load a CSV file for a given year."""
    filename = f"makelankatu-{year}.csv.gz"
    url = BASE_URL + filename

    print(f"Fetching CSV data for {year} from {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    return pd.read_csv(url, parse_dates=["time"])


def separate_sensors(sensor_df):
    filtered = {
        sensor_id: group
        for sensor_id, group in sensor_df.groupby("dev-id")
        if sensor_id in SENSORS
    }
    return filtered


def apply_date_range(df, start_date, end_date):
    mask = (df["time"] >= start_date) & (df["time"] <= end_date)
    return df.loc[mask]


def filter_data_by_sunlight(daytime=True):
    daylight_info = pd.read_csv("../data/daylight.csv", parse_dates=["sunrise", "sunset"])
    sensor_readings = get_csv()

    sensor_readings["date"] = sensor_readings["time"].dt.date
    daylight_info["date"] = daylight_info["sunrise"].dt.date

    combined_data = pd.merge(sensor_readings, daylight_info, on="date")

    if daytime:
        mask = (combined_data["time"] >= combined_data["sunrise"]) & (combined_data["time"] <= combined_data["sunset"])
    else:
        mask = (combined_data["time"] < combined_data["sunrise"]) | (combined_data["time"] > combined_data["sunset"])

    return combined_data[mask].drop(columns=["sunrise", "sunset"])


def get_day_data():
    return filter_data_by_sunlight(daytime=True)


def get_night_data():
    return filter_data_by_sunlight(daytime=False)


def get_cloudiness_data(file_path="../data/cloudiness.csv"):
    cloud_df = pd.read_csv(file_path, encoding="utf-8", sep=",")
    cloud_df.columns = ["Havaintoasema", "Vuosi", "Kuukausi", "Päivä", "Aika", "Pilvisyys"]

    cloud_df = cloud_df.rename(columns={"Vuosi": "year", "Kuukausi": "month", "Päivä": "day"})
    cloud_df["date"] = pd.to_datetime(cloud_df[["year", "month", "day"]]).dt.date
    cloud_df["Pilvisyys"] = cloud_df["Pilvisyys"].str.extract(r"(\d+)").astype(float)
    cloud_df.loc[cloud_df["Pilvisyys"] == 9, "Pilvisyys"] = None

    return cloud_df.groupby("date")["Pilvisyys"].mean().reset_index()
