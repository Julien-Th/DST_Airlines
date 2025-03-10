import requests
import json
import time

# Token d'accès obtenu précédemment
API_KEY = 'wa6t9sd254b7cny79ta9ssb8'

url = "https://api.lufthansa.com/v1/mds-references/countries"

# En-têtes de la requête, incluant l'authentification
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json'
}


countries = [] # initialisation de la liste countries
recordLimit = 100 # nombre de résultats rendus par requête (max=100)
recordOffset = 0 # initialisation du nombre de résultats skipped lors de la reqûete
totalRequests=1

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
        countries.extend(data["CountryResource"]['Countries']['Country'])  # Ajouter les pays à la liste
        
        if len(data["CountryResource"]['Countries']['Country']) < 100:
            print("Tous les pays ont été récupérés")
            break  # Si moins de 100 pays sont retournés, on a récupéré tous les pays
            recordOffset = recordOffset + 100  # Passer aux 100 résultats suivants

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
        
        
        
with open("/home/ubuntu/DST_Airlines/data/lufthansa/countries.json", "w", encoding="utf-8") as json_file:
    json.dump(countries, json_file, indent=4, ensure_ascii=False)
print(f"Nombre total de pays récupérés : {len(countries)}")
print("Les countries ont été enregistrés dans 'countries.json'.")
    
