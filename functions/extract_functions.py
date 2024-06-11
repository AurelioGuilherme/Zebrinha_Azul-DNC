import requests
import streamlit as st

def extracao_dados_climaticos(lat, lon):
    URL_CLIMA = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=4426b9cdb66cc3e1e9b3f65f07bac17e'
    r = requests.get(URL_CLIMA).json()
    return r


def extracao_dados_de_trafico(cidade_origem, cidade_destino):
    URL_TRANSITO = f"https://maps.googleapis.com/maps/api/directions/json?origin={cidade_origem}&destination={cidade_destino}&key=AIzaSyB8o6TouMPFYxH3_-x2bCPgGorwku_dTYY"
    r = requests.get(URL_TRANSITO)

    if r.status_code == 200:
        data = r.json()
        if data['status'] == 'OK':
            return data
        else:
            st.error(f"Erro na resposta da API: {data['status']}")
  
