
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Ruta al perfil específico creado manualmente
perfil_usuario = r"C:/Users/pablo/AppData/Local/Google/Chrome/User Data"
perfil_nombre = "Profile 1"  # Nombre del nuevo perfil de Chrome creado

# Configurar Chrome para usar el perfil
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={perfil_usuario}")
chrome_options.add_argument(f"--profile-directory={perfil_nombre}")
chrome_options.add_argument("--start-maximized")

# Iniciar navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Rango de páginas a guardar
pagina_inicio = 20
pagina_fin = 22

for pagina in range(pagina_inicio, pagina_fin + 1):
    url = f"https://www.tecnoempleo.com/ofertas-trabajo/?pagina={pagina}"
    driver.get(url)
    print(f"✅ Página {pagina} cargada.")
    time.sleep(5)  # Esperar que cargue el contenido

    with open(f"pagina_{pagina}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

driver.quit()
print("✅ Finalizado.")
