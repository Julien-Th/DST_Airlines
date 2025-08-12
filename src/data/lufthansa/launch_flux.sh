# arguments
WD_PATH=$1
SCRIPT_PATH=$2
TOKEN_PATH=$3
OUTPUT_PATH=$4
#WD_PATH= /home/ubuntu/DST_Airlines/
#SCRIPT_PATH= /home/ubuntu/DST_Airlines/src/data/lufthansa/
#TOKEN_PATH = /home/ubuntu/DST_Airlines/data/token/
#OUTPUT_PATH= /home/ubuntu/DST_Airlines/data/lufthansa/
# Aller dans le répertoire de travail
cd "$WD_PATH" || exit 1


# put current date as yyyy-mm-dd in $date
date=$(date --date 'next day' '+%Y-%m-%d')

echo "Launching flux for ${date}"

# Scripts (noms fixes)
TOKEN_SCRIPT="$SCRIPT_PATH/get_lufthansa_token.py"
FLIGHT_STATUS_SCRIPT="$SCRIPT_PATH/flux/get_flight_status.py"
MULTIPLE_FLIGHTS_SCRIPT="$SCRIPT_PATH/flux/get_multiple_flights.py"

# Executions
# Flight status
#python3 "$TOKEN_SCRIPT" "$TOKEN_PATH"
#python3 "$FLIGHT_STATUS_SCRIPT" "$date" "$TOKEN_PATH" "$OUTPUT_PATH"

# Multiple flights
python3 "$TOKEN_SCRIPT" "$TOKEN_PATH"
python3 "$MULTIPLE_FLIGHTS_SCRIPT" "$date" "$TOKEN_PATH" "$OUTPUT_PATH"