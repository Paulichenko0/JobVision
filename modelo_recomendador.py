import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils import cargar_datos_recomendador

# Entrenar el vectorizador directamente al cargar
df_rec = cargar_datos_recomendador()

# Entrenamiento dinámico del preprocesador
preprocessor = ColumnTransformer(transformers=[
    ("titulo", TfidfVectorizer(), "titulo"),
    ("tecnologia", TfidfVectorizer(), "tecnologias_x"),
    ("tipo_puesto", OneHotEncoder(handle_unknown="ignore"), ["tipo_puesto"]),
    ("jornada", OneHotEncoder(handle_unknown="ignore"), ["jornada"]),
    ("remoto", "passthrough", ["es_remoto"])
])

# Entrenamos con el dataset completo (sin 'link')
X_all = preprocessor.fit_transform(df_rec.drop(columns=["link"]))

def recomendar_ofertas(perfil_dict, top_n=5):
    perfil_df = pd.DataFrame([perfil_dict])
    X_user = preprocessor.transform(perfil_df)
    similitudes = cosine_similarity(X_user, X_all).flatten()
    top_idx = similitudes.argsort()[-top_n:][::-1]
    resultados = df_rec.iloc[top_idx].copy()
    resultados["confianza"] = similitudes[top_idx]
    return resultados[["titulo", "tipo_puesto", "tecnologias_x", "link", "confianza"]]

