"""
Módulo de análisis de imágenes con OpenAI Vision (GPT-4o-mini)
para la app ¿Puedo comerlo? de Disco Sopa Pitic
"""

import json
import base64
import io
from openai import OpenAI
from PIL import Image


def analizar_empaque(imagen_bytes, api_key):
    """
    Analiza una imagen de un alimento (perecedero o no) usando OpenAI Vision.
    Devuelve dict con producto, fecha, tipo_fecha, daños, confianza, mensaje.
    """
    client = OpenAI(api_key=api_key)

    imagen_b64 = base64.b64encode(imagen_bytes).decode("utf-8")

    prompt = """Eres un experto en seguridad alimentaria. Analiza esta imagen de un alimento, sea no perecedero (con empaque sellado de fábrica) o perecedero (fresco, refrigerado, sin empaque sellado).

Responde ÚNICAMENTE con un JSON válido, sin texto adicional:

{
  "producto": "nombre del producto que ves",
  "tipo_empaque": "uno de: lata, empaque_seco, empaque_flexible, botella, frasco, caja, general, lacteos, carne_pescado, fruta_verdura, panaderia_fresca",
  "fecha": "fecha en formato YYYY-MM-DD o null si no se ve",
  "tipo_fecha": "caducidad o consumo_preferente o null",
  "daños": ["lista de daños visibles: inflada, abombada, oxido, golpe_costura, golpe_cuerpo, roto, perforado, humedad, manchas, moho, insectos, sello_roto, tapa_abombada, agrio, decolorado, textura_pegajosa"],
  "confianza": "alta, media o baja",
  "mensaje": "frase corta en español de máximo 15 palabras"
}

Guía para "tipo_empaque" en perecederos:
- "lacteos": leche, yogurt, queso, crema.
- "carne_pescado": carne, pollo, pescado o mariscos crudos o cocidos.
- "fruta_verdura": fruta o verdura fresca.
- "panaderia_fresca": pan, repostería fresca sin conservadores, o tortillas de tortillería/caseras sin empaque.
Si es un no perecedero, usa la categoría de empaque que corresponda (lata, empaque_seco, empaque_flexible, botella, frasco, caja) o "general" si no encaja en ninguna. Las tortillas empacadas de bolsa de tienda (con fecha impresa) van en "empaque_flexible"."""

    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{imagen_b64}",
                        "detail": "low"
                    }}
                ]
            }],
            max_tokens=500
        )

        texto = respuesta.choices[0].message.content.strip()
        if texto.startswith("```"):
            texto = texto.split("```")[1]
            if texto.startswith("json"):
                texto = texto[4:]
            texto = texto.strip()

        resultado = json.loads(texto)

        for campo in ["producto", "tipo_empaque", "fecha", "tipo_fecha", "daños", "confianza", "mensaje"]:
            if campo not in resultado:
                resultado[campo] = None

        TIPOS_VALIDOS = [
            "lata", "empaque_seco", "empaque_flexible", "botella", "frasco", "caja", "general",
            "lacteos", "carne_pescado", "fruta_verdura", "panaderia_fresca",
        ]
        if resultado.get("tipo_empaque") not in TIPOS_VALIDOS:
            resultado["tipo_empaque"] = "general"

        if not isinstance(resultado.get("daños"), list):
            resultado["daños"] = []

        return {"exito": True, "datos": resultado}

    except json.JSONDecodeError:
        return {"exito": False, "error": "No pude leer la respuesta. Intenta con otra foto más clara.", "datos": None}
    except Exception as e:
        error_msg = str(e)
        if "invalid_api_key" in error_msg or "Incorrect API key" in error_msg:
            return {"exito": False, "error": "API key inválida. Revisa tu clave en los secretos de Streamlit.", "datos": None}
        elif "quota" in error_msg.lower() or "billing" in error_msg.lower():
            return {"exito": False, "error": "Sin crédito disponible en OpenAI. Revisa tu cuenta.", "datos": None}
        else:
            return {"exito": False, "error": f"Error al analizar: {error_msg}", "datos": None}
