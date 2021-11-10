import { Client, Create, Collection } from "faunadb";
import { customFetch, getFaunaError } from "./utils";

const faunaClient = new Client({
  secret: FAUNA_SECRET,
  domain: "db.us.fauna.com",
  fetch: customFetch,
});

addEventListener("scheduled", (event) => {
  event.waitUntil(handleScheduled(event));
});

async function handleScheduled() {
  try {
    const apiResponse = await fetch(
      "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
    );
    const data = await apiResponse.json();
    const result = await faunaClient.query(
      Create(Collection("Snapshots"), {
        data: {
          timestamp: Date.now(),
          last_updated: data.last_updated,
          stations: data.data.stations,
        },
      })
    );
    return new Response(result.ref.id, {
      status: 200,
    });
  } catch (error) {
    const faunaError = getFaunaError(error);
    return new Response(faunaError, {
      status: faunaError.status,
    });
  }
}
