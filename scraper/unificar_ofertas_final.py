import pandas as pd
import re
from bs4 import BeautifulSoup

# Cargar el CSV final limpio actual
df = pd.read_csv("ofertas_tecnoempleo_limpio_final.csv")

# Añadir columna es_hibrido en base a indicios de hibridación en la descripción
def detectar_hibrido(texto):
    if pd.isna(texto):
        return False
    texto = texto.lower()
    return any(palabra in texto for palabra in ["híbrido", "hibrido", "híbrida", "hibrida"])

# Aplicar a la descripción (o podrías aplicarlo a otra columna si prefieres)
df["es_hibrido"] = df["descripcion"].apply(detectar_hibrido)

# Reordenar para dejar es_remoto y es_hibrido juntas
columnas = df.columns.tolist()
if "es_remoto" in columnas and "es_hibrido" in columnas:
    columnas.insert(columnas.index("es_remoto") + 1, columnas.pop(columnas.index("es_hibrido")))
    df = df[columnas]

# Guardar CSV actualizado
df.to_csv("ofertas_tecnoempleo_limpio_con_hibrido.csv", index=False, encoding="utf-8")
print("✅ Archivo actualizado con columna 'es_hibrido': ofertas_tecnoempleo_limpio_con_hibrido.csv")
