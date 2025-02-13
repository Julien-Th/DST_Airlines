import requests

# Token d'accès obtenu précédemment
access_token = '9du3hqtm89h4ctkk2b6hkvm9'

# Paramètres de la requête
origin = 'FRA'  # Code IATA de l'aéroport d'origine
destination = 'JFK'  # Code IATA de l'aéroport de destination
from_date = '2025-02-12'  # Date de départ au format AAAA-MM-JJ

# URL de l'API pour les horaires des vols
api_url = f"https://api.lufthansa.com/v1/operations/schedules/{origin}/{destination}/{from_date}"

# En-têtes de la requête
headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

# Requête pour obtenir les horaires des vols
response = requests.get(api_url, headers=headers)

# Vérification de la réponse
if response.status_code == 200:
    flight_schedules = response.json()
    print(flight_schedules)
else:
    print("Erreur :", response.status_code, response.text)
