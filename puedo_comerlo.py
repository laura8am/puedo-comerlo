import streamlit as st
from datetime import date, timedelta

# ─── Configuración de página ───────────────────────────────────────────────
st.set_page_config(
    page_title="¿Puedo comerlo? | Disco Sopa Pitic",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Estilos CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Serif+Display&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #F5E6C8;
    }

    .stApp {
        background-color: #F5E6C8;
    }

    h1, h2, h3 {
        font-family: 'DM Serif Display', serif;
        color: #1B4332;
    }

    .header-block {
        background-color: #1B4332;
        border-radius: 16px;
        padding: 24px 28px 20px 28px;
        margin-bottom: 28px;
        text-align: center;
    }

    .header-title {
        color: #F5E6C8;
        font-family: 'DM Serif Display', serif;
        font-size: 2.2rem;
        margin: 0;
        line-height: 1.2;
    }

    .header-sub {
        color: #A3C4A0;
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
        font-family: 'DM Serif Display', serif;
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
    <div class="header-title">¿Puedo comerlo?</div>
    <div class="header-sub">Descubre si tu alimento todavía es seguro · Disco Sopa Pitic</div>
</div>
""", unsafe_allow_html=True)

# ─── Datos del producto ────────────────────────────────────────────────────
PRODUCTOS = {
    "🥫  Lata (atún, frijoles, vegetales, chiles...)": "lata",
    "🍝  Pasta (spaghetti, macarrón, codito...)": "empaque_seco",
    "🌾  Arroz": "empaque_seco",
    "🌽  Harina o masa": "empaque_seco",
    "🫘  Legumbres secas (frijol, lenteja, garbanzo...)": "empaque_seco",
    "🧴  Aceite o vinagre": "botella",
    "🍅  Salsa, ketchup o aderezo embotellado": "botella",
    "🥣  Cereal o avena": "caja",
    "🍪  Galletas o pan de caja": "empaque_flexible",
    "☕  Café, té o cacao": "empaque_flexible",
    "🧂  Azúcar, sal o especias": "empaque_seco",
    "🥫  Conserva en frasco (mermelada, miel, salsa...)": "frasco",
    "📦  Otro no perecedero": "general",
}

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
}

TIPS_POR_PRODUCTO = {
    "lata": "💡 Las latas sin daño duran mucho más allá de la fecha de consumo preferente. Una lata de 2019 en buen estado puede seguir siendo segura.",
    "empaque_seco": "💡 Guarda arroz, frijol y pasta en recipientes herméticos de vidrio o plástico duro. Duran años en buen estado.",
    "botella": "💡 El aceite, vinagre y la mayoría de salsas embotelladas son seguros meses después de la fecha si el envase está intacto.",
    "frasco": "💡 Las mermeladas y miel son seguros por mucho tiempo si el frasco está bien sellado y sin humedad.",
    "caja": "💡 Los cereales abiertos, guardados en bolsa hermética, duran semanas más allá de la fecha.",
    "empaque_flexible": "💡 Las galletas 'pasadas' de fecha a menudo solo pierden textura (están blandas), no son peligrosas si el empaque estaba cerrado.",
    "general": "💡 La mayoría de los no perecederos siguen siendo seguros después de la fecha si el empaque está en buen estado.",
}

# ─── PASO 1: Producto ──────────────────────────────────────────────────────
st.markdown('<div class="step-label">Paso 1 · ¿Qué tienes?</div>', unsafe_allow_html=True)

with st.container():
    producto_seleccionado = st.selectbox(
        "Elige el tipo de alimento",
        options=list(PRODUCTOS.keys()),
        label_visibility="collapsed"
    )
    tipo_empaque = PRODUCTOS[producto_seleccionado]

st.markdown("")

# ─── PASO 2: Fecha ────────────────────────────────────────────────────────
st.markdown('<div class="step-label">Paso 2 · ¿Qué dice la etiqueta?</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    tipo_fecha = st.radio(
        "Tipo de fecha",
        ["📅 Consumo preferente", "⚠️ Fecha de caducidad"],
        label_visibility="collapsed"
    )
with col2:
    fecha_producto = st.date_input(
        "Fecha en el empaque",
        value=date.today(),
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

# Imágenes de referencia visual (simuladas con HTML)
if tipo_empaque == "lata":
    st.markdown("""
    <div class="ref-img-container">
        <div class="ref-img ref-ok">🟢<br><b>Lata segura</b><br>Sin golpes en costuras<br>Sin óxido perforado<br>Tapa plana</div>
        <div class="ref-img ref-warn">🟡<br><b>Revisar</b><br>Golpe leve en el cuerpo<br>Óxido superficial<br>Sin perforaciones</div>
        <div class="ref-img ref-danger">🔴<br><b>No consumir</b><br>Lata inflada o abombada<br>Óxido con agujeros<br>Golpe en costuras</div>
    </div>
    """, unsafe_allow_html=True)
elif tipo_empaque in ["empaque_seco", "empaque_flexible"]:
    st.markdown("""
    <div class="ref-img-container">
        <div class="ref-img ref-ok">🟢<br><b>Empaque seguro</b><br>Sellado intacto<br>Sin humedad<br>Sin insectos</div>
        <div class="ref-img ref-warn">🟡<br><b>Revisar</b><br>Leve deformación<br>Sin rotura ni humedad</div>
        <div class="ref-img ref-danger">🔴<br><b>No consumir</b><br>Empaque roto<br>Humedad o moho<br>Insectos visibles</div>
    </div>
    """, unsafe_allow_html=True)
elif tipo_empaque in ["botella", "frasco"]:
    st.markdown("""
    <div class="ref-img-container">
        <div class="ref-img ref-ok">🟢<br><b>Frasco/botella seguro</b><br>Tapa bien sellada<br>Sin burbujeo raro<br>Color y olor normal</div>
        <div class="ref-img ref-warn">🟡<br><b>Revisar</b><br>Leve cambio de color<br>Sin rompimiento de sello</div>
        <div class="ref-img ref-danger">🔴<br><b>No consumir</b><br>Tapa abombada<br>Sello roto<br>Olor diferente</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="ref-img-container">
        <div class="ref-img ref-ok">🟢<br><b>Seguro</b><br>Empaque intacto<br>Sin daños visibles</div>
        <div class="ref-img ref-danger">🔴<br><b>No consumir</b><br>Daño visible<br>Humedad o insectos</div>
    </div>
    """, unsafe_allow_html=True)

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

# ─── RESULTADO ────────────────────────────────────────────────────────────
if st.button("🔍 Ver resultado", use_container_width=True, type="primary"):

    hay_danger = any(r and nivel == "danger" for r, nivel, _, _ in respuestas)
    hay_warning = any(r and nivel == "warning" for r, nivel, _, _ in respuestas)
    problemas = [(exp, p) for r, nivel, exp, p in respuestas if r]

    # Lógica de decisión
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
    elif not es_caducidad and dias_diferencia < -365:
        decision = "caution"
    else:
        decision = "safe"

    # Mensaje de días
    if dias_diferencia > 0:
        estado_fecha = f"Faltan {dias_diferencia} días para la fecha indicada."
    elif dias_diferencia == 0:
        estado_fecha = "Hoy es el último día de la fecha indicada."
    else:
        estado_fecha = f"Lleva {abs(dias_diferencia)} días pasado la fecha indicada."

    tip = TIPS_POR_PRODUCTO.get(tipo_empaque, "")

    if decision == "safe":
        st.markdown(f"""
        <div class="result-safe">
            <div class="result-emoji">✅</div>
            <div class="result-title">Puedes comerlo</div>
            <div class="result-reason">{estado_fecha} El empaque está en buen estado y no encontramos señales de riesgo.</div>
            <div class="tip-box">{tip}</div>
        </div>
        """, unsafe_allow_html=True)

    elif decision == "caution":
        razones = "<br>".join([f"• {p}" for _, p in problemas]) if problemas else "• La fecha ya pasó. Revisa bien antes de consumir."
        st.markdown(f"""
        <div class="result-caution">
            <div class="result-emoji">⚠️</div>
            <div class="result-title">Revisa antes de comer</div>
            <div class="result-reason">{estado_fecha}</div>
            <div class="result-reason">{razones}</div>
            <div class="tip-box">{tip}</div>
        </div>
        """, unsafe_allow_html=True)
        if problemas:
            for exp, _ in problemas:
                st.info(exp)

    else:
        razones = "<br>".join([f"• {p}" for _, p in problemas]) if problemas else "• La fecha de caducidad pasó hace más de dos semanas."
        st.markdown(f"""
        <div class="result-danger">
            <div class="result-emoji">🚫</div>
            <div class="result-title">No lo consumas</div>
            <div class="result-reason">{estado_fecha}</div>
            <div class="result-reason">{razones}</div>
            <div class="tip-box">💡 Antes de tirarlo, considera si puede compostarse. ¿Tienes acceso a composta en tu colonia?</div>
        </div>
        """, unsafe_allow_html=True)
        if problemas:
            for exp, _ in problemas:
                st.error(exp)

# ─── Footer ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">
    Disco Sopa Pitic · Hermosillo, Sonora · Proyecto prototipo 2025<br>
    Esta herramienta es orientativa. En caso de duda, no consumas el alimento.
</div>
""", unsafe_allow_html=True)
