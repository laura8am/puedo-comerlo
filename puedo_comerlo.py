import streamlit as st
from datetime import date
from ilustraciones import get_ilustraciones

try:
    from vision_ia import analizar_empaque
    IA_DISPONIBLE = True
except ImportError:
    IA_DISPONIBLE = False
    def analizar_empaque(img, key):
        return {"exito": False, "error": "Módulo IA no disponible."}

# ─── Configuración de página ───────────────────────────────────────────────
st.set_page_config(
    page_title="¿Puedo comerlo? | Disco Sopa Pitic",
    page_icon="🥫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Estilos CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF;
    }

    .stApp {
        background-color: #FFFFFF;
    }

    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #1B4332;
    }

    .header-block {
        border-radius: 16px;
        padding: 24px 28px 20px 28px;
        margin-bottom: 28px;
        text-align: center;
    }

    .header-title {
        color: #1B4332;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        margin: 0;
        line-height: 1.2;
    }

    .header-sub {
        color: #6B7B6A;
        font-size: 0.95rem;
        margin-top: 6px;
    }

    .step-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        color: #6B7B6A;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 20px 22px;
        margin-bottom: 18px;
        border: 1px solid #E8D9B8;
    }

    .ref-img-container {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 12px;
        margin-bottom: 8px;
    }

    .ref-img {
        flex: 1;
        min-width: 120px;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
        font-size: 0.82rem;
        font-weight: 500;
    }

    .ref-ok {
        background: #D1FAE5;
        border: 2px solid #34D399;
        color: #065F46;
    }

    .ref-warn {
        background: #FEF3C7;
        border: 2px solid #F59E0B;
        color: #92400E;
    }

    .ref-danger {
        background: #FEE2E2;
        border: 2px solid #F87171;
        color: #991B1B;
    }

    .result-safe {
        background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
        border: 2px solid #34D399;
        border-radius: 16px;
        padding: 28px 24px;
        text-align: center;
    }

    .result-caution {
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        border: 2px solid #F59E0B;
        border-radius: 16px;
        padding: 28px 24px;
        text-align: center;
    }

    .result-danger {
        background: linear-gradient(135deg, #FEE2E2, #FECACA);
        border: 2px solid #F87171;
        border-radius: 16px;
        padding: 28px 24px;
        text-align: center;
    }

    .result-emoji {
        font-size: 3.5rem;
        margin-bottom: 8px;
    }

    .result-title {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.8rem;
        margin: 0 0 10px 0;
        color: #1B4332;
    }

    .result-reason {
        font-size: 0.95rem;
        color: #374151;
        margin-bottom: 12px;
        line-height: 1.6;
    }

    .tip-box {
        background: rgba(255,255,255,0.6);
        border-radius: 10px;
        padding: 12px 14px;
        font-size: 0.88rem;
        color: #374151;
        text-align: left;
        margin-top: 10px;
    }

    .diff-box {
        background: #EEF9EE;
        border-left: 4px solid #1B4332;
        border-radius: 0 10px 10px 0;
        padding: 12px 14px;
        font-size: 0.88rem;
        color: #1B4332;
        margin-top: 10px;
        margin-bottom: 6px;
    }

    .days-tag {
        display: inline-block;
        background: #1B4332;
        color: #F5E6C8;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 6px;
    }

    .footer-note {
        text-align: center;
        font-size: 0.78rem;
        color: #9CA3AF;
        margin-top: 32px;
        padding-bottom: 20px;
    }

    .ia-tag {
        display: inline-block;
        background: #1B4332;
        color: #F5E6C8;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        border-radius: 20px;
        padding: 3px 10px;
        margin-bottom: 8px;
    }

    div[data-testid="stCheckbox"] label {
        font-size: 0.92rem !important;
        color: #374151 !important;
    }

    div[data-testid="stSelectbox"] > div {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-block">
    <div class="header-title">🥫 ¿Puedo comerlo?</div>
    <div class="header-sub">Descubre si tu alimento todavía es seguro</div>
</div>
""", unsafe_allow_html=True)

# ─── Datos del producto ────────────────────────────────────────────────────
PRODUCTOS_NO_PERECEDEROS = {
    "🥫  Lata (atún, frijoles, vegetales, chiles...)": "lata",
    "🍝  Pasta (spaghetti, macarrón, codito...)": "empaque_seco",
    "🌾  Arroz": "empaque_seco",
    "🌽  Harina o masa": "empaque_seco",
    "🫘  Legumbres secas (frijol, lenteja, garbanzo...)": "empaque_seco",
    "🧴  Aceite o vinagre": "botella",
    "🍅  Salsa, ketchup o aderezo embotellado": "botella",
    "🥣  Cereal o avena": "caja",
    "🍪  Galletas o pan de caja": "empaque_flexible",
    "🫓  Tortillas empacadas (bolsa de tienda, con fecha)": "empaque_flexible",
    "☕  Café, té o cacao": "empaque_flexible",
    "🧂  Azúcar, sal o especias": "empaque_seco",
    "🥫  Conserva en frasco (mermelada, miel, salsa...)": "frasco",
    "📦  Otro no perecedero": "general",
}

PRODUCTOS_PERECEDEROS = {
    "🥛  Lácteos (leche, yogurt, queso, crema)": "lacteos",
    "🍗  Carne, pollo o pescado": "carne_pescado",
    "🍎  Fruta o verdura fresca": "fruta_verdura",
    "🍞  Pan o panadería fresca": "panaderia_fresca",
    "🫓  Tortillas de tortillería o caseras (sin empaque)": "panaderia_fresca",
}

PRODUCTOS = {**PRODUCTOS_NO_PERECEDEROS, **PRODUCTOS_PERECEDEROS}
CATEGORIAS_PERECEDERAS = set(PRODUCTOS_PERECEDEROS.values())

PREGUNTAS_EMPAQUE = {
    "lata": [
        ("¿La lata está abombada o inflada?", "danger",
         "Señal de bacterias peligrosas (botulismo). No abras ni huelas."),
        ("¿Tiene óxido con agujeros o perforaciones?", "danger",
         "El sellado está comprometido. El contenido puede estar contaminado."),
        ("¿Tiene un golpe fuerte en las costuras (bordes)?", "warning",
         "Los golpes en las costuras pueden romper el sellado hermético."),
        ("¿Huele extraño o a metal al abrirla?", "danger",
         "Un olor diferente al normal indica deterioro o contaminación."),
    ],
    "empaque_seco": [
        ("¿El empaque está roto, rasgado o perforado?", "danger",
         "Un empaque abierto expone el producto a humedad e insectos."),
        ("¿Hay señales de humedad, manchas oscuras o moho?", "danger",
         "La humedad en granos y harinas genera toxinas peligrosas (aflatoxinas)."),
        ("¿Ves insectos, gusanos o sus huellas?", "danger",
         "Indica infestación. El producto no es seguro."),
        ("¿El producto huele rancio o diferente?", "warning",
         "Las grasas de harinas y cereales se oxidan. Puede no ser dañino pero la calidad cayó."),
    ],
    "botella": [
        ("¿La tapa está rota, oxidada o dañada?", "danger",
         "El sellado está comprometido."),
        ("¿El sello de seguridad (plastilina o botón) está roto o levantado?", "danger",
         "Indica que el producto fue abierto o manipulado."),
        ("¿El líquido tiene color, olor o textura diferente al normal?", "warning",
         "Puede indicar deterioro o contaminación."),
        ("¿Hay sedimento inusual o el líquido está turbio cuando no debería?", "warning",
         "Depende del producto: en algunos es normal (vinagre, salsas naturales), en otros no."),
    ],
    "frasco": [
        ("¿La tapa está abombada o hace un ruido diferente al abrirla?", "danger",
         "Señal de fermentación o bacterias. No la consumas."),
        ("¿Hay moho visible en la superficie o el interior?", "danger",
         "En conservas, el moho puede penetrar el producto completo."),
        ("¿El sello de vacío (el botón de la tapa) está levantado?", "danger",
         "Indica que el vacío se rompió y puede estar contaminado."),
        ("¿El producto huele agrio o diferente al normal?", "warning",
         "Puede ser fermentación natural (en algunos productos) o deterioro."),
    ],
    "caja": [
        ("¿La caja está muy húmeda o mojada?", "warning",
         "La humedad puede afectar el cereal interno."),
        ("¿La bolsa interior está rota o abierta?", "danger",
         "El producto quedó expuesto a humedad e insectos."),
        ("¿Hay insectos o señales de infestación?", "danger",
         "Indica contaminación del producto."),
        ("¿El producto tiene un olor extraño o rancio?", "warning",
         "Los cereales con grasa (avena, granola) pueden oxidarse."),
    ],
    "empaque_flexible": [
        ("¿El empaque está perforado o roto?", "danger",
         "El producto quedó expuesto a humedad e insectos."),
        ("¿Hay señales de humedad o el producto está pegajoso?", "warning",
         "La humedad afecta la textura y puede generar moho."),
        ("¿Huele rancio o diferente al normal?", "warning",
         "Las galletas y panes de caja con grasa se oxidan con el tiempo."),
    ],
    "general": [
        ("¿El empaque está roto, perforado o muy dañado?", "danger",
         "El producto quedó expuesto al ambiente."),
        ("¿Hay señales de humedad, moho o insectos?", "danger",
         "Indica deterioro o contaminación."),
        ("¿El producto huele diferente al normal?", "warning",
         "Un olor inusual siempre es señal de revisar."),
    ],
    "lacteos": [
        ("¿Hay grumos o separación anormal en la textura?", "danger",
         "Indica que el lácteo se cortó o fermentó de forma no controlada."),
        ("¿Ves moho (manchas verdes, negras o blancas afelpadas)?", "danger",
         "El moho en lácteos puede producir toxinas peligrosas."),
        ("¿Huele agrio, rancio o diferente al abrirlo?", "danger",
         "Un olor agrio fuera de lo normal indica descomposición."),
        ("¿El empaque está hinchado o el sello roto?", "warning",
         "Puede indicar fermentación por bacterias."),
    ],
    "carne_pescado": [
        ("¿Tiene un olor fuerte, agrio o a amoniaco?", "danger",
         "Señal clara de descomposición bacteriana."),
        ("¿El color cambió a gris, verdoso o muy oscuro?", "danger",
         "Los cambios de color indican deterioro avanzado."),
        ("¿La textura está pegajosa o babosa?", "danger",
         "Indica crecimiento bacteriano en la superficie."),
        ("¿Lleva más de 1-2 días refrigerado sin cocinar ni congelar?", "warning",
         "La carne y el pescado crudos se deben cocinar o congelar pronto."),
    ],
    "fruta_verdura": [
        ("¿Hay moho visible?", "danger",
         "El moho puede haberse extendido más allá de lo visible."),
        ("¿Está muy blanda, líquida o con mal olor?", "danger",
         "Señal de descomposición avanzada."),
        ("¿Tiene manchas oscuras grandes o magulladuras profundas?", "warning",
         "A veces se puede cortar la parte dañada si el resto se ve y huele bien."),
        ("¿Ha pasado ya bastante tiempo desde que la compraste?", "warning",
         "Cada fruta o verdura tiene su propio tiempo de vida útil."),
    ],
    "panaderia_fresca": [
        ("¿Hay moho visible (manchas verdes, blancas o negras)?", "danger",
         "El moho en pan se extiende más allá de lo visible; no cortes y comas el resto."),
        ("¿Huele a alcohol, agrio o raro?", "danger",
         "Indica fermentación no deseada."),
        ("¿Está duro, seco o con textura rara pero sin moho ni mal olor?", "warning",
         "Suele ser solo pérdida de calidad, no necesariamente peligroso."),
    ],
}

# Palabras clave para relacionar cada etiqueta de daño que devuelve la IA con
# las preguntas de Paso 3, y así poder marcar automáticamente las casillas que
# correspondan a lo que la IA detectó en la foto.
DAÑOS_A_PALABRAS_CLAVE = {
    "inflada": ["inflada", "abombada"],
    "abombada": ["abombada", "inflada"],
    "oxido": ["óxido"],
    "golpe_costura": ["costura"],
    "golpe_cuerpo": ["golpe"],
    "roto": ["rota", "roto", "rasgad"],
    "perforado": ["perforad"],
    "humedad": ["húmeda", "humedad", "mojada"],
    "manchas": ["manchas"],
    "moho": ["moho"],
    "insectos": ["insectos", "gusanos", "infestación"],
    "sello_roto": ["sello"],
    "tapa_abombada": ["tapa", "abombada"],
    "agrio": ["agrio", "amoniaco", "alcohol"],
    "decolorado": ["color", "gris", "verdoso", "oscuras", "oscuro"],
    "textura_pegajosa": ["pegajosa", "babosa", "grumos", "textura"],
}

# Texto legible para mostrarle al usuario los daños que detectó la IA
# (las etiquetas que devuelve el modelo son códigos internos en inglés/snake_case).
DAÑOS_ETIQUETAS = {
    "inflada": "inflada",
    "abombada": "abombada",
    "oxido": "óxido",
    "golpe_costura": "golpe en costura",
    "golpe_cuerpo": "golpe en el cuerpo",
    "roto": "roto",
    "perforado": "perforado",
    "humedad": "humedad",
    "manchas": "manchas",
    "moho": "moho",
    "insectos": "insectos",
    "sello_roto": "sello roto",
    "tapa_abombada": "tapa abombada",
    "agrio": "olor agrio",
    "decolorado": "decolorado",
    "textura_pegajosa": "textura pegajosa",
}


def _daño_legible(tag):
    tag_norm = str(tag).strip().lower()
    return DAÑOS_ETIQUETAS.get(tag_norm, tag_norm.replace("_", " "))


def _valor_o_none(valor):
    """La IA a veces devuelve el texto 'null' en vez de un valor vacío real."""
    if isinstance(valor, str) and valor.strip().lower() in ("null", "none", ""):
        return None
    return valor


def _preguntas_a_marcar(tipo_empaque, daños_detectados):
    """Índices de las preguntas de Paso 3 que coinciden con los daños que la IA vio en la foto."""
    preguntas_tipo = PREGUNTAS_EMPAQUE.get(tipo_empaque, PREGUNTAS_EMPAQUE["general"])
    idxs = set()
    for daño in daños_detectados:
        tag = str(_valor_o_none(daño) or "").strip().lower()
        if not tag:
            continue
        palabras_clave = DAÑOS_A_PALABRAS_CLAVE.get(tag, [tag])
        for idx, (pregunta, _, _) in enumerate(preguntas_tipo):
            pregunta_norm = pregunta.lower()
            if any(kw in pregunta_norm for kw in palabras_clave):
                idxs.add(idx)
    return idxs


TIPS_POR_PRODUCTO = {
    "lata": "💡 Las latas sin daño duran mucho más allá de la fecha de consumo preferente. Una lata de 2019 en buen estado puede seguir siendo segura.",
    "empaque_seco": "💡 Guarda arroz, frijol y pasta en recipientes herméticos de vidrio o plástico duro. Duran años en buen estado.",
    "botella": "💡 El aceite, vinagre y la mayoría de salsas embotelladas son seguros meses después de la fecha si el envase está intacto.",
    "frasco": "💡 Las mermeladas y miel son seguros por mucho tiempo si el frasco está bien sellado y sin humedad.",
    "caja": "💡 Los cereales abiertos, guardados en bolsa hermética, duran semanas más allá de la fecha.",
    "empaque_flexible": "💡 Las galletas 'pasadas' de fecha a menudo solo pierden textura (están blandas), no son peligrosas si el empaque estaba cerrado.",
    "general": "💡 La mayoría de los no perecederos siguen siendo seguros después de la fecha si el empaque está en buen estado.",
    "lacteos": "💡 Los lácteos deben mantenerse refrigerados siempre. Si hay duda sobre el olor o la textura, mejor no arriesgarse.",
    "carne_pescado": "💡 La carne y el pescado crudos son de los alimentos más riesgosos. Cocina bien y evita dejarlos a temperatura ambiente.",
    "fruta_verdura": "💡 Muchas frutas y verduras se pueden recuperar cortando la parte dañada, si el resto se ve y huele bien.",
    "panaderia_fresca": "💡 El pan fresco sin conservadores dura pocos días a temperatura ambiente. Congélalo si no lo vas a comer pronto.",
}

# ─── PASO 1: Producto ──────────────────────────────────────────────────────
st.markdown('<div class="step-label">Paso 1 · ¿Qué tienes?</div>', unsafe_allow_html=True)

with st.container():
    OPCIONES_CATEGORIA = ["📦 No perecedero", "🥛 Perecedero"]
    categoria_producto = st.radio(
        "Categoría",
        OPCIONES_CATEGORIA,
        horizontal=True,
        label_visibility="collapsed"
    )
    opciones_producto = PRODUCTOS_PERECEDEROS if categoria_producto == OPCIONES_CATEGORIA[1] else PRODUCTOS_NO_PERECEDEROS
    producto_seleccionado = st.selectbox(
        "Elige el tipo de alimento",
        options=list(opciones_producto.keys()),
        label_visibility="collapsed"
    )
    tipo_empaque = opciones_producto[producto_seleccionado]

es_perecedero_actual = tipo_empaque in CATEGORIAS_PERECEDERAS

st.markdown("")

# ─── Variables IA ────────────────────────────────────────────────────────
# Persistidas en session_state: Streamlit corre todo el script de nuevo en cada
# interacción, así que lo que la IA detecta más abajo (al subir la foto) solo
# puede rellenar los campos de fecha de aquí arriba en el rerun siguiente, no
# en el mismo. Ver el st.rerun() tras guardar el resultado del análisis.
if "ia_datos" not in st.session_state:
    st.session_state.ia_datos = {}

fecha_detectada = st.session_state.ia_datos.get("fecha")
tipo_fecha_detectado = st.session_state.ia_datos.get("tipo_fecha")

# ─── PASO 2: Fecha ────────────────────────────────────────────────────────
# Los perecederos casi nunca traen una fecha de caducidad/consumo preferente
# impresa (son frescos, sin empaque de fábrica), así que este paso se salta
# por completo y la evaluación depende solo del estado del alimento (Paso 3).
es_caducidad = False
dias_diferencia = 0

if es_perecedero_actual:
    st.markdown('<div class="step-label">Paso 2 · Estado del alimento</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="diff-box">
        Los perecederos no suelen traer una fecha de caducidad impresa. Vamos directo a revisar su estado en el siguiente paso.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="step-label">Paso 2 · ¿Qué dice la etiqueta?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        opciones_fecha = ["📅 Consumo preferente", "⚠️ Fecha de caducidad"]
        idx_fecha = 1 if tipo_fecha_detectado == "caducidad" else 0
        tipo_fecha = st.radio(
            "Tipo de fecha",
            opciones_fecha,
            index=idx_fecha,
            label_visibility="collapsed"
        )
    with col2:
        valor_fecha = date.today()
        if fecha_detectada:
            try:
                from datetime import datetime
                valor_fecha = datetime.strptime(fecha_detectada, "%Y-%m-%d").date()
            except Exception:
                pass
        fecha_producto = st.date_input(
            "Fecha en el empaque",
            value=valor_fecha,
            label_visibility="collapsed"
        )

    # Explicación de la diferencia
    es_caducidad = "caducidad" in tipo_fecha.lower()
    hoy = date.today()
    dias_diferencia = (fecha_producto - hoy).days

    if not es_caducidad:
        st.markdown("""
        <div class="diff-box">
            <b>Consumo preferente</b> = el fabricante garantiza la mejor calidad hasta esa fecha.<br>
            Después de ella, el alimento puede seguir siendo <b>seguro</b>, aunque puede cambiar en sabor o textura.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="diff-box" style="border-color: #F97316; background: #FFF7ED;">
            <b>Fecha de caducidad</b> = el alimento puede no ser seguro después de esta fecha.<br>
            A diferencia del consumo preferente, aquí sí importa mucho no pasarla.
        </div>
        """, unsafe_allow_html=True)

st.markdown("")

# ─── PASO 3: Estado del empaque ───────────────────────────────────────────
st.markdown('<div class="step-label">Paso 3 · ¿Cómo está el empaque?</div>', unsafe_allow_html=True)

# ─── Subida de foto ────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#FFFFFF; border-radius:14px; padding:16px 18px; border:2px dashed #A3C4A0; margin-bottom:16px; text-align:center;">
    <div style="font-size:2rem; margin-bottom:4px;">📷</div>
    <div style="font-weight:600; color:#1B4332; font-size:0.95rem;">Toma una foto de tu empaque</div>
    <div style="color:#6B7B6A; font-size:0.82rem; margin-top:4px;">Coloca el empaque en una superficie plana con buena luz y sube la foto aquí</div>
</div>
""", unsafe_allow_html=True)

foto_empaque = st.file_uploader(
    "Sube la foto de tu empaque",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed",
    help="Toma la foto con buena luz. Enfoca en las costuras, la tapa y cualquier área dañada."
)

if foto_empaque is not None:
    img_bytes = foto_empaque.getvalue()
    foto_id = f"{foto_empaque.name}_{foto_empaque.size}"

    st.markdown('<div class="step-label">Tu empaque</div>', unsafe_allow_html=True)
    col_foto, col_ref = st.columns([1, 1])
    with col_foto:
        st.image(img_bytes, caption="Tu empaque", use_container_width=True)

    ia_key = None
    try:
        ia_key = st.secrets.get("OPENAI_API_KEY", None)
    except Exception:
        pass

    if ia_key:
        if st.session_state.get("ia_foto_id") != foto_id:
            with col_ref:
                with st.spinner("Analizando..."):
                    ia_resultado = analizar_empaque(img_bytes, ia_key)
            if ia_resultado and ia_resultado.get("exito"):
                datos = ia_resultado["datos"]
                datos["producto"] = _valor_o_none(datos.get("producto"))
                datos["fecha"] = _valor_o_none(datos.get("fecha"))
                datos["tipo_fecha"] = _valor_o_none(datos.get("tipo_fecha"))
                datos["vida_util"] = _valor_o_none(datos.get("vida_util"))
                daños_detectados = [d for d in (datos.get("daños") or []) if _valor_o_none(d)]
                datos["daños"] = daños_detectados

                for idx in _preguntas_a_marcar(tipo_empaque, daños_detectados):
                    st.session_state[f"chk_{tipo_empaque}_{idx}"] = True

                st.session_state.ia_datos = datos
                st.session_state.ia_foto_id = foto_id
                st.rerun()
            else:
                with col_ref:
                    err = ia_resultado.get("error", "Error") if ia_resultado else "Error al analizar"
                    st.warning(err)
        else:
            d = st.session_state.ia_datos
            producto_detectado = d.get("producto")
            daños_ia = d.get("daños", [])
            confianza = d.get("confianza", "media")
            tipo_detectado = d.get("tipo_empaque")
            vida_util = d.get("vida_util")

            aviso_categoria = ""
            if tipo_detectado and tipo_detectado != tipo_empaque:
                if tipo_detectado in CATEGORIAS_PERECEDERAS and tipo_empaque not in CATEGORIAS_PERECEDERAS:
                    aviso_categoria = '<br><span style="color:#9A3412;">💡 Parece perecedero — cambia a "🥛 Perecedero" en el Paso 1 para preguntas más precisas.</span>'
                elif tipo_detectado not in CATEGORIAS_PERECEDERAS and tipo_empaque in CATEGORIAS_PERECEDERAS:
                    aviso_categoria = '<br><span style="color:#9A3412;">💡 Parece no perecedero — cambia a "📦 No perecedero" en el Paso 1 para preguntas más precisas.</span>'

            # Los perecederos no tienen fecha (Paso 2 se salta para ellos), así
            # que la línea de fecha no aplica; para fruta_verdura mostramos en
            # su lugar la vida útil típica que estimó la IA para ese producto.
            if tipo_detectado in CATEGORIAS_PERECEDERAS:
                linea_fecha = f"🕒 {vida_util}<br>" if vida_util else ""
            else:
                linea_fecha = ("📅 " + fecha_detectada if fecha_detectada else "📅 Fecha no visible") + "<br>"

            with col_ref:
                st.markdown(f"""
                <div style="background:#F0FDF4; border-radius:10px; padding:12px; font-size:0.82rem; color:#065F46; height:100%;">
                    <span class="ia-tag">IA</span><br>
                    <b>{producto_detectado or 'No identificado'}</b><br>
                    {linea_fecha}
                    {"⚠️ " + ", ".join(_daño_legible(d) for d in daños_ia) if daños_ia else "✅ Sin daños visibles"}<br>
                    <span style="color:#6B7B6A;font-size:0.75rem;">Confianza: {confianza}</span>{aviso_categoria}
                </div>
                """, unsafe_allow_html=True)
    else:
        with col_ref:
            st.markdown("""
            <div style="background:#F0FDF4; border-radius:10px; padding:12px; font-size:0.82rem; color:#065F46; height:100%;">
                <b>Compara con la guía de abajo ↓</b><br><br>
                Mira tu foto y busca:<br>
                🔍 ¿Hay golpes, óxido o hinchazón?<br>
                🔍 ¿El sellado está intacto?<br>
                🔍 ¿Hay humedad, manchas o insectos?
            </div>
            """, unsafe_allow_html=True)
    st.markdown("")

# Imágenes de referencia visual (simuladas con HTML)
st.markdown(get_ilustraciones(tipo_empaque), unsafe_allow_html=True)

# Checkboxes de estado
preguntas = PREGUNTAS_EMPAQUE.get(tipo_empaque, PREGUNTAS_EMPAQUE["general"])
respuestas = []

if "info_visible" not in st.session_state:
    st.session_state.info_visible = set()

for idx, (pregunta, nivel, explicacion) in enumerate(preguntas):
    info_key = f"{tipo_empaque}_{idx}"
    col_check, col_info = st.columns([0.85, 0.15])
    with col_check:
        resp = st.checkbox(pregunta, key=f"chk_{info_key}")
    with col_info:
        if st.button("?", key=f"info_{info_key}", help=explicacion):
            if info_key in st.session_state.info_visible:
                st.session_state.info_visible.discard(info_key)
            else:
                st.session_state.info_visible.add(info_key)
    if info_key in st.session_state.info_visible:
        st.caption(f"ℹ️ {explicacion}")
    respuestas.append((resp, nivel, explicacion, pregunta))

st.markdown("")

# ─── PASO 4: Resultado ─────────────────────────────────────────────────────
st.markdown('<div class="step-label">Paso 4 · Obtén tu resultado</div>', unsafe_allow_html=True)

if st.button("🔍 Ver resultado", use_container_width=True, type="primary"):

    hay_danger = any(r and nivel == "danger" for r, nivel, _, _ in respuestas)
    hay_warning = any(r and nivel == "warning" for r, nivel, _, _ in respuestas)
    problemas = [(exp, p) for r, nivel, exp, p in respuestas if r]

    # Lógica de decisión
    # Los perecederos (es_perecedero_actual) se saltan el Paso 2, así que
    # es_caducidad queda en False y dias_diferencia en 0: la decisión depende
    # solo de las respuestas del Paso 3 (hay_danger / hay_warning).
    if hay_danger:
        decision = "danger"
    elif hay_warning and es_caducidad and dias_diferencia < -30:
        decision = "danger"
    elif hay_warning:
        decision = "caution"
    elif es_caducidad and dias_diferencia < -14:
        decision = "caution"
    elif es_caducidad and dias_diferencia < 0:
        decision = "caution"
    elif not es_perecedero_actual and not es_caducidad and dias_diferencia < -365:
        decision = "caution"
    else:
        decision = "safe"

    # Mensaje de días (los perecederos no tienen fecha, así que no aplica)
    if es_perecedero_actual:
        estado_fecha = ""
    elif dias_diferencia > 0:
        estado_fecha = f"Faltan {dias_diferencia} días para la fecha indicada."
    elif dias_diferencia == 0:
        estado_fecha = "Hoy es el último día de la fecha indicada."
    else:
        estado_fecha = f"Lleva {abs(dias_diferencia)} días pasado la fecha indicada."

    tip = TIPS_POR_PRODUCTO.get(tipo_empaque, "")
    fila_estado_fecha = f'<div class="result-reason">{estado_fecha}</div>' if estado_fecha else ""

    if decision == "safe":
        razon_safe = f"{estado_fecha} El empaque está en buen estado y no encontramos señales de riesgo." if estado_fecha else "No encontramos señales de riesgo en su estado."
        st.markdown(f"""
        <div class="result-safe">
            <div class="result-emoji">✅</div>
            <div class="result-title">Puedes comerlo</div>
            <div class="result-reason">{razon_safe}</div>
            <div class="tip-box">{tip}</div>
        </div>
        """, unsafe_allow_html=True)

    elif decision == "caution":
        razones = "<br>".join([f"• {exp}" for exp, _ in problemas]) if problemas else "• La fecha ya pasó. Revisa bien antes de consumir."
        st.markdown(f"""
        <div class="result-caution">
            <div class="result-emoji">⚠️</div>
            <div class="result-title">Revisa antes de comer</div>
            {fila_estado_fecha}
            <div class="result-reason">{razones}</div>
            <div class="tip-box">{tip}</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        razones = "<br>".join([f"• {exp}" for exp, _ in problemas]) if problemas else "• La fecha de caducidad pasó hace más de dos semanas."
        st.markdown(f"""
        <div class="result-danger">
            <div class="result-emoji">🚫</div>
            <div class="result-title">No lo consumas</div>
            {fila_estado_fecha}
            <div class="result-reason">{razones}</div>
            <div class="tip-box">💡 Antes de tirarlo, considera si puede compostarse. ¿Tienes acceso a composta en tu colonia?</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">
    Disco Sopa Pitic · Hermosillo, Sonora · Proyecto prototipo 2026<br>
    Esta herramienta es orientativa. En caso de duda, no consumas el alimento.
</div>
""", unsafe_allow_html=True)
