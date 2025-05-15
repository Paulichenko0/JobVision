import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# ✅ Cargar el archivo CSV desde la carpeta 'data'
df = pd.read_csv("data/ofertas_unificadas_definitivo.csv")

# ✅ Obtener todos los enlaces únicos
links = df["link"].dropna().unique().tolist()

# ✅ Función para extraer idioma y formación mínima de cada detalle
def extraer_info_detalle(url):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        detalles = soup.find_all("div", class_="d-flex py-2")

        idioma = None
        formacion = None

        for detalle in detalles:
            textos = detalle.find_all("div")
            if len(textos) >= 2:
                texto = textos[1].get_text(strip=True)
                if texto.startswith("Idiomas:"):
                    idioma = texto.replace("Idiomas:", "").strip()
                elif texto.startswith("Formación Mínima:"):
                    formacion = texto.replace("Formación Mínima:", "").strip()

        return idioma, formacion
    except Exception:
        return None, None

# ✅ Iterar sobre todos los links y recolectar resultados
resultados = []
for url in tqdm(links):
    idioma, formacion = extraer_info_detalle(url)
    resultados.append({
        "link": url,
        "idioma": idioma,
        "formacion_minima": formacion
    })

# ✅ Guardar en archivo final
df_resultado = pd.DataFrame(resultados)
df_resultado.to_csv("data/idioma_formacion_completo.csv", index=False)
