import streamlit as st
from utils import cargar_datos

def mostrar_filtros():
    df = cargar_datos()
    st.sidebar.header("🔍 Filtros")

    # Empresa (eliminar vacíos y ordenar)
    empresa_sel = st.sidebar.multiselect(
        "Empresa", 
        sorted(df["empresa"].dropna().astype(str).str.strip().unique())
    )

    # Tecnologías (extraer todas y limpiar)
    tecnologias_unicas = sorted(
        set(
            t.strip()
            for ts in df["tecnologias"].dropna()
            for t in ts.split(",")
            if t.strip()
        )
    )
    tecnologias_sel = st.sidebar.multiselect("Tecnología", tecnologias_unicas)

    # Lugar (sin nulos ni espacios vacíos)
    lugar_sel = st.sidebar.multiselect(
        "Lugar", 
        sorted(df["Lugar"].dropna().astype(str).str.strip().unique())
    )

    # Formación mínima (si está disponible)
    formacion_sel = []
    if "formacion_minima" in df.columns:
        formacion_unicas = sorted(df["formacion_minima"].dropna().astype(str).str.strip().unique())
        formacion_sel = st.sidebar.multiselect("Formación Mínima", formacion_unicas)

    # Idioma (si está disponible)
    idioma_sel = []
    if "idioma" in df.columns:
        idioma_unicas = sorted(df["idioma"].dropna().astype(str).str.strip().unique())
        idioma_sel = st.sidebar.multiselect("Idioma", idioma_unicas)

    # Checkboxes
    remoto = st.sidebar.checkbox("Solo 100% remoto")
    hibrido = st.sidebar.checkbox("Solo híbrido (por tipo de empleo)")

    return empresa_sel, tecnologias_sel, lugar_sel, formacion_sel, idioma_sel, remoto, hibrido
