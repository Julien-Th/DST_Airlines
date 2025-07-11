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
url = "https://api.lufthansa.com/v1/mds-references/aircraft"

# En-têtes de la requête, incluant l'authentification
headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

aircrafts = [] # initialisation de la liste aircrafts
recordLimit = 100 # nombre de résultats rendus par requête (max=100)
recordOffset = 0 # initialisation du nombre de résultats skipped lors de la reqûete
totalRequests=1

while True:
    params = {
        'limit': recordLimit,
        'offset': recordOffset
    }
    print(totalRequests)
    response = requests.get(url, headers=headers, params=params)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        print("Code 200")
        data = response.json()
        aircrafts.extend(data["AircraftResource"]['AircraftSummaries']['AircraftSummary'])  # Ajouter les compagnies aériennes à la liste
        
        if len(data["AircraftResource"]['AircraftSummaries']['AircraftSummary']) < 100:
            print("Tous les aircrafts ont été récupérés")
            break  # Si moins de 100 aircrafts sont retournés, on a récupéré tous les aircrafts
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
    
    # Si problème au niveau de la requête
    elif response.status_code == 404:
        print("Code 404")
        totalRequests += 1  # Incrémenter le nombre de requêtes
        recordOffset += 1

    else:
        print(f"Erreur {response.status_code}: {response.text}")
        break
        
        
        
with open("/home/ubuntu/DST_Airlines/data/lufthansa/aircrafts.json", "w", encoding="utf-8") as json_file:
    json.dump(aircrafts, json_file, indent=4, ensure_ascii=False)
print(f"Nombre total de aircrafts récupérés : {len(aircrafts)}")
print("Les aircrafts ont été enregistrés dans 'aircrafts.json'.")
    
