import requests
import json
import time
import os
import sys
from itertools import product
import pandas as pd
from datetime import datetime

# 🔹 Récupérer la date passée en argument
if len(sys.argv) < 2:
    print("❌ Erreur : veuillez fournir une date (ex: 2025-06-25) en argument.")
    sys.exit(1)

date = sys.argv[1]  # Exemple : 2025-06-25

# 🔹 Charger le token depuis un fichier
token_storage_path = sys.argv[2]
# token_storage_path = "/home/ubuntu/DST_Airlines/data/token/"
token_file_path = os.path.join(token_storage_path, "access_token.txt")
if not os.path.exists(token_file_path):
    print(f"❌ Token introuvable à : {token_file_path}")
    sys.exit(1)

with open(token_file_path, "r") as f:
    access_token = f.read().strip()

# 🔹 Paramètres
origins = ["CDG", "ORY", "NCE", "MRS", "LYS","MAD","BCN","AGP","FCO","MXP","VCE","NAP","LHR","LGW","MAN","STN","LTN","BHX","FRA","HNN","MUC"]
destinations = ["CDG", "ORY", "NCE", "MRS", "LYS","MAD","BCN","AGP","FCO","MXP","VCE","NAP","LHR","LGW","MAN","STN","LTN","BHX","FRA","HNN","MUC"]
recordLimit = 100
maxRequestsPerHour = 1000

# 🔹 Fichier de sortie
output_path = sys.argv[3]
output_file = os.path.join(output_path, f"flights_{date}.json")
# output_file = f"/home/ubuntu/DST_Airlines/data/lufthansa/all_flights_{date}.json"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# 🔹 En-têtes HTTP
headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

# 🔹 Fonction pour récupérer les vols
def fetch_flights_for_route(origin, destination, date, headers):
    url = f"https://api.lufthansa.com/v1/operations/customerflightinformation/route/{origin}/{destination}/{date}"
    flights = []
    recordOffset = 0
    totalRequests = 0

    while True:
        params = {'limit': recordLimit, 'offset': recordOffset}

        try:
            response = requests.get(url, headers=headers, params=params)
            totalRequests += 1

            if totalRequests >= maxRequestsPerHour:
                print("⏳ Limite horaire atteinte. Pause 1 heure.")
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
                print("⏱ Trop de requêtes/seconde. Pause 1s.")
                time.sleep(1)
            else:
                print(f"❌ Erreur {origin}->{destination}: {response.status_code} - {response.text}")
                break

        except requests.RequestException as e:
            print(f"❌ Erreur réseau {origin}->{destination}: {e}")
            break

    return flights

# 🔹 Récupération vols aller/retour
all_flights = []

print("📦 Téléchargement des vols aller...")
for origin, destination in product(origins, destinations):
    if origin != destination:
        all_flights.extend(fetch_flights_for_route(origin, destination, date, headers))

print("📦 Téléchargement des vols retour...")
for origin, destination in product(destinations, origins):
    if origin != destination:
        all_flights.extend(fetch_flights_for_route(origin, destination, date, headers))

# 🔹 Sauvegarde JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_flights, f, indent=4, ensure_ascii=False)

print(f"✅ Total {len(all_flights)} vols enregistrés dans {output_file}")

# 🔹 Post-traitement : DataFrame + retard
def compute_delay_minutes(scheduled_date, scheduled_time, actual_date, actual_time):
    try:
        scheduled_dt = datetime.strptime(f"{scheduled_date} {scheduled_time}", "%Y-%m-%d %H:%M")
        actual_dt = datetime.strptime(f"{actual_date} {actual_time}", "%Y-%m-%d %H:%M")
        return int((actual_dt - scheduled_dt).total_seconds() / 60)
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

        record = {
            "DepartureAirport": dep.get("AirportCode"),
            "DepartureScheduledDate": dep.get("Scheduled", {}).get("Date"),
            "DepartureScheduledTime": dep.get("Scheduled", {}).get("Time"),
            "DepartureActualDate": dep.get("Actual", {}).get("Date"),
            "DepartureActualTime": dep.get("Actual", {}).get("Time"),

            "ArrivalAirport": arr.get("AirportCode"),
            "ArrivalScheduledDate": arr.get("Scheduled", {}).get("Date"),
            "ArrivalScheduledTime": arr.get("Scheduled", {}).get("Time"),
            "ArrivalActualDate": arr.get("Actual", {}).get("Date"),
            "ArrivalActualTime": arr.get("Actual", {}).get("Time"),

            "AirlineID": op_carrier.get("AirlineID"),
            "FlightNumber": op_carrier.get("FlightNumber"),
            "AircraftCode": equipment.get("AircraftCode"),

            "FlightStatusCode": status.get("Code"),
            "FlightStatusDescription": status.get("Description"),

            "DepartureDelayMinutes": compute_delay_minutes(
                dep.get("Scheduled", {}).get("Date"),
                dep.get("Scheduled", {}).get("Time"),
                dep.get("Actual", {}).get("Date"),
                dep.get("Actual", {}).get("Time"),
            ),
            "ArrivalDelayMinutes": compute_delay_minutes(
                arr.get("Scheduled", {}).get("Date"),
                arr.get("Scheduled", {}).get("Time"),
                arr.get("Actual", {}).get("Date"),
                arr.get("Actual", {}).get("Time"),
            ),
        }

        records.append(record)

    except Exception as e:
        print(f"⚠ Erreur lors du traitement d’un vol : {e}")

# 🔹 Export CSV
df = pd.DataFrame(records)
csv_output_path = output_file.replace(".json", ".csv")
df.to_csv(csv_output_path, index=False, encoding="utf-8")
print(f"✅ CSV exporté vers : {csv_output_path}")
