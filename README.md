# DST_Airlines
DataScientest - Parcours DE - Projet Airlines
Année 2025

## Init
Read the `doc/Readme.md`

## Data
### Lufthansa API
https://developer.lufthansa.com/io-docs#/
Steps to get passenger flights data :
- register at https://developer.lufthansa.com/
- follow the instructions until you get your **Key** and your **Secret** (after login)

#### Execute one script

- execute `python3 src/data/lufthansa/get_lufthansa_token.py`

- execute your script with `python3 + name of script`

- see the result in `data/lufthansa/`


#### Get all referentiels

- execute `sh src/data/lufthansa/launch_referentiels.sh`

#### Get flux

- execute `sh src/data/lufthansa/launch_flux.sh /home/ubuntu/DST_Airlines/ /home/ubuntu/DST_Airlines/src/data/lufthansa/ /home/ubuntu/DST_Airlines/data/token/ /home/ubuntu/DST_Airlines/data/lufthansa/`

## Our API
### Launch
Execute `cd DST_Airlines/src/api;uvicorn main:app --reload`
### Docs
http://127.0.0.1:8000/docs