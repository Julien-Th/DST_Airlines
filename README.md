# DST_Airlines
DataScientest - Parcours DE - Projet Airlines
Promotion DE Continu Oct 24

## Clone from github
Read and follow `doc/Readme.md`
Execute `sudo chmod 775 data`

# Install Airflow
Read and follow `doc/airflow.md`

## Our API + IHM
### Launch
Execute `docker-compose up --build`
### Go to API docs
http://localhost:8001/docs
### Go to IHM
http://localhost:8502/

## Arborescence projet
<pre> 
├── Requetes_SQL
│   └── database
│       └── create_database.sql

├── airflow
│   ├── dags
│   │   ├── __pycache__
│   │   └── get_lufthansa_flux.py
│   ├── logs
│   │   ├── dag_id=Lufthansa_API
│   │   ├── dag_processor_manager
│   │   └── scheduler
│   ├── plugins
│   ├── airflow.sh
│   └── docker-compose.yaml
├── data -- gitignored on github
│   ├── lufthansa
│   │   ├── flights_2025-09-22.csv
│   │   └── flights_2025-09-22.json
│   └── token
│       └── access_token.txt
├── doc
│   ├── imgs
│   │   ├── API.md
│   │   ├── IHM.md
│   │   ├── airflow.md
│   │   ├── image-1.png
│   │   ├── image-2.png
│   │   ├── image-3.png
│   │   ├── image-4.png
│   │   └── image.png
│   ├── uml
│   │   ├── UML-Airlines.JPG
│   │   └── UML-Airlines.drawio
│   ├── LufthansaAPI.md
│   ├── ML.md
│   ├── Readme.md
│   ├── airflow.md
│   ├── cheatsheet.md
│   ├── db_postgres.md
│   └── python.md
├── models
│   └── ML_flight_delay.pkl
├── src
│   ├── ML
│   │   ├── feature_engineering
│   │   ├── predict
│   │   └── train
│   ├── api
│   │   ├── Dockerfile.fastapi
│   │   ├── Dockerfile.streamlit
│   │   ├── ihm.py
│   │   ├── main.py
│   │   ├── use.sh
│   │   └── use_examples.sh
│   ├── data
│   │   └── lufthansa
│   │       ├── flux
│   │       │   ├── get_flight_status.py
│   │       │   ├── get_multiple_flights.py
│   │       │   └── get_multiple_flights_tomorrow.py
│   │       ├── referentiels
│   │       │   ├── get_aircrafts.py
│   │       │   ├── get_airlines.py
│   │       │   ├── get_airports.py
│   │       │   ├── get_cities.py
│   │       │   └── get_countries.py
│   │       ├── check_data_csv_export.py
│   │       ├── get_lufthansa_token.py
│   │       ├── launch_flux.sh
│   │       ├── launch_flux_tomorrow.sh
│   │       ├── launch_referentiels.sh
│   │       ├── parse_json_airlines.py
│   │       └── parse_json_airports.py
│   ├── postgres
│   │   ├── init
│   │   ├── docker-compose.yaml
│   │   └── init_tables.sh
│   └── requirements.txt
├── README.md
├── docker-compose.yml
└── requirements.txt
</pre>

