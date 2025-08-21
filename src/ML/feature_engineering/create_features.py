import os
import sys
import pandas as pd
from datetime import datetime

def load_csvs_in_range(folder_path, start_date, end_date):
    """
    Charge tous les fichiers CSV dont le nom est du type flights_YYYY-MM-DD.csv
    compris entre start_date et end_date.
    """
    dfs = []
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    for file in os.listdir(folder_path):
        if file.startswith("flights_") and file.endswith(".csv"):
            try:
                file_date = datetime.strptime(file.split("_")[1].replace(".csv", ""), "%Y-%m-%d").date()
                if start_date <= file_date <= end_date:
                    df = pd.read_csv(os.path.join(folder_path, file))
                    dfs.append(df)
            except Exception as e:
                print(f"⚠️ Erreur avec le fichier {file} : {e}")

    if not dfs:
        raise ValueError("Aucun fichier valide trouvé dans l’intervalle donné.")
    return pd.concat(dfs, ignore_index=True)

def add_features(df):
    # ArrivalDelay booléen
    df["ArrivalDelay"] = df["ArrivalDelayMinutes"] > 0

    return df

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python feature_engineering.py <input_folder> <start_date> <end_date> <output_csv>")
        sys.exit(1)

    input_folder = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    output_csv = sys.argv[4]

    df = load_csvs_in_range(input_folder, start_date, end_date)
    df = add_features(df)

    df.to_csv(output_csv, index=False)
    print(f"✅ Fichier enrichi sauvegardé : {output_csv}")
