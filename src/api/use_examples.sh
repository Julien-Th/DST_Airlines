curl -X POST "http://127.0.0.1:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "test123"}'

curl -X POST "http://127.0.0.1:8000/login" \
     -d "username=testuser&password=test123"

curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:8000/flights/tomorrow

curl -X POST "http://127.0.0.1:8000/predict" \
   -H "Authorization: Bearer <TOKEN>" \
   -H "Content-Type: application/json" \
   -d '[{
         "DepartureDayPeriod": "Morning",
         "DepartureAirport": "CDG",
         "ArrivalAirport": "FRA",
         "AirlineID": "LH",
         "FlightNumber": "1051",
         "AircraftCode": "321"
       }]'
