import os
import pandas as pd
from bs4 import BeautifulSoup

# Carpeta donde están las páginas HTML descargadas
carpeta = "html_pages"  # Debes tener archivos como: pagina_23.html, pagina_24.html, ...

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

            resultados.append({
                "titulo": titulo_elem.get_text(strip=True) if titulo_elem else None,
                "empresa": empresa_elem.get_text(strip=True) if empresa_elem else None,
                "descripcion": desc_elem.get_text(strip=True) if desc_elem else None,
                "fecha": fecha_elem.get_text(strip=True) if fecha_elem else None,
                "tecnologias": ", ".join([t.get_text(strip=True) for t in tecnologias_elem]),
                "link": titulo_elem["href"] if titulo_elem and titulo_elem.has_attr("href") else None
            })
        except Exception:
            continue

    return resultados

# Procesar páginas 23 a 151
ofertas_totales = []
for pagina in range(23, 28):
    archivo = os.path.join(carpeta, f"pagina_{pagina}.html")
    if not os.path.exists(archivo):
        print(f"⛔ Archivo no encontrado: {archivo}")
        continue

    with open(archivo, encoding="utf-8") as f:
        contenido = f.read()
        ofertas = extraer_ofertas(contenido)
        ofertas_totales.extend(ofertas)
        print(f"✅ Página {pagina} procesada. Ofertas encontradas: {len(ofertas)}")

# Guardar en CSV
df = pd.DataFrame(ofertas_totales)
df.to_csv("ofertas_tecnoempleo_p23_a_p151.csv", index=False, encoding="utf-8")
print(f"✅ Total de ofertas guardadas: {len(df)}")

