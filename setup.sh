#!/bin/bash
set -e

PROJECT_ROOT=$(pwd)
API_DIR="$PROJECT_ROOT/src/api"
MODEL_DIR="$PROJECT_ROOT/models"

# Vérifier que le modèle existe
if [ ! -f "$MODEL_DIR/ML_flight_delay.pkl" ]; then
  echo "❌ Modèle ML_flight_delay.pkl introuvable dans $MODEL_DIR"
  exit 1
fi

echo "✅ Modèle trouvé"

# -----------------------------
# Dockerfile FastAPI
# -----------------------------
cat > "$API_DIR/Dockerfile.fastapi" <<EOF
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copier le modèle depuis la racine
COPY ../../models /app/models

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

echo "✅ Dockerfile FastAPI créé"

# -----------------------------
# Dockerfile Streamlit
# -----------------------------
cat > "$API_DIR/Dockerfile.streamlit" <<EOF
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "ihm.py", "--server.port=8501", "--server.address=0.0.0.0"]
EOF

echo "✅ Dockerfile Streamlit créé"

# -----------------------------
# main.py FastAPI
# -----------------------------
cat > "$API_DIR/main.py" <<'EOF'
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import List, Union
from pydantic import BaseModel
import subprocess
import os
import pickle
import jwt
import pandas as pd

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

fake_users_db = {
    "admin": {"username": "admin", "password": "admin123"},
    "testuser": {"username": "testuser", "password": "test123"}
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

class Flight(BaseModel):
    DepartureAirport: str
    DepartureScheduledDate: Union[str, None] = None
    DepartureScheduledTime: Union[str, None] = None
    ArrivalAirport: str
    ArrivalScheduledDate: Union[str, None] = None
    ArrivalScheduledTime: Union[str, None] = None
    AirlineID: str
    FlightNumber: Union[str, int]
    AircraftCode: str
    DepartureDayPeriod: str

class PredictionResponse(BaseModel):
    FlightNumber: Union[str, int]
    PredictedArrivalDelay: bool

app = FastAPI(title="DST Airlines API")

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/flights/tomorrow")
def get_flights_tomorrow(user: str = Depends(get_current_user)):
    # Appel réel API Lufthansa ou traitement CSV réel
    # Ici on suppose que le script shell retourne un CSV réel
    tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")
    base_dir = "/app/"
    script_dir = "/app/src/data/lufthansa/"
    token_dir = "/app/data/token/"
    output_dir = "/app/data/lufthansa/"

    cmd = [
        "sh",
        os.path.join(script_dir, "launch_flux_tomorrow.sh"),
        base_dir,
        script_dir,
        token_dir,
        output_dir,
    ]
    subprocess.run(cmd, check=True)

    csv_file = os.path.join(output_dir, f"flights_{tomorrow}.csv")
    if not os.path.exists(csv_file):
        raise HTTPException(status_code=404, detail="Flights data not found")

    df = pd.read_csv(csv_file)
    return df.to_dict(orient="records")

@app.post("/predict", response_model=List[PredictionResponse])
def predict(flights: List[Flight], user: str = Depends(get_current_user)):
    model_path = "/app/models/ML_flight_delay.pkl"
    if not os.path.exists(model_path):
        raise HTTPException(status_code=500, detail="Model not found")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    df = pd.DataFrame([f.dict() for f in flights])
    X = df[["DepartureDayPeriod", "DepartureAirport", "ArrivalAirport", "AirlineID", "FlightNumber", "AircraftCode"]]
    X["FlightNumber"] = X["FlightNumber"].astype(str)

    try:
        preds = model.predict(X)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

    return [
        {"FlightNumber": flight.FlightNumber, "PredictedArrivalDelay": bool(pred)}
        for flight, pred in zip(flights, preds)
    ]
EOF

echo "✅ main.py FastAPI créé"

# -----------------------------
# ihm.py Streamlit
# -----------------------------
cat > "$API_DIR/ihm.py" <<'EOF'
import streamlit as st
import requests

API_URL = "http://fastapi:8000"

st.set_page_config(page_title="DST Airlines", page_icon="✈️")
st.title("✈️ DST Airlines - Prédiction des Retards")

st.sidebar.header("Authentification")
username = st.sidebar.text_input("Nom d'utilisateur", "testuser")
password = st.sidebar.text_input("Mot de passe", "test123", type="password")

if st.sidebar.button("Se connecter"):
    response = requests.post(f"{API_URL}/login", data={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        st.session_state["token"] = token
        st.sidebar.success("✅ Connecté")
    else:
        st.sidebar.error("❌ Identifiants invalides")

if "token" in st.session_state:
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{API_URL}/flights/tomorrow", headers=headers)

    if response.status_code == 200:
        flights = response.json()
        st.subheader("📋 Vols du lendemain")

        for i, flight in enumerate(flights):
            with st.container():
                st.markdown(
                    f"**{flight['DepartureAirport']} → {flight['ArrivalAirport']} | Vol {flight['FlightNumber']}**\n\n"
                    f"🛫 Départ prévu : {flight.get('DepartureScheduledDate','')} {flight.get('DepartureScheduledTime','')}\n"
                    f"🛬 Arrivée prévue : {flight.get('ArrivalScheduledDate','')} {flight.get('ArrivalScheduledTime','')}\n"
                    f"✈️ Compagnie : {flight['AirlineID']}  |  Aircraft : {flight.get('AircraftCode','')}\n"
                    f"🕒 Départ : {flight.get('DepartureDayPeriod','')}"
                )

                if st.button(f"Prédire retard pour vol {flight['FlightNumber']}", key=f"btn_{i}"):
                    flight_to_predict = [flight]
                    pred_resp = requests.post(f"{API_URL}/predict", headers=headers, json=flight_to_predict)
                    if pred_resp.status_code == 200:
                        prediction = pred_resp.json()[0]
                        if prediction["PredictedArrivalDelay"]:
                            st.error("⚠️ Ce vol risque d'avoir un retard")
                        else:
                            st.success("✅ Ce vol devrait être à l'heure")
                    else:
                        st.error(f"Erreur lors de la prédiction : {pred_resp.status_code} - {pred_resp.text}")
    else:
        st.error("Impossible de récupérer les vols du lendemain.")
EOF

echo "✅ ihm.py Streamlit créé"

echo "🎉 Tous les fichiers et Dockerfiles sont prêts. Tu peux lancer :"
echo "docker-compose up --build"
