# Flight Delay Prediction  

Ce projet permet de :  
1. **Préparer les données** (`create_features.py`) → ajout de variables utiles.  
2. **Entraîner un modèle ML** (`train_model.py`) → prédiction de retard à l’arrivée.  
3. **Faire des prédictions** sur de nouveaux vols (`predict.py`).  

---

## 1. Feature Engineering (`create_features.py`)

Ce script :  
- Combine plusieurs fichiers CSV contenant des vols (nommés `flights_YYYY-MM-DD.csv`).  
- Filtre les fichiers selon une **date de début** et une **date de fin**.  
- Ajoute la variable target :  
  - `ArrivalDelay` : booléen (`True` si `ArrivalDelayMinutes > 0`).   
- Sauvegarde le dataset enrichi dans un nouveau CSV.  

### Utilisation
```bash
python3 create_features.py <input_folder> <start_date> <end_date> <output_csv>
```

- `<input_folder>` : dossier contenant les fichiers `flights_YYYY-MM-DD.csv`.  
- `<start_date>` et `<end_date>` : bornes de l’intervalle (format `YYYY-MM-DD`).  
- `<output_csv>` : chemin de sortie du CSV enrichi.  

### Exemple
```bash
python3 feature_engineering/create_features.py /home/ubuntu/DST_Airlines/data/lufthansa 2025-08-12 2025-08-21 /home/ubuntu/DST_Airlines/data/train/flights_train_202508.csv
```

---

## 2. Training (`train_model.py`)

Ce script :  
- Charge le CSV enrichi.  
- Entraîne plusieurs modèles (`LogisticRegression`, `DecisionTree`, `RandomForest`).  
- Évalue leur performance avec un **jeu train/test**.  
- Sélectionne le meilleur modèle.  
- Sauvegarde le modèle **complet (pipeline = prétraitement + modèle)** en `.pkl`.  

### Utilisation
```bash
python3 train_model.py <input_csv> <output_model.pkl>
```

- `<input_csv>` : CSV enrichi (sortie de `feature_engineering.py`).  
- `<output_model.pkl>` : chemin du fichier modèle sauvegardé.  

### Exemple
```bash
python3 train_model.py /home/ubuntu/DST_Airlines/data/train/flights_train_202508.csv /home/ubuntu/DST_Airlines/models/ML_flight_delay.pkl
```

---

## 3. Prediction (`predict_model.py`)

Ce script :  
- Charge le modèle sauvegardé (`.pkl`).  
- Charge un CSV avec de **nouveaux vols** (mêmes colonnes explicatives).  
- Applique automatiquement le prétraitement + modèle.  
- Ajoute une colonne `ArrivalDelay_Pred` (prédiction du retard).  
- Sauvegarde le résultat dans un CSV.  

### Utilisation
```bash
python3 predict_model.py <input_model.pkl> <input_csv> <output_csv>
```

- `<input_model.pkl>` : modèle sauvegardé.  
- `<input_csv>` : CSV des nouveaux vols à prédire (doit contenir au minimum :  
  `DepartureDayPeriod, DepartureAirport, ArrivalAirport, AirlineID, FlightNumber, AircraftCode`).  
- `<output_csv>` : fichier CSV avec les prédictions ajoutées.  

### Exemple
```bash
python3 predict_model.py /home/ubuntu/DST_Airlines/models/ML_flight_delay.pkl /home/ubuntu/DST_Airlines/data/predict/flights_2025-08-22.csv /home/ubuntu/DST_Airlines/data/predict/predicted_flights_2025-08-22.csv
```

---

## Résumé du workflow

1. **Préparer les données**  
   ```bash
   python feature_engineering.py ./data 2025-08-15 2025-08-17 ./outputs/flights_features.csv
   ```

2. **Entraîner et sauvegarder le modèle**  
   ```bash
   python train_model.py ./outputs/flights_features.csv ./models/flight_model.pkl
   ```

3. **Faire des prédictions sur de nouveaux vols**  
   ```bash
   python predict.py ./models/flight_model.pkl ./data/new_flights.csv ./outputs/predictions.csv
   ```
