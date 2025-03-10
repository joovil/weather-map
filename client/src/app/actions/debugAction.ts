"use server";

import { apiFetch } from "../../utils/apiFetch";

export const testPostAction = async (startDate: Date, endDate: Date) => {
  console.log(startDate, endDate);
  const body = JSON.stringify({
    startDate,
    endDate,
  });

  console.log(body);

  const res = await apiFetch("/debug", {
    method: "POST",
    body,
    headers: {
      "Content-Type": "application/json",
    },
  });

  const data = await res.json();
  console.log(data);
};

export const testGetAction = async () => {
  const res = await apiFetch("/sensors");
  const data = await res.json();
  console.log(data);
};
