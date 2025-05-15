import streamlit as st
from utils import cargar_datos

def mostrar_landing():
    df = cargar_datos()
    st.title("💼 Explorador de Ofertas de Empleo en IT - Tecnoempleo")

    # Mostrar la imagen principal sin advertencia
    st.image("data/tecnoempleo_banner.jpg", use_container_width=True)

    st.header("✅ Resumen General")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Ofertas", len(df))
    with col2:
        st.metric("Empresas Únicas", df["empresa"].nunique())
    with col3:
        st.metric("Tecnologías Usadas", df["tecnologias"].str.split(',').explode().nunique())
