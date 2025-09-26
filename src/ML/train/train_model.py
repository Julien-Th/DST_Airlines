import sys
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python train_model.py <input_csv> <output_model.pkl>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_model = sys.argv[2]

    # Chargement
    df = pd.read_csv(input_csv)

    # Variables explicatives
    features = ["DepartureDayPeriod", "DepartureAirport", "ArrivalAirport", 
                "AirlineID", "FlightNumber", "AircraftCode"]
    X = df[features]
    y = df["ArrivalDelay"]

    # Colonnes catégorielles
    categorical_cols = features

    # Préprocesseur : OneHotEncoder
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
        ]
    )

    # Modèles candidats
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "DecisionTree": DecisionTreeClassifier(),
        "RandomForest": RandomForestClassifier()
    }

    best_model = None
    best_acc = 0
    best_name = ""

    for name, model in models.items():
        # Pipeline = preprocessing + modèle
        pipe = Pipeline(steps=[("preprocessor", preprocessor),
                               ("model", model)])

        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Entraînement
        pipe.fit(X_train, y_train)

        # Évaluation
        y_pred = pipe.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"{name} Accuracy: {acc:.4f}")

        if acc > best_acc:
            best_acc = acc
            best_model = pipe
            best_name = name

    print(f"Meilleur modèle : {best_name} (accuracy={best_acc:.4f})")
    print("Classification report:\n", classification_report(y_test, best_model.predict(X_test)))

    # Sauvegarde du pipeline complet
    with open(output_model, "wb") as f:
        pickle.dump(best_model, f)

    print(f"Modèle sauvegardé dans : {output_model}")
