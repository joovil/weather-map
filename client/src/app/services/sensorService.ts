import { SensorServiceParams } from "@/types";
import { apiFetch } from "@/utils/apiFetch";

// TODO: Implement date params, add error handling
export const getSensorService = async ({
  id = "",
  location,
  type = "",
  note = "",
  attached = "",
  // install_date_from = "",
  // install_date_to = "",
  fields = [""],
}: SensorServiceParams) => {
  const params = new URLSearchParams({
    id,
    location: location ? location.toString() : "",
    type,
    note,
    attached,
    // install_date_from,
    // install_date_to,
  });
  fields.forEach((f) => params.append("fields", f));

  const res = await apiFetch("/sensors?" + params.toString());
  const data = await res.json();
  console.log(data);

  return data;
};
