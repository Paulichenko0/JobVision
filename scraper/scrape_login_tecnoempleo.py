import time
import os
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ------------------- CARGAR CREDENCIALES -------------------
load_dotenv()
USUARIO = os.getenv("USUARIO_TECNOEMPLEO")
PASSWORD = os.getenv("PASSWORD_TECNOEMPLEO")

# ------------------- CONFIGURAR CHROME INDETECTABLE -------------------
options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(options=options, headless=False)
wait = WebDriverWait(driver, 15)

# ------------------- LOGIN -------------------
driver.get("https://www.tecnoempleo.com/demanda-trabajo-informatica.php")

try:
    wait.until(EC.presence_of_element_located((By.NAME, "e_mail"))).send_keys(USUARIO)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "cmd_acceso").click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Mi cuenta de Candidato')]")))
    print("✅ Login completado. Redirigiendo a página 15...")
    driver.get("https://www.tecnoempleo.com/ofertas-trabajo/?pagina=16")

except Exception as e:
    print("❌ Error durante el login:", e)
    driver.quit()
    exit()

# ------------------- FUNCIÓN DE EXTRACCIÓN -------------------
def extraer_ofertas(soup):
    ofertas = soup.find_all("div", class_="p-3 border rounded mb-3 bg-white")
    resultados = []

    for oferta in ofertas:
        try:
            titulo_elem = oferta.find("h3", class_="fs-5 mb-2")
            empresa_elem = oferta.find("a", class_="text-primary link-muted")
            enlace_elem = oferta.find("h3").find("a")
            descripcion_elem = oferta.find("span", class_="hidden-md-down text-gray-800")
            fecha_elem = oferta.find("span", class_="badge badge-warning ml-1 lead fs--11")

            if not all([titulo_elem, empresa_elem, enlace_elem, descripcion_elem, fecha_elem]):
                continue

            titulo = titulo_elem.get_text(strip=True)
            enlace = enlace_elem["href"]
            empresa = empresa_elem.get_text(strip=True)
            descripcion = descripcion_elem.get_text(strip=True)
            fecha = fecha_elem.get_text(strip=True)

            ubicacion_raw_elem = oferta.find("div", class_="col-12 col-lg-3 text-gray-700 pt-2 text-right hidden-md-down")
            if ubicacion_raw_elem:
                ubicacion_raw = ubicacion_raw_elem.get_text(separator="|", strip=True)
                ubicacion_split = ubicacion_raw.split("|")
                ubicacion = ubicacion_split[0] if len(ubicacion_split) > 0 else ""
                modalidad = ubicacion_split[1] if len(ubicacion_split) > 1 else ""
                tipo = ubicacion_split[2] if len(ubicacion_split) > 2 else ""
            else:
                ubicacion = modalidad = tipo = ""

            tecnologias = [tech.get_text(strip=True) for tech in oferta.find_all("span", class_="badge bg-gray-500 mx-1")]

            resultados.append({
                "titulo": titulo,
                "empresa": empresa,
                "enlace": enlace,
                "ubicacion": ubicacion,
                "modalidad": modalidad,
                "tipo_empleo": tipo,
                "tecnologias": ", ".join(tecnologias),
                "fecha": fecha,
                "descripcion": descripcion
            })

        except Exception as e:
            print("⚠️ Error puntual:", e)
            continue

    return resultados

# ------------------- SCROLL + EXTRACCIÓN -------------------
print("🔄 Scroll forzado...")
for _ in range(5):
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight / 5);")
    time.sleep(1)

time.sleep(3)
soup = BeautifulSoup(driver.page_source, "html.parser")
resultados = extraer_ofertas(soup)

# ------------------- GUARDAR RESULTADOS -------------------
if not resultados:
    print("⛔ Página 15 sigue vacía.")
else:
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(resultados)
    df.to_csv("data/ofertas_tecnoempleo_undetected_p16.csv", index=False, encoding="utf-8")
    print(f"✅ Guardadas {len(df)} ofertas desde la página 15")
    
driver.quit()
