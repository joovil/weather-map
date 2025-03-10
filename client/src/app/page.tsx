import SearchButton from "@/components/SearchButton";
import MapWrapper from "@/components/MapWrapper";
import SensorCard from "@/components/SensorCard";
import { Sensor } from "@/types";
import { apiFetch } from "@/utils/apiFetch";

export type LatestData = {
  id: string;
  properties: {
    measurement: {
      humidity: number;
      temperature: number;
      time: string;
    };
  };
};

export default async function Home() {
  const res = await apiFetch("/sensors");

  const sensors: Sensor[] = await res.json();
  // Sort sensors to have sensors in the sun to be displayed first
  const sortedSensors = sensors.sort((a) => {
    if (a.type === "Auringossa") {
      return -1;
    }
    if (a.type === "Varjossa") {
      return 1;
    }
    return 0;
  });

  // Get latest data
  let latestData: LatestData[] = [];
  const resLatest = await fetch(
    "https://bri3.fvh.io/opendata/makelankatu/makelankatu_latest.geojson",
  );

  if (resLatest.status === 200) {
    const data = await resLatest.json();
    latestData = data.features;
  }

  return (
    <main className="flex flex-col gap-6">
      <div className="2xl:flex 2xl:gap-12">
        <h1 className="mb-2 text-5xl 2xl:pt-9">Mäkelänkatu</h1>
        <div className="2xl:w-fill aspect-[2/3] w-full border-2 sm:aspect-[2/1] 2xl:aspect-[2/1]">
          <MapWrapper />
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
        {sortedSensors.map((sensor) => (
          <SensorCard
            key={sensor.id}
            sensor={sensor}
            latestData={
              latestData && latestData.filter((d) => d.id === sensor.id)[0]
            }
          />
        ))}
      </div>

      <div className="flex justify-center">
        <SearchButton /> 
      </div>
    </main>
  );
}
