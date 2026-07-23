"""
Guarda fotos + el veredicto final del usuario (solo si dio su consentimiento),
para ir armando un dataset con el que a futuro se pueda entrenar un modelo
propio en vez de depender de la API de OpenAI.

IMPORTANTE: en Streamlit Community Cloud el disco es efímero — esta carpeta
se borra en cada redeploy o reinicio de la app. Esto sirve para probar el
flujo de recolección localmente; para que los datos persistan de verdad en
producción, guardar_muestra() debe apuntar a un almacenamiento externo
(un bucket de S3/GCS, una base de datos, etc.) en vez de disco local.
"""

import json
import os
import uuid
from datetime import datetime, timezone

CARPETA_DATOS = "datos_recolectados"


def guardar_muestra(imagen_bytes, extension, metadata):
    """
    Guarda la imagen y sus metadatos (categoría, respuestas del usuario,
    veredicto final, lo que dijo la IA si se usó) como un par de archivos
    con el mismo identificador. Devuelve ese identificador.
    """
    os.makedirs(CARPETA_DATOS, exist_ok=True)

    identificador = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}_{uuid.uuid4().hex[:8]}"
    extension = (extension or "jpg").lstrip(".").lower()

    ruta_imagen = os.path.join(CARPETA_DATOS, f"{identificador}.{extension}")
    with open(ruta_imagen, "wb") as f:
        f.write(imagen_bytes)

    ruta_metadata = os.path.join(CARPETA_DATOS, f"{identificador}.json")
    with open(ruta_metadata, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return identificador
