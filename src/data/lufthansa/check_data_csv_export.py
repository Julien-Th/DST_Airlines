# Libraries
import json
import pandas as pd

# Countries data : from JSON to dataframe
# Ouverture du fichier JSON
with open('/home/ubuntu/DST_Airlines/data/lufthansa/countries.json', 'r') as f:
    countries = json.load(f)

# Liste pour stocker les données sous forme de tuples (CountryCode, LanguageCode, Name)
records = []
index=0

# Parcours du JSON pour extraire les informations
for country in countries:
    index +=1
    country_code = country["CountryCode"]

    # Vérifier si 'Names' existe et si c'est une liste ou un dictionnaire
    if "Names" in country:
        names = country["Names"]
        
        # Si 'Names' est un dictionnaire avec une clé "Name"
        if isinstance(names, dict) and "Name" in names:
            name_info = names["Name"]
            # Si 'Name' est une liste
            if isinstance(name_info, list):
                for name_item in name_info:
                    language_code = name_item.get("@LanguageCode", "")
                    name = name_item.get("$", "")
                    records.append((country_code, language_code, name))
            # Si 'Name' est un dictionnaire
            elif isinstance(name_info, dict):
                language_code = name_info.get("@LanguageCode", "")
                name = name_info.get("$", "")
                records.append((country_code, language_code, name))
            
            else:
                print("Name isn't a dict or a list for",country_code,"index",index)
        
        # Si "Names" est déjà une liste
        elif isinstance(names, list):
            for name_info in names:
                # Vérification que 'name_info' est bien un dictionnaire
                if isinstance(name_info, dict):
                    language_code = name_info.get("@LanguageCode", "")
                    name = name_info.get("$", "")
                    records.append((country_code, language_code, name))
                else :
                    print("name_info isn't a dict for",country_code,"index",index)

        else :
            print("Names isn't a dict or a list for",country_code,"index",index)

    else:
        print("Names not in country for",country_code,"index",index)

# Création d'un DataFrame avec les données extraites
df_countries = pd.DataFrame(records, columns=["CountryCode", "CountryLanguageCode", "CountryName"])

# Afficher le DataFrame
print(df_countries.head)

# Filtre pour ne garder que les Names en anglais
df_countries_en = df_countries[df_countries['CountryLanguageCode'] == 'EN']

# Vérification qu'aucun CountryCode n'a été perdu
country_codes_all = df_countries['CountryCode'].unique()
country_codes_en = df_countries['CountryCode'].unique()

missing_country_codes = set(country_codes_all) - set(country_codes_en)
if missing_country_codes:
    print(f"Les CountryCodes suivants ont été perdus : {missing_country_codes}")
else:
    print("\nAucun CountryCode n'a été perdu.")


# Renomme les colonnes
#df_countries_en = df_countries_en.rename(columns={'Name': 'CountryName'})
#df_countries_en = df_countries_en.rename(columns={'LanguageCode': 'CountryLanguageCode'})
#print(df_countries_en.head)


# Cities data : from JSON to dataframe
# Ouverture du fichier JSON
with open('/home/ubuntu/DST_Airlines/data/lufthansa/cities.json', 'r') as f:
    cities = json.load(f)

# Liste pour stocker les données sous forme de tuples (CityCode,CountryCode, LanguageCode, Name)
records = []
index=0

# Parcours du JSON pour extraire les informations
for city in cities:
    index +=1
    country_code = city["CountryCode"]
    city_code = city["CityCode"]

    # Vérifier si 'Names' existe et si c'est une liste ou un dictionnaire
    if "Names" in city:
        names = city["Names"]
        
        # Si 'Names' est un dictionnaire avec une clé "Name"
        if isinstance(names, dict) and "Name" in names:
            name_info = names["Name"]
            # Si 'Name' est une liste, traiter comme une liste normale
            if isinstance(name_info, list):
                for name_item in name_info:
                    language_code = name_item.get("@LanguageCode", "")
                    name = name_item.get("$", "")
                    records.append((city_code,country_code, language_code, name))
            # Si 'Name' est un dictionnaire (cas particulier)
            elif isinstance(name_info, dict):
                language_code = name_info.get("@LanguageCode", "")
                name = name_info.get("$", "")
                records.append((city_code,country_code, language_code, name))
            
            else:
                print("Name isn't a dict or a list for",city_code,"index",index)
        
        # Si "Names" est déjà une liste
        elif isinstance(names, list):
            for name_info in names:
                # Vérification que 'name_info' est bien un dictionnaire
                if isinstance(name_info, dict):
                    language_code = name_info.get("@LanguageCode", "")
                    name = name_info.get("$", "")
                    records.append((city_code,country_code, language_code, name))
                else :
                    print("name_info isn't a dict for",city_code,"index",index)

        else :
            print("Names isn't a dict or a list for",city_code,"index",index)

    else:
        print("Names not in city for",city_code)

# Création d'un DataFrame avec les données extraites
df_cities = pd.DataFrame(records, columns=["CityCode","CountryCode", "CityLanguageCode", "CityName"])

# Afficher le DataFrame
print(df_cities.head)

# Filtre pour ne garder que les Names en anglais
df_cities_en = df_cities[df_cities['CityLanguageCode'] == 'EN']

# Vérifier qu'aucun CountryCode n'a été perdu
city_codes_all = df_cities['CityCode'].unique()
city_codes_en = df_cities['CityCode'].unique()

# Vérifier si des CityCodes ont été perdus
missing_city_codes = set(city_codes_all) - set(city_codes_en)
if missing_city_codes:
    print(f"Les CityCodes suivants ont été perdus : {missing_city_codes}")
else:
    print("Aucun CityCode n'a été perdu.")


# Renomme les colonnes
#df_cities_en = df_cities_en.rename(columns={'Name': 'CityName'})
#df_cities_en = df_cities_en.rename(columns={'LanguageCode': 'CityLanguageCode'})
#print(df_cities_en.head)


# Vérifier que tous les CountryCode de Cities sont dans Countries et inversement
missing_in_countries = set(df_cities_en['CountryCode']) - set(df_countries_en['CountryCode'])
missing_in_cities = set(df_countries_en['CountryCode']) - set(df_cities_en['CountryCode'])

# Afficher les résultats
if missing_in_countries:
    print(f"Les CountryCodes suivants sont dans Cities mais pas dans Countries : {missing_in_countries}")
else:
    print("Tous les CountryCodes de Cities sont présents dans Countries.")

if missing_in_cities:
    print(f"Les CountryCodes suivants sont dans Countries mais pas dans Cities : {missing_in_cities}")
else:
    print("Tous les CountryCodes de Countries sont présents dans Cities.")


# Vérification que CityCode est une clé primaire
# Compter la fréquence des CityCode dans Cities
city_code_counts = df_cities_en.groupby('CityCode')['CountryCode'].nunique()

# Vérifier si un CityCode est associé à plusieurs CountryCode
non_unique_city_codes = city_code_counts[city_code_counts > 1]

# Afficher les résultats
if not non_unique_city_codes.empty:
    print(f"Les CityCodes suivants sont associés à plusieurs CountryCodes :")
    print(non_unique_city_codes)
else:
    print("Tous les CityCodes sont associés à un seul CountryCode.")


# airports data : from JSON to dataframe
# Ouvrir le fichier JSON en mode lecture
with open('/home/ubuntu/DST_Airlines/data/lufthansa/airports.json', 'r') as f:
    airports = json.load(f)

# Liste pour stocker les données sous forme de tuples (AirportCode,CityCode,CountryCode, LanguageCode, Name)
records = []
index=0

# Parcours du JSON pour extraire les informations pertinentes
for airport in airports:
    index +=1
    country_code = airport["CountryCode"]
    city_code = airport["CityCode"]
    airport_code = airport["AirportCode"]
    location_type = airport["LocationType"]

    # Vérifier si 'Names' existe et si c'est une liste ou un dictionnaire
    if "Names" in airport:
        names = airport["Names"]
        
        # Si 'Names' est un dictionnaire avec une clé "Name"
        if isinstance(names, dict) and "Name" in names:
            name_info = names["Name"]
            # Si 'Name' est une liste, traiter comme une liste normale
            if isinstance(name_info, list):
                for name_item in name_info:
                    language_code = name_item.get("@LanguageCode", "")
                    name = name_item.get("$", "")
                    records.append((airport_code,location_type,city_code,country_code, language_code, name))
            # Si 'Name' est un dictionnaire (cas particulier)
            elif isinstance(name_info, dict):
                language_code = name_info.get("@LanguageCode", "")
                name = name_info.get("$", "")
                records.append((airport_code,location_type,city_code,country_code, language_code, name))
            
            else:
                print("Name isn't a dict or a list for airportcode",airport_code,"index",index)
        
        # Si "Names" est déjà une liste
        elif isinstance(names, list):
            for name_info in names:
                # Vérification que 'name_info' est bien un dictionnaire
                if isinstance(name_info, dict):
                    language_code = name_info.get("@LanguageCode", "")
                    name = name_info.get("$", "")
                    records.append((airport_code,location_type,city_code,country_code, language_code, name))
                else:
                    print("name_info isn't a dict for airportcode",airport_code,"index",index)

        else :
            print("Names isn't a dict or a list for airportcode",airport_code,"index",index)

    else:
        print("Names not in airport for",airport_code,"index",index)

# Créer un DataFrame avec les données extraites
df_airports = pd.DataFrame(records, columns=["AirportCode","LocationType","CityCode","CountryCode", "AirportLanguageCode", "AirportName"])

# Afficher le DataFrame
print(df_airports.head)

df_airports = df_airports[df_airports['LocationType'] == 'Airport']

# Filtre pour ne garder que les Names en anglais
df_airports_en = df_airports[df_airports['AirportLanguageCode'] == 'EN']

# Vérifier qu'aucun AirportCode n'a été perdu
airport_codes_all = df_airports['AirportCode'].unique()
airport_codes_en = df_airports['AirportCode'].unique()

# Vérifier si des AirportCodes ont été perdus
missing_airport_codes = set(airport_codes_all) - set(airport_codes_en)
if missing_airport_codes:
    print(f"Les AirportCodes suivants ont été perdus : {missing_airport_codes}")
else:
    print("Aucun AirportCode n'a été perdu.")


# Renomme les colonnes
#df_airports_en = df_airports_en.rename(columns={'Name': 'AirportName'})
#df_airports_en = df_airports_en.rename(columns={'LanguageCode': 'AirportLanguageCode'})
#print(df_airports_en.head)


# Vérifier que tous les CountryCode de Airports sont dans Countries et inversement
missing_in_countries = set(df_airports_en['CountryCode']) - set(df_countries_en['CountryCode'])
missing_in_airports = set(df_countries_en['CountryCode']) - set(df_airports_en['CountryCode'])

# Afficher les résultats
if missing_in_countries:
    print(f"Les CountryCodes suivants sont dans Airports mais pas dans Countries : {missing_in_countries}")
else:
    print("Tous les CountryCodes de Airports sont présents dans Countries.")

if missing_in_airports:
    print(f"Les CountryCodes suivants sont dans Countries mais pas dans Airports : {missing_in_airports}")
else:
    print("Tous les CountryCodes de Countries sont présents dans Airports.")


# Vérifier que tous les CityCode de Airports sont dans Cities et inversement
missing_in_cities = set(df_airports_en['CityCode']) - set(df_cities_en['CityCode'])
missing_in_airports = set(df_cities_en['CityCode']) - set(df_airports_en['CityCode'])

# Afficher les résultats
if missing_in_cities:
    print(f"Les CityCodes suivants sont dans Airports mais pas dans Cities : {missing_in_cities}")
else:
    print("Tous les CityCodes de Airports sont présents dans Cities.")

if missing_in_airports:
    print(f"Les CityCodes suivants sont dans Cities mais pas dans Airports : {missing_in_airports}")
else:
    print("Tous les CitiCode de Cities sont présents dans Airports.")


# Vérification que AirportCode est une clé primaire
# Compter la fréquence des AirportCodes dans Airports : Country
airport_code_counts = df_airports_en.groupby('AirportCode')['CountryCode'].nunique()

# Vérifier si un AirportCode est associé à plusieurs CountryCode
non_unique_airport_codes = airport_code_counts[airport_code_counts > 1]

# Afficher les résultats
if not non_unique_airport_codes.empty:
    print(f"Les AirportCodes suivants sont associés à plusieurs CountryCodes :")
    print(non_unique_airport_codes)
else:
    print("Tous les AirportCodes sont associés à un seul CountryCode.")


# Compter la fréquence des AirportCodes dans Airports : Cities
airport_code_counts = df_airports_en.groupby('AirportCode')['CityCode'].nunique()

# Vérifier si un AirportCode est associé à plusieurs CityCode
non_unique_airport_codes = airport_code_counts[airport_code_counts > 1]

# Afficher les résultats
if not non_unique_airport_codes.empty:
    print(f"Les AirportCodes suivants sont associés à plusieurs CityCodes :")
    print(non_unique_airport_codes)
else:
    print("Tous les AirportCodes sont associés à un seul CityCode.")


# airlines data : from JSON to dataframe
# Ouvrir le fichier JSON en mode lecture
with open('/home/ubuntu/DST_Airlines/data/lufthansa/airlines.json', 'r') as f:
    airlines = json.load(f)


# Liste pour stocker les données sous forme de tuples (AirlineID, AirlineID_ICAO, Name)
records = []
index=0

# Parcours du JSON pour extraire les informations pertinentes
for airline in airlines:
    index +=1
    airline_ID = airline["AirlineID"]
    airline_ID_ICAO = airline.get("AirlineID_ICAO", None)

    # Vérifier si 'Names' existe et si c'est une liste ou un dictionnaire
    if "Names" in airline:
        names = airline["Names"]
        
        # Si 'Names' est un dictionnaire avec une clé "Name"
        if isinstance(names, dict) and "Name" in names:
            name_info = names["Name"]
            # Si 'Name' est une liste
            if isinstance(name_info, list):
                for name_item in name_info:
                    language_code = name_item.get("@LanguageCode", "")
                    name = name_item.get("$", "")
                    records.append((airline_ID,airline_ID_ICAO, language_code, name))
            # Si 'Name' est un dictionnaire
            elif isinstance(name_info, dict):
                language_code = name_info.get("@LanguageCode", "")
                name = name_info.get("$", "")
                records.append((airline_ID,airline_ID_ICAO, language_code, name))
            
            else:
                print("Name isn't a dict or a list for",airline_ID,"index",index)
        
        # Si "Names" est déjà une liste
        elif isinstance(names, list):
            for name_info in names:
                # Vérification que 'name_info' est bien un dictionnaire
                if isinstance(name_info, dict):
                    language_code = name_info.get("@LanguageCode", "")
                    name = name_info.get("$", "")
                    records.append((airline_ID,airline_ID_ICAO, language_code, name))
                else :
                    print("name_info isn't a dict for",airline_ID,"index",index)

        else :
            print("Names isn't a dict or a list for",airline_ID,"index",index)

    else:
        print("Names not in country for",airline_ID,"index",index)

# Création d'un DataFrame avec les données extraites
df_airlines = pd.DataFrame(records, columns=["AirlineID","AirlineID_ICAO", "AirlineLanguageCode", "Name"])

# Afficher le DataFrame
print(df_airlines.head)


# Filtre pour ne garder que les Names en anglais
df_airlines_en = df_airlines[df_airlines['AirlineLanguageCode'] == 'EN']

# Vérification qu'aucun AirlineID n'a été perdu
airline_codes_all = df_airlines['AirlineID'].unique()
airline_codes_en = df_airlines['AirlineID'].unique()

missing_airline_codes = set(airline_codes_all) - set(airline_codes_en)
if missing_airline_codes:
    print(f"Les AirlineID suivants ont été perdus : {missing_airline_codes}")
else:
    print("\nAucun AirlineID n'a été perdu.")


if df_airlines_en['AirlineID'].is_unique:
    print("Tous les AirlineID sont uniques.")
else:
    print("Il y a des doublons dans les AirlineID.")


duplicate_ids = df_airlines_en['AirlineID'][df_airlines_en['AirlineID'].duplicated()]
if not duplicate_ids.empty:
    print("AirlineID en double :")
    print(duplicate_ids.unique())
else:
    print("Aucun AirlineID en double.")


airline_id_counts = df_airlines_en['AirlineID'].value_counts()
print(airline_id_counts[airline_id_counts > 1])  # Affiche uniquement ceux avec des doublons


# Repérer les AirlineID dupliqués
duplicated_airlines = df_airlines_en[df_airlines_en.duplicated(subset='AirlineID', keep=False)]

# Afficher les lignes concernées
print("Lignes avec des AirlineID dupliqués :")
print(duplicated_airlines.sort_values(by='AirlineID'))

# Renomme les colonnes
#df_airlines_en = df_airlines_en.rename(columns={'Name': 'AirlineName'})
#df_airlines_en = df_airlines_en.rename(columns={'LanguageCode': 'AirlineLanguageCode'})
#print(df_airlines_en.head)

df_airlines_en = df_airlines_en.drop_duplicates(subset=["AirlineID", "AirlineID_ICAO"])

# Aircrafts data : from JSON to dataframe
# Ouverture du fichier JSON
with open('/home/ubuntu/DST_Airlines/data/lufthansa/aircrafts.json', 'r') as f:
    aircrafts = json.load(f)

# Liste pour stocker les données sous forme de tuples (AircraftCode, LanguageCode, Name)
records = []
index=0

# Parcours du JSON pour extraire les informations
for aircraft in aircrafts:
    index +=1
    aircraft_code = aircraft["AircraftCode"]

    # Vérifier si 'Names' existe et si c'est une liste ou un dictionnaire
    if "Names" in aircraft:
        names = aircraft["Names"]
        
        # Si 'Names' est un dictionnaire avec une clé "Name"
        if isinstance(names, dict) and "Name" in names:
            name_info = names["Name"]
            # Si 'Name' est une liste
            if isinstance(name_info, list):
                for name_item in name_info:
                    language_code = name_item.get("@LanguageCode", "")
                    name = name_item.get("$", "")
                    records.append((aircraft_code, language_code, name))
            # Si 'Name' est un dictionnaire
            elif isinstance(name_info, dict):
                language_code = name_info.get("@LanguageCode", "")
                name = name_info.get("$", "")
                records.append((aircraft_code, language_code, name))
            
            else:
                print("Name isn't a dict or a list for",aircraft_code,"index",index)
        
        # Si "Names" est déjà une liste
        elif isinstance(names, list):
            for name_info in names:
                # Vérification que 'name_info' est bien un dictionnaire
                if isinstance(name_info, dict):
                    language_code = name_info.get("@LanguageCode", "")
                    name = name_info.get("$", "")
                    records.append((aircraft_code, language_code, name))
                else :
                    print("name_info isn't a dict for",aircraft_code,"index",index)

        else :
            print("Names isn't a dict or a list for",aircraft_code,"index",index)

    else:
        print("Names not in country for",aircraft_code,"index",index)

# Création d'un DataFrame avec les données extraites
df_aircrafts = pd.DataFrame(records, columns=["AircraftCode", "AircraftLanguageCode", "AircraftName"])

# Afficher le DataFrame
print(df_aircrafts.head)

# Filtre pour ne garder que les Names en anglais
df_aircrafts_en = df_aircrafts[df_aircrafts['AircraftLanguageCode'] == 'EN']

# Vérification qu'aucun AircraftCode n'a été perdu
aircraft_codes_all = df_aircrafts['AircraftCode'].unique()
aircraft_codes_en = df_aircrafts['AircraftCode'].unique()

missing_aircraft_codes = set(aircraft_codes_all) - set(aircraft_codes_en)
if missing_aircraft_codes:
    print(f"Les AircraftCodes suivants ont été perdus : {missing_aircraft_codes}")
else:
    print("\nAucun AircraftCode n'a été perdu.")




# Status dataframe
status = [
    {"StatusCode": "CD", "StatusDescription": "Flight Cancelled"},
    {"StatusCode": "DP", "StatusDescription": "Flight Departed"},
    {"StatusCode": "RT", "StatusDescription": "Flight Rerouted"},
    {"StatusCode": "DV", "StatusDescription": "Flight Diverted"},
    {"StatusCode": "HD", "StatusDescription": "Flight Heavy Delay"},
    {"StatusCode": "FE", "StatusDescription": "Flight Early"},
    {"StatusCode": "OT", "StatusDescription": "Flight On Time"},
    {"StatusCode": "DL", "StatusDescription": "Flight Delayed"},
    {"StatusCode": "LD", "StatusDescription": "Flight Landed"},
    {"StatusCode": "NI", "StatusDescription": "Flight Next Information"},
    {"StatusCode": "NA", "StatusDescription": "No Status"},
]

status = pd.DataFrame(status)

# Export des dataframe en CSV
df_airlines_en.to_csv("/home/ubuntu/DST_Airlines/data/lufthansa/airlines_en.csv", index=False, encoding='utf-8')
df_countries_en.to_csv("/home/ubuntu/DST_Airlines/data/lufthansa/countries_en.csv", index=False, encoding='utf-8')
df_cities_en.to_csv("/home/ubuntu/DST_Airlines/data/lufthansa/cities_en.csv", index=False, encoding='utf-8')
df_airports_en.to_csv("/home/ubuntu/DST_Airlines/data/lufthansa/airports_en.csv", index=False, encoding='utf-8')
df_aircrafts_en.to_csv("/home/ubuntu/DST_Airlines/data/lufthansa/aircrafts_en.csv", index=False, encoding='utf-8')
status.to_csv("/home/ubuntu/DST_Airlines/data/lufthansa/status.csv", index=False, encoding='utf-8')











