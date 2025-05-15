import pandas as pd
import streamlit as st

@st.cache_data
def cargar_datos():
    # Cargar el archivo final definitivo
    df = pd.read_csv("data/ofertas_unificadas_enriquecido.csv")

    # Corregir columnas mal nombradas y unificar nombres
    df.rename(columns={
        "tecnologias_x": "tecnologias",
        "es_jefedepoyeco": "es_jefe_de_proyecto",
        "es_técnicodesisemas": "es_tecnico_de_sistemas",
        "es_cibeseguidad": "es_ciberseguridad",
        "es_idusia": "es_industria",
        "es_aquiecotic": "es_arquitecto_it",
        "es_igeieos": "es_ingeniero",
        "es_(pesecial)": "es_especialista",
        "es_yoas": "otros",
        "es_yoast": "otros_2",
        "es_híbridoyoast": "otros_3",
        "es_híbridoyoas": "otros_4"
    }, inplace=True)

    # Conversión explícita de algunas columnas nuevas
    for col in ["formacion_minima", "idioma"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df.fillna("", inplace=True)
    return df

@st.cache_data
def cargar_datos_recomendador():
    return pd.read_csv("data/ofertas_recomendador.csv")
