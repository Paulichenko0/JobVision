
import os
import pandas as pd
from bs4 import BeautifulSoup

# Carpeta donde están los archivos descargados
carpeta = r"C:/Users/pablo/Downloads"

def extraer_ofertas(html):
    soup = BeautifulSoup(html, "html.parser")
    resultados = []

    ofertas = soup.find_all("div", class_="p-3 border rounded mb-3 bg-white")
    for oferta in ofertas:
        try:
            titulo_elem = oferta.find("h3", class_="fs-5 mb-2").find("a")
            empresa_elem = oferta.find("a", class_="text-primary link-muted")
            desc_elem = oferta.find("span", class_="hidden-md-down text-gray-800")
            fecha_elem = oferta.find("span", class_="badge badge-warning ml-1 lead fs--11")
            tecnologias_elem = oferta.find_all("span", class_="badge bg-gray-500 mx-1")

            # Ubicación, modalidad, tipo de empleo (en el div de 3 columnas a la derecha)
            ubicacion_div = oferta.find("div", class_="col-12 col-lg-3 text-gray-700 pt-2 text-right hidden-md-down")
            ubicacion = modalidad = tipo_empleo = None
            if ubicacion_div:
                partes = [p.strip() for p in ubicacion_div.get_text(separator="|").split("|")]
                if len(partes) > 0: ubicacion = partes[0]
                if len(partes) > 1: modalidad = partes[1]
                if len(partes) > 2: tipo_empleo = partes[2]

            resultados.append({
                "titulo": titulo_elem.get_text(strip=True) if titulo_elem else None,
                "empresa": empresa_elem.get_text(strip=True) if empresa_elem else None,
                "descripcion": desc_elem.get_text(strip=True) if desc_elem else None,
                "fecha": fecha_elem.get_text(strip=True) if fecha_elem else None,
                "tecnologias": ", ".join([t.get_text(strip=True) for t in tecnologias_elem]),
                "link": titulo_elem["href"] if titulo_elem and titulo_elem.has_attr("href") else None,
                "ubicacion": ubicacion,
                "modalidad": modalidad,
                "tipo_empleo": tipo_empleo
            })
        except Exception:
            continue

    return resultados

# Procesar desde página 25 a 151
ofertas_totales = []
for pagina in range(25, 152):
    archivo = os.path.join(carpeta, f"pagina_{pagina}.html")
    if not os.path.exists(archivo):
        print(f"⛔ Archivo no encontrado: {archivo}")
        continue

    with open(archivo, encoding="utf-8") as f:
        contenido = f.read()
        ofertas = extraer_ofertas(contenido)
        ofertas_totales.extend(ofertas)
        print(f"✅ Página {pagina} procesada. Ofertas encontradas: {len(ofertas)}")

# Guardar CSV completo
df = pd.DataFrame(ofertas_totales)
df.to_csv("ofertas_tecnoempleo_25_a_151_completo.csv", index=False, encoding="utf-8")
print(f"✅ Total ofertas guardadas: {len(df)} en 'ofertas_tecnoempleo_25_a_151_completo.csv'")
