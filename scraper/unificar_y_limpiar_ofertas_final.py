
import pandas as pd
import re
from bs4 import BeautifulSoup

# Cargar ambos CSVs
df1 = pd.read_csv("ofertas_tecnoempleo.csv")
df2 = pd.read_csv("ofertas_tecnoempleo_25_a_151_completo.csv")

# Unirlos
df = pd.concat([df1, df2], ignore_index=True)

# Eliminar duplicados
df = df.drop_duplicates(subset=["titulo", "empresa", "link"], keep="first")

# Eliminar filas sin campos esenciales
df = df.dropna(subset=["titulo", "empresa", "link"])

# Limpiar texto
def limpiar_texto(texto):
    if pd.isna(texto):
        return ""
    texto = BeautifulSoup(str(texto), "html.parser").get_text()
    texto = re.sub(r"[\n\r\t]+", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

# Aplicar limpieza a columnas clave
for col in ["titulo", "empresa", "descripcion", "tecnologias", "ubicacion", "modalidad", "tipo_empleo"]:
    if col in df.columns:
        df[col] = df[col].astype(str).apply(limpiar_texto)

# Guardar CSV final limpio
df.to_csv("ofertas_tecnoempleo_FINAL.csv", index=False, encoding="utf-8")
print(f"✅ Archivo unificado y limpio guardado: 'ofertas_tecnoempleo_FINAL.csv' con {len(df)} registros.")
