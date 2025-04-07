import json
import csv
import hashlib
from collections import defaultdict

input_file = "/home/ubuntu/DST_Airlines/data/lufthansa/airports.json"
output_file = "/home/ubuntu/DST_Airlines/data/lufthansa/airports.csv"

def get_airport_hash(airport):
    """Crée un hash unique pour l'objet JSON (pour détecter les doublons parfaits)."""
    return hashlib.md5(json.dumps(airport, sort_keys=True).encode('utf-8')).hexdigest()

# Charger les données JSON
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Grouper les aéroports par AirportCode
airport_groups = defaultdict(list)
for airport in data:
    code = airport.get("AirportCode")
    airport_groups[code].append(airport)

# Supprimer les doublons parfaits
deduplicated_data = []
print("\n🔍 Analyse des doublons :")
for code, group in airport_groups.items():
    unique_hashes = {}
    for airport in group:
        airport_hash = get_airport_hash(airport)
        if airport_hash not in unique_hashes:
            unique_hashes[airport_hash] = airport
        else:
            print(f"✂️ Doublon parfait retiré pour {code}")
    
    if len(group) > 1:
        print(f"📌 {code} a {len(group)} occurrence(s), {len(unique_hashes)} gardée(s).")
    
    deduplicated_data.extend(unique_hashes.values())

# Identifier toutes les langues
languages = set()
for airport in deduplicated_data:
    names = airport.get("Names", {}).get("Name", [])
    if isinstance(names, dict):
        names = [names]
    for name in names:
        languages.add(name["@LanguageCode"])

# Préparer les en-têtes CSV
headers = [
    'AirportCode',
    'CityCode',
    'CountryCode',
    'Latitude',
    'Longitude',
    'UtcOffset',
    'TimeZoneId'
]
language_columns = sorted(languages)
headers.extend(language_columns)

# Écrire le fichier CSV
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    for airport in deduplicated_data:
        row = {
            'AirportCode': airport.get('AirportCode'),
            'CityCode': airport.get('CityCode'),
            'CountryCode': airport.get('CountryCode'),
            'Latitude': airport.get('Position', {}).get('Coordinate', {}).get('Latitude'),
            'Longitude': airport.get('Position', {}).get('Coordinate', {}).get('Longitude'),
            'UtcOffset': airport.get('UtcOffset'),
            'TimeZoneId': airport.get('TimeZoneId')
        }

        for lang in language_columns:
            row[lang] = ''

        names = airport.get("Names", {}).get("Name", [])
        if isinstance(names, dict):
            names = [names]
        for name in names:
            row[name["@LanguageCode"]] = name["$"]

        writer.writerow(row)

print("\n✅ CSV généré avec doublons parfaits supprimés.")
