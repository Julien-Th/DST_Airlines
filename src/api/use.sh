#!/bin/bash

API_URL="http://127.0.0.1:8000"
USERNAME="testuser"
PASSWORD="test123"

# curl -X POST "http://127.0.0.1:8000/register" \
#      -H "Content-Type: application/json" \
#      -d '{"username": "testuser", "password": "test123"}'

# 1. Login pour récupérer le token
TOKEN=$(curl -s -X POST "$API_URL/login" \
  -d "username=$USERNAME&password=$PASSWORD" \
  | jq -r '.access_token')

if [ "$TOKEN" == "null" ]; then
  echo "❌ Impossible de récupérer le token"
  exit 1
fi

echo "✅ Token récupéré"

# 2. Exemple de vol à prédire
DATA='[
  {
    "DepartureAirport": "CDG",
    "ArrivalAirport": "LHR",
    "AirlineID": "AF",
    "FlightNumber": "123",
    "AircraftCode": "A320",
    "DepartureDayPeriod": "Morning"
  }
]'

# 3. Appel à /predict avec le token
curl -s -X POST "$API_URL/predict" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$DATA" | jq
