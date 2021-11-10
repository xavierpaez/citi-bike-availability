from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import requests
import datetime
import pytz
import csv
import pickle

client = FaunaClient(
  secret="FAUNA_KEY",
  domain="db.us.fauna.com",
  # NOTE: Use the correct domain for your database's Region Group.
  port=443,
  scheme="https"
)
stations = []
try:
  result = client.query(q.paginate(
    q.documents(q.collection("Snapshots")), size=60000)
  )['data']

except e.NotFound as err:
  print("error")
 
counter = 0
for ref in result:
  collection = client.query(q.get(ref))
  id = client.query(q.select("id", ref))
  counter += 1
  print(counter)
  for station in collection['data']['stations']:
    station["id"] = id
    stations.append(station)

selected_stations = [
  '478',
  '4238',
  '508',
  '72',
  '4236',
  '530',
  '422',
  '513',
  '480',
  '4235',
  '495',
  '513',
  '3236',
  '479',
  '3699',
  '423',
  '457',
  '468',
  '469',
  '4269',
  '4651',
  '2021',
  '529',
  '477',
  '3724',
  '2006',
  '3809',
  '3443',
  '510',
  '3731',
  '4232',
  '3785',
  '465',
  '281',
  '4073',
  '3233',
  '484',
  '3132',
  '3457',
  '3814',
  '456',
  '4058',
  '4239',
  '4675',
  '153',
  '305',
  '464',
  '367',
  '522',
  '228',
  '4240',
  '3734',
  '3815',
  '228',
  '3243',
  '4279',
  '3815',
  '454',
  '164',
  '516',
  '3462',
  '455'
]

with open('stations.pickle', 'wb') as handle:
    pickle.dump(stations, handle, protocol=pickle.HIGHEST_PROTOCOL)

#Getting information about CitiBike Stations and saving it in a map.
station_information = {}
try: 
  response = requests.get("https://gbfs.citibikenyc.com/gbfs/en/station_information.json")
except requests.exceptions.HTTPError as error:
    print(error)

for station in response.json()['data']['stations']:
    station_information[station['station_id']] = station

selected_stations_to_export = []
stations_to_export = []
try:
  for station in stations:
      if (station_information.get(station['station_id'])):
        station.update(station_information[station['station_id']])
        station['last_reported_datetime'] = datetime.datetime.fromtimestamp(station['last_reported'], pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
        stations_to_export.append(station)
        if station['station_id'] in selected_stations:
          selected_stations_to_export.append(station)
except KeyError:
  print('Can not find "something"')

with open('selectedStations-2.pickle', 'wb') as handle:
    pickle.dump(selected_stations_to_export, handle, protocol=pickle.HIGHEST_PROTOCOL)

header = ["station_id", "name", "lon","lat","region_id","name","capacity","station_type", "is_renting","is_returning","num_bikes_disabled","station_status","num_bikes_available","num_docks_disabled","num_docks_available","num_ebikes_available","last_reported", "last_reported_datetime"]
with open('finalData-selected-new.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = header, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(selected_stations_to_export)
