import requests
import json
import time
import os
from itertools import product
import pandas as pd
from datetime import datetime

# Token d'accès
API_KEY = 'q9rg66448y3cn6agguc7bvdn'

# Paramètres
origins = ["CDG", "ORY", "BVA", "MRS", "LYS"]     # Aéroports de départ
destinations = ["FRA", "HHN", "MUC"]              # Aéroports d’arrivée
date = "2025-05-13"
recordLimit = 100
maxRequestsPerHour = 1000

# Fichier de sortie
output_path = "/home/ubuntu/DST_Airlines/data/lufthansa/all_flights.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# En-têtes HTTP
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json'
}

# Fonction pour récupérer les vols pour une paire (origin, destination)
def fetch_flights_for_route(origin, destination, date, headers):
    url = f"https://api.lufthansa.com/v1/operations/customerflightinformation/route/{origin}/{destination}/{date}"
    flights = []
    recordOffset = 0
    totalRequests = 0

    while True:
        params = {
            'limit': recordLimit,
            'offset': recordOffset
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            totalRequests += 1

            # Gestion de la limite horaire
            if totalRequests >= maxRequestsPerHour:
                print("Limite horaire atteinte. Pause 1 heure.")
                time.sleep(3600)
                totalRequests = 0

            if response.status_code == 200:
                data = response.json()
                flights_data = (
                    data.get("FlightInformation", {})
                        .get("Flights", {})
                        .get("Flight", [])
                )

                if not flights_data:
                    break

                flights.extend(flights_data)
                print(f"✔ {origin} → {destination} : {len(flights_data)} vols récupérés.")

                if len(flights_data) < recordLimit:
                    break

                recordOffset += recordLimit
                time.sleep(0.2)

            elif response.status_code == 403 and 'Over Queries Per Second' in response.text:
                print("Trop de requêtes/secondes. Pause 1s.")
                time.sleep(1)
            else:
                print(f"❌ Erreur {origin}->{destination}: {response.status_code} - {response.text}")
                break

        except requests.RequestException as e:
            print(f"❌ Erreur réseau {origin}->{destination}: {e}")
            break

    return flights

# Récupération pour toutes les paires
all_flights = []

print("📦 Téléchargement des vols aller...")
for origin, destination in product(origins, destinations):
    if origin == destination:
        continue
    flights = fetch_flights_for_route(origin, destination, date, headers)
    all_flights.extend(flights)

print("📦 Téléchargement des vols retour...")
for origin, destination in product(destinations, origins):
    if origin == destination:
        continue
    flights = fetch_flights_for_route(origin, destination, date, headers)
    all_flights.extend(flights)

# Sauvegarde JSON
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_flights, f, indent=4, ensure_ascii=False)

print(f"✅ Total {len(all_flights)} vols enregistrés dans {output_path}")

# ===== Post-traitement : création DataFrame + calcul des retards =====

def compute_delay_minutes(scheduled_date, scheduled_time, actual_date, actual_time):
    try:
        scheduled_dt = datetime.strptime(f"{scheduled_date} {scheduled_time}", "%Y-%m-%d %H:%M")
        actual_dt = datetime.strptime(f"{actual_date} {actual_time}", "%Y-%m-%d %H:%M")
        delay = (actual_dt - scheduled_dt).total_seconds() / 60
        return int(delay)
    except Exception:
        return None

records = []

for flight in all_flights:
    try:
        dep = flight.get("Departure", {})
        arr = flight.get("Arrival", {})
        op_carrier = flight.get("OperatingCarrier", {})
        equipment = flight.get("Equipment", {})
        status = flight.get("Status", {})

        dep_sched_date = dep.get("Scheduled", {}).get("Date")
        dep_sched_time = dep.get("Scheduled", {}).get("Time")
        dep_act_date = dep.get("Actual", {}).get("Date")
        dep_act_time = dep.get("Actual", {}).get("Time")

        arr_sched_date = arr.get("Scheduled", {}).get("Date")
        arr_sched_time = arr.get("Scheduled", {}).get("Time")
        arr_act_date = arr.get("Actual", {}).get("Date")
        arr_act_time = arr.get("Actual", {}).get("Time")

        record = {
            "DepartureAirport": dep.get("AirportCode"),
            "DepartureScheduledDate": dep_sched_date,
            "DepartureScheduledTime": dep_sched_time,
            "DepartureActualDate": dep_act_date,
            "DepartureActualTime": dep_act_time,

            "ArrivalAirport": arr.get("AirportCode"),
            "ArrivalScheduledDate": arr_sched_date,
            "ArrivalScheduledTime": arr_sched_time,
            "ArrivalActualDate": arr_act_date,
            "ArrivalActualTime": arr_act_time,

            "AirlineID": op_carrier.get("AirlineID"),
            "FlightNumber": op_carrier.get("FlightNumber"),

            "AircraftCode": equipment.get("AircraftCode"),

            "FlightStatusCode": status.get("Code"),
            "FlightStatusDescription": status.get("Description"),

            "DepartureDelayMinutes": compute_delay_minutes(dep_sched_date, dep_sched_time, dep_act_date, dep_act_time),
            "ArrivalDelayMinutes": compute_delay_minutes(arr_sched_date, arr_sched_time, arr_act_date, arr_act_time),
        }

        records.append(record)

    except Exception as e:
        print(f"⚠ Erreur lors du traitement d’un vol : {e}")

# Convertir en DataFrame
df = pd.DataFrame(records)

# Export CSV
csv_output_path = output_path.replace(".json", ".csv")
df.to_csv(csv_output_path, index=False, encoding="utf-8")

print(f"✅ CSV exporté vers : {csv_output_path}")
