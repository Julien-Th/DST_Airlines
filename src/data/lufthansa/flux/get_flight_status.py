import requests
import json
import time
import os
import sys

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

# Parameters
origin = "FRA"
destination = "CDG"
# date = "2025-05-05"
recordLimit = 100 # nombre de résultats rendus par requête (max=100)
recordOffset = 0 # initialisation du nombre de résultats skipped lors de la reqûete
totalRequests=1

# 🔹 Fichier de sortie
output_path = sys.argv[3]
output_file = os.path.join(output_path, f"flights_{date}.json")
# output_file = f"/home/ubuntu/DST_Airlines/data/lufthansa/flights_{date}.json"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# URL de l'API "Customer Flight Information by Route"
url = f"https://api.lufthansa.com/v1/operations/customerflightinformation/route/{origin}/{destination}/{date}"

# En-têtes de la requête, incluant l'authentification
headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

flights = [] # initialisation de la liste des vols


while True:
    params = {
        'limit': recordLimit,
        'offset': recordOffset
    }
    
    response = requests.get(url, headers=headers, params=params)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        print(totalRequests)
        data = response.json()
        flights.extend(data["FlightInformation"]['Flights']['Flight'])  # Ajouter les vols à la liste
        
        if len(data["FlightInformation"]['Flights']['Flight']) < 100:
            print("Tous les vols ont été récupérés")
            break  # Si moins de 100 vols sont retournés, on a récupéré tous les vols
        

        totalRequests += 1  # Incrémenter le nombre de requêtes
        recordOffset += 100
            
    # Respecter la limite de 6 requêtes par seconde (1 requête toutes les 1 seconde maximum)
    elif response.status_code == 403 and response.text == '{ "Error": "Account Over Queries Per Second Limit" }':
        print("Limite seconde atteinte, en pause pendant 1 seconde...")
        time.sleep(1)  # Attendre 1 seconde après 6 requêtes

    # Respecter la limite de 1000 requêtes par heure
    elif totalRequests >= 1000:
        print("Limite horaire atteinte, en pause pendant 1 heure...")
        time.sleep(3600)  # Attendre 1 heure (3600 secondes)
        totalRequests = 0  # Réinitialiser le compteur de requêtes après la pause d'une heure
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        break
        
        
        
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(flights, json_file, indent=4, ensure_ascii=False)
print(f"Nombre total de vols récupérés : {len(flights)}")
print("Les vols ont été enregistrés dans 'flights.json'.")
    
