import csv
import datetime
import os

from astral import LocationInfo
from astral.sun import sun

city = LocationInfo(
    "Helsinki", "Finland", "Europe/Helsinki", 60.19628790558516, 24.953944343215543
)
print(
    (
        f"Information for {city.name}/{city.region}\n"
        f"Timezone: {city.timezone}\n"
        f"Latitude: {city.latitude:.02f}; Longitude: {city.longitude:.02f}\n"
    )
)

year = 2025
data = []

for m in range(1, 13):
    for d in range(1, 32):
        try:
            s = sun(
                city.observer, date=datetime.date(year, m, d), tzinfo="Europe/Helsinki"
            )
            data.append(
                {
                    # Set timezone to 0000 to be same as in makelankatu csv
                    "sunrise": s["sunrise"].strftime("%Y-%m-%dT%H:%M:%S.%f+0000"),
                    "sunset": s["sunset"].strftime("%Y-%m-%dT%H:%M:%S.%f+0000"),
                }
            )
        except Exception as e:
            print(f"{d}/{m}")
            print(e)


# line = data[0]["sunrise"]
# print(line.)
# print(replace(" ", "T"))
filepath = os.path.join(os.path.dirname(__file__), "..", "..", "data", "daylight25.csv")

with open(filepath, "w", newline="") as csvfile:
    fieldNames = ["sunrise", "sunset"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
    writer.writeheader()
    writer.writerows(data)
