"""
Módulo de análisis de imágenes con OpenAI Vision (GPT-4o-mini)
para la app ¿Puedo comerlo? de Disco Sopa Pitic
"""

import json
import base64
from openai import (
    OpenAI,
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
    BadRequestError,
    APIStatusError,
)
from logica import valor_o_none

TIMEOUT_SEGUNDOS = 30


def analizar_empaque(imagen_bytes, api_key):
    """
    Analiza una imagen de un alimento (perecedero o no) usando OpenAI Vision.
    Devuelve dict con producto, fecha, tipo_fecha, daños, confianza, mensaje.
    """
    client = OpenAI(api_key=api_key, timeout=TIMEOUT_SEGUNDOS)

    imagen_b64 = base64.b64encode(imagen_bytes).decode("utf-8")

    prompt = """Eres un experto en seguridad alimentaria. Analiza esta imagen. Primero determina si lo que ves es realmente un alimento (comida o bebida) — no un objeto, utensilio, planta, mascota, persona, etc.

"es_alimento" es OBLIGATORIO y debe ser literalmente el booleano true o false — nunca null ni omitirlo. Si tienes cualquier duda de que sea comida, responde false.

Responde ÚNICAMENTE con un JSON válido, sin texto adicional:

{
  "es_alimento": true o false (obligatorio, nunca null),
  "producto": "nombre de lo que ves, sea alimento u objeto",
  "tipo_empaque": "uno de: lata, empaque_seco, empaque_flexible, botella, frasco, caja, general, lacteos, carne_pescado, fruta_verdura, panaderia_fresca (usa 'general' si es_alimento es false)",
  "fecha": "fecha en formato YYYY-MM-DD o null si no se ve",
  "tipo_fecha": "caducidad o consumo_preferente o null",
  "daños": ["lista de daños visibles: inflada, abombada, oxido, golpe_costura, golpe_cuerpo, roto, perforado, humedad, manchas, moho, insectos, sello_roto, tapa_abombada, agrio, decolorado, textura_pegajosa"],
  "vida_util": "para fruta_verdura: estimado típico de vida útil a temperatura ambiente o refrigerada para ESE producto específico, ej. 'Plátano: 3-5 días a temperatura ambiente' o null si tipo_empaque no es fruta_verdura",
  "confianza": "alta, media o baja",
  "mensaje": "frase corta en español de máximo 15 palabras"
}

Si "es_alimento" es false, deja "daños" como una lista vacía y el resto de los campos que no apliquen en null — no evalúes seguridad ni inventes daños para algo que no es comida.

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

        for campo in ["es_alimento", "producto", "tipo_empaque", "fecha", "tipo_fecha", "daños", "vida_util", "confianza", "mensaje"]:
            if campo not in resultado:
                resultado[campo] = None

        # Estricto a propósito: solo seguimos si la IA confirmó explícitamente
        # que es un alimento. Si no contestó ese campo, lo dejó en null, o dijo
        # que no, lo tratamos como "no es comida" — es preferible rechazar de
        # más a que un objeto cualquiera termine evaluado como "seguro".
        if resultado.get("es_alimento") is not True:
            objeto = valor_o_none(resultado.get("producto")) or "lo que subiste"
            return {"exito": False, "error": f"Esto no parece ser un alimento ({objeto}). Sube una foto de tu comida.", "datos": None}

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
    except AuthenticationError:
        return {"exito": False, "error": "API key inválida. Revisa tu clave en los secretos de Streamlit.", "datos": None}
    except RateLimitError:
        return {"exito": False, "error": "Se alcanzó el límite de uso de OpenAI (o no hay crédito disponible). Espera un momento o revisa tu cuenta.", "datos": None}
    except APITimeoutError:
        return {"exito": False, "error": "La IA tardó demasiado en responder. Intenta de nuevo.", "datos": None}
    except APIConnectionError:
        return {"exito": False, "error": "No se pudo conectar con OpenAI. Revisa tu conexión a internet e intenta de nuevo.", "datos": None}
    except BadRequestError:
        return {"exito": False, "error": "La foto no se pudo procesar (puede ser muy pesada o un formato no soportado). Intenta con otra.", "datos": None}
    except APIStatusError as e:
        return {"exito": False, "error": f"El servidor de OpenAI respondió con un error ({e.status_code}). Intenta más tarde.", "datos": None}
    except Exception as e:
        return {"exito": False, "error": f"Error al analizar: {e}", "datos": None}
