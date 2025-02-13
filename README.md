# DST_Airlines
DataScientest - Parcours DE - Projet Airlines

## Init
Read the `doc/Readme.md`

## Data
### Lufthansa API
https://developer.lufthansa.com/io-docs#/
Steps to get passenger flights data :
- register at https://developer.lufthansa.com/
- follow the instructions until you get your **Key** and your **Secret** (after login)
- execute ```
    python3 src/data/lufthansa/get_lufthansa_token.py
```
- copy your token and replace it in `src/data/lufthansa/get_lufthansa_data.py` on line 4
- execute ```
    python3 get_flight_schedules.py
```
- see the result in `data/lufthansa/horaires_vols.json`