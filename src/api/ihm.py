import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="DST Airlines", page_icon="✈️")

st.title("✈️ DST Airlines - Prédiction des Retards")

# --- Login (token)
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

# --- Liste des vols
if "token" in st.session_state:
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{API_URL}/flights/tomorrow", headers=headers)

    if response.status_code == 200:
        flights = response.json()
        st.subheader("📋 Vols du lendemain")
        for i, flight in enumerate(flights):
            with st.container():
                st.write(f"**{flight['DepartureAirport']} → {flight['ArrivalAirport']}**")
                st.write(f"🛫 Départ prévu : {flight['DepartureScheduledDate']} {flight['DepartureScheduledTime']}")
                st.write(f"🛬 Arrivée prévue : {flight['ArrivalScheduledDate']} {flight['ArrivalScheduledTime']}")
                st.write(f"✈️ Compagnie : {flight['AirlineID']}  |  Vol : {flight['FlightNumber']}")
                
                if st.button(f"Prédire retard pour vol {flight['FlightNumber']}", key=f"btn_{i}"):
                    pred_resp = requests.post(f"{API_URL}/predict", headers=headers, json=[flight])
                    if pred_resp.status_code == 200:
                        prediction = pred_resp.json()[0]
                        if prediction["PredictedArrivalDelay"]:
                            st.error("⚠️ Ce vol risque d'avoir un retard")
                        else:
                            st.success("✅ Ce vol devrait être à l'heure")
    else:
        st.error("Impossible de récupérer les vols.")
