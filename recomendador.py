import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from modelo_recomendador import recomendar_ofertas

def mostrar_recomendador():
    st.title("🎯 Predice tu Próximo Trabajo")
    st.markdown("Completa tu perfil para recibir ofertas compatibles.")

    puestos_disponibles = [
        "Data Engineer", "Data Scientist", "Backend Developer",
        "Frontend Developer", "DevOps", "Fullstack", "Analista", "Consultor"
    ]

    tecnologias_disponibles = [
        "Python", "SQL", "Java", "JavaScript", "C#", "Docker", "Kubernetes",
        "ETL", "AWS", "Azure", "Power BI", "Spark", "Pandas", "TensorFlow"
    ]

    with st.form("form_recomendador"):
        titulo = st.selectbox("Puesto deseado", puestos_disponibles, index=0)
        tipo_puesto = st.selectbox("Tipo de puesto", ["Analista", "Programador", "Consultor", "DevOps", "BigData"])
        tecnologias_seleccionadas = st.multiselect("Tecnologías clave", tecnologias_disponibles, default=["Python", "SQL"])
        jornada = st.selectbox("Tipo de jornada", ["Completa", "Indiferente", "Intensiva", "Media Jornada"])
        remoto = st.checkbox("¿Prefieres trabajar en remoto?", value=True)
        submit = st.form_submit_button("🔍 Buscar ofertas")

    if submit:
        tecnologias = ", ".join(tecnologias_seleccionadas)

        perfil = {
            "titulo": titulo,
            "tipo_puesto": tipo_puesto,
            "tecnologias_x": tecnologias,
            "jornada": jornada,
            "es_remoto": 1 if remoto else 0
        }

        st.info("Buscando coincidencias...")
        resultados = recomendar_ofertas(perfil, top_n=5)

        if not resultados.empty:
            confianza_top = resultados["confianza"].iloc[0]
            mae_aproximado = 1 - confianza_top

            st.metric("✅ Confianza en la mejor coincidencia", f"{confianza_top*100:.2f}%")
            st.metric("❌ Desajuste (MAE estimado)", f"{mae_aproximado:.2f}")

            st.subheader("🔝 Top 5 Recomendaciones")
            st.dataframe(resultados.drop(columns=["confianza"]).reset_index(drop=True), use_container_width=True)

            st.subheader("📊 Similitud de las Ofertas")
            fig, ax = plt.subplots()
            ax.barh(resultados["titulo"], resultados["confianza"], color='skyblue')
            ax.invert_yaxis()
            ax.set_xlabel("Similitud")
            ax.set_title("Nivel de coincidencia con tu perfil")
            st.pyplot(fig)

        else:
            st.warning("No se encontraron coincidencias. Intenta con otro perfil.")
