cd ~/DST_Airlines/

# put current date as yyyy-mm-dd in $date
date=$(date '+%Y-%m-%d')

# generate token
python3 src/data/lufthansa/get_lufthansa_token.py
# create json + csv flight status of the day
python3 src/data/lufthansa/flux/get_flight_status.py $date

# generate token
python3 src/data/lufthansa/get_lufthansa_token.py
# create json + csv multiple flights of the day
python3 src/data/lufthansa/flux/get_multiple_flights.py $date