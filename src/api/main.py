from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import pandas as pd
import pickle
import os
import subprocess
from typing import List, Optional

# ---------------------------
# Config
# ---------------------------
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ---------------------------
# Fake Users DB (in-memory)
# ---------------------------
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin123",  # ⚠️ à remplacer par un hash dans un vrai cas
    }
}

# ---------------------------
# Auth Helpers
# ---------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ---------------------------
# Models
# ---------------------------
class Flight(BaseModel):
    DepartureDayPeriod: str
    DepartureAirport: str
    ArrivalAirport: str
    AirlineID: str
    FlightNumber: str
    AircraftCode: str

class PredictionResponse(BaseModel):
    FlightNumber: str
    ArrivalDelay_Pred: bool

class RegisterUser(BaseModel):
    username: str
    password: str

# ---------------------------
# Routes
# ---------------------------
@app.get("/")
def read_root():
    return {"message": "✈️ API DST_Airlines is running 🚀"}

@app.post("/register")
def register(user: RegisterUser):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_users_db[user.username] = {
        "username": user.username,
        "password": user.password  # ⚠️ en vrai il faut hasher le mot de passe
    }
    return {"msg": f"User {user.username} registered successfully"}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/flights/tomorrow")
def get_flights_tomorrow(user: str = Depends(get_current_user)):
    tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")
    csv_path = f"/home/ubuntu/DST_Airlines/data/lufthansa/flights_{tomorrow}.csv"

    # Si le CSV n'existe pas encore → on lance le shell
    if not os.path.exists(csv_path):
        base_dir = "/home/ubuntu/DST_Airlines/"
        script_dir = "/home/ubuntu/DST_Airlines/src/data/lufthansa/"
        token_dir = "/home/ubuntu/DST_Airlines/data/token/"
        output_dir = "/home/ubuntu/DST_Airlines/data/lufthansa/"

        try:
            subprocess.run(
                ["sh", os.path.join(script_dir, "launch_flux_tomorrow.sh"),
                 base_dir, script_dir, token_dir, output_dir],
                check=True, capture_output=True, text=True
            )
        except subprocess.CalledProcessError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors du lancement du script : {e.stderr}"
            )

    # Vérifier si le CSV a bien été généré
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Fichier des vols introuvable après génération")

    # Charger et renvoyer les vols
    df = pd.read_csv(csv_path)
    return df.to_dict(orient="records")


@app.post("/predict", response_model=List[PredictionResponse])
def predict(flights: List[Flight], user: str = Depends(get_current_user)):
    # Charger le modèle
    model_path = "./models/model.pkl"
    if not os.path.exists(model_path):
        raise HTTPException(status_code=500, detail="Model not found")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    df = pd.DataFrame([f.dict() for f in flights])
    preds = model.predict(df)

    return [
        {"FlightNumber": f.FlightNumber, "ArrivalDelay_Pred": bool(p)}
        for f, p in zip(flights, preds)
    ]
