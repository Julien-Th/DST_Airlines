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

# -----------------------------
# CONFIG
# -----------------------------
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# -----------------------------
# Users simulés
# -----------------------------
fake_users_db = {
    "admin": {"username": "admin", "password": "admin123"},
    "testuser": {"username": "testuser", "password": "test123"}
}

# -----------------------------
# Sécurité
# -----------------------------
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

# -----------------------------
# Pydantic Models
# -----------------------------
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

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(title="DST Airlines API")

# -----------------------------
# ROUTES
# -----------------------------
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/flights/tomorrow")
def get_flights_tomorrow(user: str = Depends(get_current_user)):
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

    # Conversion FlightNumber en string pour correspondre au type attendu par le modèle
    X["FlightNumber"] = X["FlightNumber"].astype(str)

    try:
        preds = model.predict(X)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

    return [
        {"FlightNumber": flight.FlightNumber, "PredictedArrivalDelay": bool(pred)}
        for flight, pred in zip(flights, preds)
    ]
