export type Sensor = {
  id: string;
  location: [number, number];
  type: "Auringossa" | "Varjossa" | undefined;
  note: string | null;
  attached: string;
  installDate: Date;
};

export type SensorData = {
  id: number;
  time: Date;
  humidity: number;
  temperature: number;
  sensor: string;
};

export interface SensorServiceParams {
  id?: string;
  location?: [number, number];
  type?: string;
  note?: string;
  attached?: string;
  install_date_from?: string;
  install_date_to?: string;
  fields?: string[];
}
