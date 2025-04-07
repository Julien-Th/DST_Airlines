import json
import csv
from collections import Counter

input_file = "/home/ubuntu/DST_Airlines/data/lufthansa/airports.json"
output_file = "/home/ubuntu/DST_Airlines/data/lufthansa/airports.csv"

# Charger les données JSON (remplace par le chemin de ton fichier si besoin)
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Préparer les en-têtes du CSV
headers = [
    'AirportCode',
    'CityCode',
    'CountryCode',
    'Latitude',
    'Longitude',
    'UtcOffset',
    'TimeZoneId'
]

# Trouver toutes les langues présentes pour les noms
languages = set()
for airport in data:
    names = airport.get("Names", {}).get("Name", [])
    if isinstance(names, dict):  # cas où il n'y a qu'un seul nom
        names = [names]
    for name in names:
        languages.add(name["@LanguageCode"])

# Trier les langues pour les colonnes
language_columns = sorted(languages)
headers.extend(language_columns)

# Écrire le fichier CSV
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    for airport in data:
        row = {
            'AirportCode': airport.get('AirportCode'),
            'CityCode': airport.get('CityCode'),
            'CountryCode': airport.get('CountryCode'),
            'Latitude': airport.get('Position', {}).get('Coordinate', {}).get('Latitude'),
            'Longitude': airport.get('Position', {}).get('Coordinate', {}).get('Longitude'),
            'UtcOffset': airport.get('UtcOffset'),
            'TimeZoneId': airport.get('TimeZoneId')
        }

        # Initialiser les noms par langue à vide
        for lang in language_columns:
            row[lang] = ''

        names = airport.get("Names", {}).get("Name", [])
        if isinstance(names, dict):  # un seul nom
            names = [names]
        for name in names:
            lang = name["@LanguageCode"]
            row[lang] = name["$"]

        writer.writerow(row)

print("CSV généré avec succès sous le nom 'airports.csv'")


# Compter les occurrences de chaque AirportCode
airport_code_counter = Counter(airport.get("AirportCode") for airport in data)
duplicates = {code: count for code, count in airport_code_counter.items() if count > 1}
# Affichage des doublons
if duplicates:
    print("🚨 Doublons détectés sur les AirportCode :")
    for code, count in duplicates.items():
        print(f"  - {code} apparaît {count} fois")
else:
    print("✅ Aucun doublon détecté sur les AirportCode.")

