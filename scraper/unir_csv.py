import pandas as pd

# Cargar ambos CSVs
df_base = pd.read_csv("C:/Users/pablo/OneDrive/Escritorio/JobVision/scraper/ofertas_final_optimizado.csv")
df_scrapeado = pd.read_csv("C:/Users/pablo/OneDrive/Escritorio/JobVision/scraper/ofertas_scrapeadas_todo.csv")

# Renombrar columna para poder hacer el merge
df_scrapeado.rename(columns={"url": "link"}, inplace=True)

# Unir los dos datasets por la columna 'link'
df_unido = pd.merge(df_base, df_scrapeado, on="link", how="left")

# Guardar resultado
df_unido.to_csv("C:/Users/pablo/OneDrive/Escritorio/JobVision/scraper/ofertas_unificadas_final.csv", index=False)
print("✅ CSV unido guardado como 'ofertas_unificadas_final.csv'")
