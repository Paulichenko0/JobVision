import streamlit as st

# Configuración inicial de la app
st.set_page_config(page_title="Explorador de Ofertas IT", layout="wide")

# Importación de módulos
from landing_page import mostrar_landing
from filtros import mostrar_filtros
from tabla_resultados import mostrar_tabla
from analisis_avanzado import mostrar_analisis_avanzado
from recomendador import mostrar_recomendador  # 💡 Aquí ya debe incluir la lógica del formulario y resultados

# Función principal
def main():
    st.sidebar.title("📌 Navegación")
    vista = st.sidebar.radio(
        "Selecciona una sección:",
        ["Inicio", "Ver Ofertas", "Análisis Avanzado", "📈 Predice tu Próximo Trabajo"]
    )

    if vista == "Inicio":
        mostrar_landing()
    elif vista == "Ver Ofertas":
        filtros = mostrar_filtros()
        mostrar_tabla(filtros)
    elif vista == "Análisis Avanzado":
        mostrar_analisis_avanzado()
    elif vista == "📈 Predice tu Próximo Trabajo":
        mostrar_recomendador()

# Punto de entrada
if __name__ == "__main__":
    main()
