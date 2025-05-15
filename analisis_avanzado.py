import streamlit as st
import pandas as pd
import plotly.express as px
from utils import cargar_datos
import unidecode

def mostrar_analisis_avanzado():
    df = cargar_datos()
    st.title("📊 Análisis Avanzado de Ofertas IT")

    # ───── Contrato vs Jornada en columnas ─────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📁 Tipo de Contrato más común")
        contrato = df["tipo_contrato"].astype(str).str.strip()
        contrato = contrato[contrato != ""]
        if not contrato.empty:
            top_contrato = contrato.value_counts().head(10).reset_index()
            top_contrato.columns = ["Tipo de Contrato", "Número de Ofertas"]
            fig1 = px.pie(top_contrato, names="Tipo de Contrato", values="Número de Ofertas", hole=0.4)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("No hay datos válidos de tipo de contrato para mostrar.")

    with col2:
        st.subheader("⏰ Tipos de Jornada más comunes")
        jornada = df["jornada"].astype(str).str.strip()
        jornada = jornada[jornada != ""]
        if not jornada.empty:
            top_jornada = jornada.value_counts().head(10).reset_index()
            top_jornada.columns = ["Jornada", "Ofertas"]
            fig4 = px.pie(top_jornada, names="Jornada", values="Ofertas", title="", hole=0.4)
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning("No hay datos de jornada para mostrar.")

    # ───── Años de Experiencia en bloque abajo ─────
    st.subheader("⏳ Años de Experiencia Requerida")
    if "experiencia" in df.columns:
        experiencia = df["experiencia"].astype(str).str.strip().str.lower()
        experiencia = experiencia.apply(unidecode.unidecode)
        experiencia = experiencia.replace({
            "mas de 5 anos": "Más de 5 años",
            "mas de 10 anos": "Más de 10 años",
            "3 anos": "3 años",
            "3-5 anos": "3-5 años",
            "1 ano": "1 año",
            "2 anos": "2 años",
            "sin experiencia": "Sin experiencia",
            "menos de un ano": "Menos de un año",
            "3 aÃ±os": "3 años",
            "mas de 5 aÃ±os": "Más de 5 años"
        })
        top_exp = experiencia.value_counts().head(10).reset_index()
        top_exp.columns = ["Experiencia", "Ofertas"]
        if not top_exp.empty:
            fig3 = px.bar(
                top_exp,
                x="Experiencia",
                y="Ofertas",
                color="Experiencia",
                height=400
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("No hay datos válidos de experiencia para mostrar.")
    else:
        st.warning("No se encuentra la columna 'experiencia'.")
