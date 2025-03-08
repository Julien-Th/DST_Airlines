import requests
import json

# Token d'accès obtenu précédemment
API_KEY = '6mqewaqv4xb2gcn3u4xhb6hp'

# URL de l'API "Countries"
url = "https://api.lufthansa.com/v1/mds-references/cities"

# En-têtes de la requête, incluant l'authentification
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json'
}

# Envoi de la requête GET
response = requests.get(url, headers=headers)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Analyse de la réponse JSON
    cities_data = response.json()
    # Écrire dans un fichier JSON
    with open("/home/ubuntu/DST_Airlines/data/lufthansa/cities.json", "w", encoding="utf-8") as json_file:
        json.dump(cities_data, json_file, indent=4, ensure_ascii=False)
    print("Les cities ont été enregistrées dans 'cities.json'.")
else:
    # Si la requête échoue, afficher le code d'erreur
    print(f"Erreur {response.status_code}: {response.text}")
