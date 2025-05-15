import streamlit as st
import pandas as pd
import plotly.express as px
from utils import cargar_datos

def mostrar_tabla(filtros):
    empresa_sel, tecnologias_sel, lugar_sel, formacion_sel, idioma_sel, remoto, hibrido = filtros
    df = cargar_datos()

    # Normalizar campos clave
    df["empresa"] = df["empresa"].astype(str).str.strip()
    df["tecnologias"] = df["tecnologias"].astype(str).str.upper()

    # Aplicar filtros
    if empresa_sel:
        df = df[df["empresa"].isin(empresa_sel)]
    if tecnologias_sel:
        df = df[df["tecnologias"].apply(lambda x: any(t in x for t in tecnologias_sel))]
    if lugar_sel:
        df = df[df["Lugar"].isin(lugar_sel)]
    if formacion_sel and "formacion_minima" in df.columns:
        df = df[df["formacion_minima"].isin(formacion_sel)]
    if idioma_sel and "idioma" in df.columns:
        df = df[df["idioma"].isin(idioma_sel)]
    if remoto:
        df = df[df["es_remoto"] == True]
    if hibrido:
        df = df[df["es_tipo_hibrido"] == True]

    df = df.copy()
    df["titulo"] = df["titulo"].str.title()
    df["link"] = df["link"].apply(lambda url: f"[Ver oferta]({url})")

    # Columnas booleanas de categoría profesional (si existen)
    columnas_booleanas = [
        "es_devops", "es_bigdata", "es_consultor", "es_analista",
        "es_programador", "es_tecnico_de_sistemas", "es_jefe_de_proyecto"
    ]
    columnas_booleanas = [col for col in columnas_booleanas if col in df.columns]

    # Crear columna 'categorias'
    df["categorias"] = df[columnas_booleanas].apply(
        lambda row: ", ".join(col.replace("es_", "").replace("_", " ").title() for col in row.index if row[col]),
        axis=1
    ) if columnas_booleanas else ""

    # Columnas visibles
    columnas_visibles = [
        "titulo", "empresa", "categorias", "Lugar", "tecnologias",
        "fecha_publicacion", "link"
    ]
    df_visible = df[columnas_visibles]

    # Paginación
    total_filas = len(df_visible)
    filas_por_pagina = 50
    pagina = st.number_input("Página", min_value=1, max_value=max(1, (total_filas // filas_por_pagina) + 1), step=1)
    inicio = (pagina - 1) * filas_por_pagina
    fin = inicio + filas_por_pagina

    st.subheader("📊 Resultados Filtrados")
    st.write(f"Mostrando {inicio + 1} - {min(fin, total_filas)} de {total_filas} ofertas")
    st.markdown(
        df_visible.iloc[inicio:fin].to_markdown(index=False),
        unsafe_allow_html=True
    )

    # 🔍 Empresas con más ofertas
    st.subheader("🏢 Empresas con más ofertas")
    df_empresas = df[df["empresa"].str.len() > 0].copy()

    if not df_empresas.empty:
        conteo_empresas = df_empresas["empresa"].value_counts().head(10).reset_index()
        conteo_empresas.columns = ["Empresa", "Ofertas"]

        fig = px.bar(
            conteo_empresas,
            x="Ofertas",
            y="Empresa",
            orientation="h",
            title="Top 10 Empresas con más Ofertas Publicadas",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No se encontraron empresas con suficientes datos para graficar.")

    # 📌 Años de experiencia más solicitados
    st.subheader("📌 Años de experiencia más solicitados")
    df_exp = df[df["experiencia"].astype(str).str.strip().str.len() > 0].copy()

    if not df_exp.empty:
        conteo_exp = df_exp["experiencia"].value_counts().head(10).reset_index()
        conteo_exp.columns = ["Experiencia", "Ofertas"]

        fig_exp = px.bar(
            conteo_exp,
            x="Ofertas",
            y="Experiencia",
            orientation="h",
            title="Top 10 Años de Experiencia Requeridos",
            height=400
        )
        st.plotly_chart(fig_exp, use_container_width=True)
    else:
        st.warning("No hay datos válidos de experiencia para graficar.")
