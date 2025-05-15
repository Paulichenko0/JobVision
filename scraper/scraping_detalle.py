import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time

# Cargar los enlaces del CSV
df = pd.read_csv("C:/Users/pablo/OneDrive/Escritorio/JobVision/scraper/ofertas_tecnoempleo_final.csv")
urls = df["link"].dropna().unique().tolist()

# Scraper robusto con selectores corregidos
def extraer_datos(url):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')

        # Información estructurada
        lista_items = soup.select("li.list-item.clearfix.border-bottom")
        campos = {}
        for item in lista_items:
            clave_tag = item.select_one("span.d-inline-block")
            valor_tag = item.select_one("span.float-end")
            if clave_tag and valor_tag:
                clave = clave_tag.text.strip().lower()
                valor = valor_tag.text.strip()
                campos[clave] = valor

        # Tecnologías
        tecnologias = [a.text.strip() for a in soup.select("span.float-end a")]

        return {
            "url": url,
            "tecnologias": ", ".join(tecnologias),
            "tipo_puesto": campos.get("funciones"),
            "idioma": campos.get("idiomas"),
            "formacion_minima": campos.get("formación mínima"),
            "tipo_contrato": campos.get("tipo contrato"),
            "nivel_profesional": campos.get("nivel profesional"),
            "experiencia": campos.get("experiencia"),
            "jornada": campos.get("jornada"),
            "ubicacion": campos.get("provincia puesto")
        }
    except Exception as e:
        return {
            "url": url,
            "error": str(e)
        }

# Scraping en lote
resultados = [extraer_datos(url) for url in tqdm(urls)]

# Guardar resultados
df_resultado = pd.DataFrame(resultados)
df_resultado.to_csv("ofertas_scrapeadas_todo.csv", index=False)
print("✅ Archivo guardado como ofertas_scrapeadas_todo.csv")
