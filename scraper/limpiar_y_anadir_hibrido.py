
import pandas as pd
import re
from bs4 import BeautifulSoup

# Cargar el CSV original limpio sin 'es_hibrido'
df = pd.read_csv("ofertas_tecnoempleo_final.csv")

# Función para limpiar texto
def limpiar_texto(texto):
    if pd.isna(texto):
        return ""
    texto = BeautifulSoup(str(texto), "html.parser").get_text()
    texto = re.sub(r"[\n\r\t]+", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

# Aplicar limpieza
for col in ["titulo", "empresa", "descripcion", "tecnologias", "tipo_empleo", "fecha_real", "fecha_publicacion"]:
    if col in df.columns:
        df[col] = df[col].astype(str).apply(limpiar_texto)

# Crear columna es_hibrido
def detectar_hibrido(texto):
    if pd.isna(texto):
        return False
    texto = texto.lower()
    return any(palabra in texto for palabra in ["híbrido", "hibrido", "híbrida", "hibrida"])

df["es_hibrido"] = df["descripcion"].apply(detectar_hibrido)

# Reordenar columnas
columnas_ordenadas = [
    "titulo", "empresa", "tipo_empleo", "es_remoto", "es_hibrido", "tecnologias",
    "descripcion", "fecha_real", "fecha_publicacion", "link"
]
df = df[columnas_ordenadas]

# Guardar resultado final
df.to_csv("ofertas_tecnoempleo_limpio_con_hibrido.csv", index=False, encoding="utf-8")
print("✅ Archivo final guardado como 'ofertas_tecnoempleo_limpio_con_hibrido.csv'")
