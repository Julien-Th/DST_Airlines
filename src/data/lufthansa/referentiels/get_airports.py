import requests
import json
import time
import os

# 🔹 Charger le token depuis un fichier
token_path = "/home/ubuntu/DST_Airlines/data/token/access_token.txt"
if not os.path.exists(token_path):
    print(f"❌ Token introuvable à : {token_path}")
    sys.exit(1)

with open(token_path, "r") as f:
    access_token = f.read().strip()

# URL de l'API "Countries"
url = "https://api.lufthansa.com/v1/mds-references/airports"

# En-têtes de la requête, incluant l'authentification
headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

airports = [] # initialisation de la liste airport
recordLimit = 100 # nombre de résultats rendus par requête (max=100)
recordOffset = 0 # initialisation du nombre de résultats skipped lors de la reqûete
totalRequests=1

while True:
    params = {
        'limit': recordLimit,
        'offset': recordOffset,
        'LHoperated': 0
    }
    print(totalRequests)
    response = requests.get(url, headers=headers, params=params)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        print("Code 200")
        data = response.json()
        airports.extend(data["AirportResource"]['Airports']['Airport'])  # Ajouter les aéroports à la liste
        
        if len(data["AirportResource"]['Airports']['Airport']) < 100:
            print("Tous les aéroports ont été récupérés")
            break  # Si moins de 100 aéroports sont retournés, on a récupéré tous les aéroports
            recordOffset = recordOffset + 100  # Passer aux 100 résultats suivants

        totalRequests += 1  # Incrémenter le nombre de requêtes
        recordOffset += 100
            
    # Respecter la limite de 6 requêtes par seconde (1 requête toutes les 1 seconde maximum)
    elif response.status_code == 403 :
        print("Limite seconde atteinte, en pause pendant 1 seconde...")
        time.sleep(1)  # Attendre 1 seconde après 6 requêtes

    # Respecter la limite de 1000 requêtes par heure
    elif totalRequests >= 1000:
        print("Limite horaire atteinte, en pause pendant 1 heure...")
        time.sleep(3600)  # Attendre 1 heure (3600 secondes)
        totalRequests = 0  # Réinitialiser le compteur de requêtes après la pause d'une heure

    elif response.status_code == 404:
        print("Code 404")
        totalRequests += 1  # Incrémenter le nombre de requêtes
        recordOffset += 1

    else:
        print(f"Erreur {response.status_code}: {response.text}")
        print("\n")
        print(response.text)
        break
        
        
        
with open("/home/ubuntu/DST_Airlines/data/lufthansa/airports.json", "w", encoding="utf-8") as json_file:
    json.dump(airports, json_file, indent=4, ensure_ascii=False)
print(f"Nombre total d'aéroports récupérés : {len(airports)}")
print("Les aéroports ont été enregistrés dans 'airports.json'.")
    
