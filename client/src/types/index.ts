export type Sensor = {
  id: string;
  lat: number;
  lon: number;
  location: "Vallila" | "Koivukyla" | "Laajasalo";
  install_date: Date;
  csv_link: string;
};

export type SensorData = {
  id: number;
  time: Date;
  humidity: number;
  temperature: number;
  sensor: string;
};

export interface SensorParams {
  id?: string;
  location?: [number, number];
  type?: string;
  note?: string;
  attached?: string;
  install_date_from?: string;
  install_date_to?: string;
  fields?: string[];
}

export type SensorFilter = {
  dateRange?: [string, string];
  attachedTo?: string;
  type?: string;
  note?: string;
};

export interface SensorDataParams {
  sensor_id?: string;
  start_date?: string;
  end_date?: string;
  humidity_from?: number;
  humidity_to?: number;
  temperature_from?: number;
  temperature_to?: number;
}
