import requests
import os

# URL pour obtenir le token
token_url = "https://api.lufthansa.com/v1/oauth/token"

# Tes identifiants
client_id = 'g77yk92xt8yraa6rhmxs8tjsa'
client_secret = 'zPm6Jg6TjF'

# Chemin de stockage du token
token_storage_path = "/home/ubuntu/DST_Airlines/data/token/"
token_file_path = os.path.join(token_storage_path, "access_token.txt")

# Paramètres pour la requête
data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials'
}

# En-têtes de la requête
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Requête pour obtenir le token
response = requests.post(token_url, data=data, headers=headers)

# Vérification de la réponse
if response.status_code == 200:
    access_token = response.json().get('access_token')
    print("Token d'accès :", access_token)

    # Vérifie que le dossier existe, sinon le créer
    os.makedirs(token_storage_path, exist_ok=True)

    # Écriture du token dans le fichier (écrasement à chaque exécution)
    with open(token_file_path, "w") as f:
        f.write(access_token)
else:
    print("Erreur :", response.status_code, response.text)
