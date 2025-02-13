import requests

# URL pour obtenir le token
token_url = "https://api.lufthansa.com/v1/oauth/token"

# Tes identifiants
client_id = 'g77yk92xt8yraa6rhmxs8tjsa'
client_secret = 'zPm6Jg6TjF'

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
else:
    print("Erreur :", response.status_code, response.text)

