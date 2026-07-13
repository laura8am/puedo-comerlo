# ¿Puedo comerlo?

App de [Disco Sopa Pitic](https://www.instagram.com/discosopapitic) (Hermosillo, Sonora) para ayudar a decidir si un alimento todavía es seguro para comer, a partir de su fecha de etiqueta y el estado visible del empaque o del alimento — reduciendo el desperdicio de comida que en realidad todavía está en buen estado.

## Qué hace

1. **Elige el alimento** — no perecedero (lata, pasta, botella, frasco, caja, empaque flexible) o perecedero (lácteos, carne/pescado, fruta/verdura, panadería fresca).
2. **Fecha de la etiqueta** — consumo preferente vs. fecha de caducidad (los perecederos se saltan este paso: casi nunca traen fecha impresa).
3. **Estado del alimento** — un cuestionario de sí/no adaptado a cada categoría (moho, óxido, olor, textura, etc.), con imágenes de referencia. Opcionalmente puedes subir una foto: si hay una `OPENAI_API_KEY` configurada, la IA (GPT-4o-mini vía OpenAI Vision) detecta el producto, la fecha, daños visibles y — para fruta/verdura — una vida útil estimada, y marca automáticamente las casillas que correspondan.
4. **Resultado** — puedes comerlo / revisa antes de comer / no lo consumas, con una explicación y un tip para alargar la vida del producto.

## Correr localmente

```bash
pip install -r requirements.txt
streamlit run puedo_comerlo.py
```

Abre en `http://localhost:8501`.

### Análisis de fotos con IA (opcional)

El análisis de fotos requiere una API key de OpenAI. Sin ella, la app sigue funcionando normalmente (solo se salta el análisis automático y muestra una guía de comparación estática).

Crea `.streamlit/secrets.toml` (no se sube al repo, ver `.gitignore`):

```toml
OPENAI_API_KEY = "sk-..."
```

En Streamlit Community Cloud, esto se configura en **Manage app → Settings → Secrets**.

## Estructura del proyecto

| Archivo | Qué contiene |
|---|---|
| `puedo_comerlo.py` | La UI de Streamlit (los 4 pasos, la subida de foto, el resultado). |
| `logica.py` | Datos y lógica pura sin dependencia de Streamlit: categorías de producto, preguntas por categoría, la lógica de decisión (`decidir`), y los helpers para sanear/traducir lo que devuelve la IA. Separado así para poder probarlo con pruebas unitarias normales. |
| `vision_ia.py` | Llama a OpenAI Vision (GPT-4o-mini) para analizar la foto del alimento. |
| `ilustraciones.py` | Ilustraciones SVG de referencia (🟢/🟡/🔴) para cada categoría. |
| `tests/` | Pruebas unitarias de `logica.py`. |

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Se corren automáticamente en cada push/PR vía GitHub Actions (`.github/workflows/ci.yml`), junto con una verificación de que todos los `.py` compilan.

## Deploy

Desplegado en [Streamlit Community Cloud](https://share.streamlit.io), apuntando a la rama `main` y `puedo_comerlo.py` como archivo principal. Cada push a `main` redespliega automáticamente.

## Aviso

Esta herramienta es orientativa, no un sustituto del criterio propio. En caso de duda, no consumas el alimento.
