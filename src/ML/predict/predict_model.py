import sys
import pandas as pd
import pickle

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python predict.py <input_model.pkl> <input_csv> <output_csv>")
        sys.exit(1)

    input_model = sys.argv[1]
    input_csv = sys.argv[2]
    output_csv = sys.argv[3]

    # 🔹 Charger le modèle (pipeline complet)
    with open(input_model, "rb") as f:
        model = pickle.load(f)

    # 🔹 Charger les nouvelles données
    df_new = pd.read_csv(input_csv)

    # Variables utilisées pour la prédiction
    features = ["DepartureDayPeriod", "DepartureAirport", "ArrivalAirport", 
                "AirlineID", "FlightNumber", "AircraftCode"]

    if not all(col in df_new.columns for col in features):
        raise ValueError(f"Le fichier doit contenir au minimum les colonnes : {features}")

    X_new = df_new[features]

    # 🔹 Faire la prédiction
    preds = model.predict(X_new)

    # Ajouter la prédiction au DataFrame
    df_new["ArrivalDelay_Pred"] = preds

    # Sauvegarde
    df_new.to_csv(output_csv, index=False)
    print(f"Prédictions sauvegardées dans : {output_csv}")
