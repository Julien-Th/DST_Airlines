import json
import pandas as pd

input_file = "/home/ubuntu/DST_Airlines/data/lufthansa/airlines.json"
output_file = "/home/ubuntu/DST_Airlines/data/lufthansa/airlines.csv"

# Charger le fichier JSON
with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Extraire les informations nécessaires avec gestion des valeurs manquantes
airlines_list = []
for airline in data:
    airlines_list.append({
        "AirlineID": airline.get("AirlineID", "N/A"),  # Valeur par défaut "N/A" si absent
        "AirlineID_ICAO": airline.get("AirlineID_ICAO", "N/A"),
        "Name": airline.get("Names", {}).get("Name", {}).get("$", "Unknown")  # Gérer les structures absentes
    })

# Créer un DataFrame
df = pd.DataFrame(airlines_list)

# Exporter le DataFrame en CSV
df.to_csv(output_file, index=False, encoding="utf-8")

# Test d'unicité des identifiants
def test_unique_identifiers(df):
    """Vérifie que AirlineID et AirlineID_ICAO sont uniques. Affiche les doublons si erreur."""
    try:
        assert df["AirlineID"].nunique() == len(df), "Les AirlineID ne sont pas uniques !"
        assert df["AirlineID_ICAO"].nunique() == len(df), "Les AirlineID_ICAO ne sont pas uniques !"
        print("✅ Test d'unicité passé avec succès.")
    except AssertionError as e:
        print(f"❌ Erreur : {e}")
        
        # Afficher les 10 premiers doublons de AirlineID
        duplicates_airlineid = df[df.duplicated("AirlineID", keep=False)]
        if not duplicates_airlineid.empty:
            print("\n🔍 Doublons sur AirlineID (10 premiers) :")
            print(duplicates_airlineid.head(10))

        # Afficher les 10 premiers doublons de AirlineID_ICAO
        duplicates_airlineid_icao = df[df.duplicated("AirlineID_ICAO", keep=False)]
        if not duplicates_airlineid_icao.empty:
            print("\n🔍 Doublons sur AirlineID_ICAO (10 premiers) :")
            print(duplicates_airlineid_icao.head(10))

# Lancer le test
test_unique_identifiers(df)
