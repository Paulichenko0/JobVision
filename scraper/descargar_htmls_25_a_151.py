
import pyautogui
import time

print("Tienes 10 segundos para abrir Chrome, loguearte en Tecnoempleo y dejar el foco en la barra de direcciones.")
time.sleep(10)

pagina_inicio = 25
pagina_fin = 151

for pagina in range(pagina_inicio, pagina_fin + 1):
    url = f"https://www.tecnoempleo.com/ofertas-trabajo/?pagina={pagina}"

    # Navegar a la URL
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.typewrite(url)
    pyautogui.press('enter')
    print(f"🔄 Página {pagina} cargando...")
    time.sleep(7)

    # Guardar la página
    pyautogui.hotkey('ctrl', 's')
    time.sleep(2)

    # Escribir nombre de archivo
    pyautogui.typewrite(f"pagina_{pagina}.html")
    time.sleep(1)

    # Confirmar
    pyautogui.press('enter')
    print(f"✅ Guardada pagina_{pagina}.html")
    time.sleep(4)

print("✅ Descarga de todas las páginas completada.")
