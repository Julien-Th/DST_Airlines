cd ~/DST_Airlines/

# generate token
python3 src/data/lufthansa/get_lufthansa_token.py

# create json referentiels
python3 src/data/lufthansa/referentiels/get_aircrafts.py
python3 src/data/lufthansa/referentiels/get_airlines.py
python3 src/data/lufthansa/referentiels/get_cities.py
python3 src/data/lufthansa/referentiels/get_countries.py

# regenerate token
python3 src/data/lufthansa/get_lufthansa_token.py

# create other json referentiels
python3 src/data/lufthansa/referentiels/get_airports.py

# put current date as yyyy-mm-dd in $date
date=$(date '+%Y-%m-%d')

# checking json files + transform into csv
python3 src/data/lufthansa/check_data_csv_export.py