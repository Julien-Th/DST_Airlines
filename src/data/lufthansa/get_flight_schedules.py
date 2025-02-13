import json
import requests

# Token d'accès obtenu précédemment
access_token = '9du3hqtm89h4ctkk2b6hkvm9'

# Paramètres de la requête
origin = 'FRA'  # Code IATA de l'aéroport d'origine (ex: Francfort)
destination = 'JFK'  # Code IATA de l'aéroport de destination (ex: New York JFK)
from_date = '2025-02-14'  # Date de départ (YYYY-MM-DD)

# URL de l'API Lufthansa pour récupérer les horaires des vols
api_url = f"https://api.lufthansa.com/v1/operations/schedules/{origin}/{destination}/{from_date}"

# En-têtes de la requête
headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

# Requête API
response = requests.get(api_url, headers=headers)

# Vérification de la réponse
if response.status_code == 200:
    flight_schedules = response.json()  # Convertir la réponse en JSON

    # Écrire dans un fichier JSON
    with open("/home/ubuntu/DST_Airlines/data/lufthansa/horaires_vols.json", "w", encoding="utf-8") as json_file:
        json.dump(flight_schedules, json_file, indent=4, ensure_ascii=False)

    print("Les horaires des vols ont été enregistrés dans 'horaires_vols.json'.")
else:
    print("Erreur :", response.status_code, response.text)
