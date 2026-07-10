import streamlit as st
from datetime import date
from vision_ia import analizar_empaque

st.set_page_config(
    page_title="¿Puedo comerlo?",
    page_icon="🥫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #FFFFFF;
}

.stApp { background-color: #FFFFFF; }

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 640px;
}

h1, h2, h3 { color: #000000; }

/* Header */
.header {
    border-bottom: 2px solid #000;
    padding-bottom: 20px;
    margin-bottom: 40px;
}
.header-eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 6px;
}
.header-title {
    font-size: 2.6rem;
    font-weight: 900;
    color: #000;
    line-height: 1;
    margin: 0;
}

/* Step label */
.step {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 8px;
    margin-top: 32px;
}

/* Upload zone */
.upload-zone {
    border: 1.5px solid #000;
    padding: 28px 20px;
    text-align: center;
    margin-bottom: 16px;
    cursor: pointer;
}
.upload-icon { font-size: 1.8rem; margin-bottom: 6px; }
.upload-title { font-weight: 700; font-size: 0.95rem; color: #000; }
.upload-sub { font-size: 0.78rem; color: #666; margin-top: 4px; }

/* IA result tag */
.ia-tag {
    display: inline-block;
    background: #000;
    color: #fff;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    padding: 3px 10px;
    margin-bottom: 8px;
}

/* Fecha diff box */
.diff-box {
    border-left: 3px solid #000;
    padding: 10px 14px;
    font-size: 0.84rem;
    color: #333;
    background: #f8f8f8;
    margin: 12px 0;
    line-height: 1.5;
}

/* Ref images placeholder */
.ref-row {
    display: flex;
    gap: 10px;
    margin: 14px 0;
}
.ref-card {
    flex: 1;
    border: 1.5px solid #000;
    padding: 14px 8px;
    text-align: center;
    font-size: 0.75rem;
    font-weight: 600;
    color: #000;
}
.ref-card-warn { border-color: #000; background: #fffbe6; }
.ref-card-danger { border-color: #000; background: #fff5f5; }

/* Results */
.result-box {
    padding: 28px 24px;
    margin-top: 20px;
    border: 2px solid #000;
}
.result-safe { border-color: #000; background: #f0fff4; }
.result-caution { border-color: #000; background: #fffbe6; }
.result-danger { border-color: #000; background: #fff5f5; }

.result-verdict {
    font-size: 2rem;
    font-weight: 900;
    color: #000;
    line-height: 1;
    margin-bottom: 10px;
    text-transform: uppercase;
}
.result-body {
    font-size: 0.88rem;
    color: #333;
    line-height: 1.6;
    margin-bottom: 12px;
}
.result-tip {
    font-size: 0.8rem;
    color: #555;
    border-top: 1px solid #ddd;
    padding-top: 10px;
    margin-top: 10px;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #e5e5e5;
    margin: 8px 0 16px 0;
}

/* Button override */
.stButton > button {
    background: #000 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 0 !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 14px 24px !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #222 !important;
}

/* Radio y selectbox */
div[data-testid="stRadio"] label { font-size: 0.9rem !important; color: #000 !important; }
div[data-testid="stCheckbox"] label { font-size: 0.88rem !important; color: #111 !important; }

/* Footer */
.footer {
    border-top: 1px solid #e5e5e5;
    padding-top: 16px;
    margin-top: 40px;
    font-size: 0.72rem;
    color: #aaa;
    text-align: center;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
    <div class="header-eyebrow">Disco Sopa Pitic · Hermosillo, Sonora</div>
    <div class="header-title">¿Puedo<br>comerlo?</div>
</div>
""", unsafe_allow_html=True)

# ── DATOS ─────────────────────────────────────────────────────────────────
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
    "🫙  Conserva en frasco (mermelada, miel, salsa...)": "frasco",
    "📦  Otro no perecedero": "general",
}

PREGUNTAS = {
    "lata": [
        ("¿Está abombada o inflada?", "danger", "Señal de bacterias peligrosas (botulismo)."),
        ("¿Tiene óxido con perforaciones?", "danger", "El sellado está comprometido."),
        ("¿Golpe fuerte en las costuras (bordes)?", "warning", "Puede romper el sellado hermético."),
        ("¿Huele extraño al abrirla?", "danger", "Olor diferente indica deterioro."),
    ],
    "empaque_seco": [
        ("¿El empaque está roto o perforado?", "danger", "Expone el producto a humedad e insectos."),
        ("¿Hay humedad, manchas oscuras o moho?", "danger", "Genera toxinas peligrosas (aflatoxinas)."),
        ("¿Ves insectos o huellas de infestación?", "danger", "El producto está contaminado."),
        ("¿Huele rancio o diferente?", "warning", "Las grasas de harinas y cereales se oxidan."),
    ],
    "empaque_flexible": [
        ("¿El empaque está perforado o roto?", "danger", "Producto expuesto a humedad e insectos."),
        ("¿Hay humedad o el producto está pegajoso?", "warning", "Puede generar moho."),
        ("¿Huele rancio o diferente?", "warning", "Las grasas de galletas se oxidan con el tiempo."),
    ],
    "botella": [
        ("¿La tapa está rota u oxidada?", "danger", "Sellado comprometido."),
        ("¿El sello de seguridad está roto?", "danger", "Producto fue abierto o manipulado."),
        ("¿El líquido tiene color u olor diferente?", "warning", "Puede indicar deterioro."),
        ("¿Hay sedimento inusual o turbidez?", "warning", "Depende del producto, revisa."),
    ],
    "frasco": [
        ("¿La tapa está abombada?", "danger", "Señal de fermentación o bacterias."),
        ("¿Hay moho visible?", "danger", "En conservas, el moho penetra todo."),
        ("¿El botón de la tapa está levantado?", "danger", "El vacío se rompió."),
        ("¿Huele agrio o diferente?", "warning", "Puede ser fermentación o deterioro."),
    ],
    "caja": [
        ("¿La caja está muy húmeda?", "warning", "Afecta el contenido interno."),
        ("¿La bolsa interior está abierta o rota?", "danger", "Expuesto a humedad e insectos."),
        ("¿Hay insectos o señales de infestación?", "danger", "Producto contaminado."),
        ("¿Huele rancio?", "warning", "Cereales con grasa se oxidan."),
    ],
    "general": [
        ("¿El empaque está roto o muy dañado?", "danger", "Expuesto al ambiente."),
        ("¿Hay humedad, moho o insectos?", "danger", "Deterioro o contaminación."),
        ("¿Huele diferente al normal?", "warning", "Señal de alerta."),
    ],
}

TIPS = {
    "lata": "Las latas sin daño duran mucho más allá de la fecha indicada.",
    "empaque_seco": "Guarda arroz, frijol y pasta en recipientes herméticos de vidrio. Duran años.",
    "empaque_flexible": "Galletas 'pasadas' solo pierden textura, no son peligrosas si el empaque estaba cerrado.",
    "botella": "Aceite y vinagre son seguros meses después si el envase está intacto.",
    "frasco": "Mermelada y miel son seguros por mucho tiempo con frasco bien sellado.",
    "caja": "Cereales abiertos, en bolsa hermética, duran semanas más.",
    "general": "La mayoría de los no perecederos son seguros si el empaque está en buen estado.",
}

# ── PASO 1 ────────────────────────────────────────────────────────────────
st.markdown('<div class="step">Paso 1 · ¿Qué tienes?</div>', unsafe_allow_html=True)
producto_sel = st.selectbox("Producto", list(PRODUCTOS.keys()), label_visibility="collapsed")
tipo_empaque = PRODUCTOS[producto_sel]

# ── Variables IA ──────────────────────────────────────────────────────────
ia_resultado = None
producto_detectado = None
fecha_detectada = None
tipo_fecha_detectado = None

# ── PASO 2 ────────────────────────────────────────────────────────────────
st.markdown('<div class="step">Paso 2 · ¿Qué dice la etiqueta?</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    es_caducidad_idx = 1 if tipo_fecha_detectado == "caducidad" else 0
    tipo_fecha = st.radio(
        "Tipo",
        ["Consumo preferente", "Fecha de caducidad"],
        index=es_caducidad_idx,
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
    fecha_producto = st.date_input("Fecha", value=valor_fecha, label_visibility="collapsed")

es_caducidad = "caducidad" in tipo_fecha.lower()
hoy = date.today()
dias = (fecha_producto - hoy).days

if not es_caducidad:
    st.markdown('<div class="diff-box"><b>Consumo preferente</b> — el fabricante garantiza calidad hasta esa fecha. Después puede seguir siendo <b>seguro</b>, aunque cambie en sabor o textura.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="diff-box"><b>Fecha de caducidad</b> — después de esta fecha el alimento puede no ser seguro. A diferencia del consumo preferente, aquí sí importa no pasarla.</div>', unsafe_allow_html=True)

# ── PASO 3 ────────────────────────────────────────────────────────────────
st.markdown('<div class="step">Paso 3 · ¿Cómo está el empaque?</div>', unsafe_allow_html=True)

st.markdown("""
<div class="upload-zone">
    <div class="upload-icon">📷</div>
    <div class="upload-title">Sube una foto de tu empaque</div>
    <div class="upload-sub">Superficie plana · buena luz · enfoca la fecha y el estado</div>
</div>
""", unsafe_allow_html=True)

foto = st.file_uploader("Foto", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")

if foto is not None:
    img_bytes = foto.read()
    col_img, col_ia = st.columns([1,1])
    with col_img:
        st.image(img_bytes, use_container_width=True)

    # Análisis IA
    ia_key = None
    try:
        ia_key = st.secrets.get("OPENAI_API_KEY", None)
    except Exception:
        pass

    if ia_key:
        with col_ia:
            with st.spinner("Analizando..."):
                ia_resultado = analizar_empaque(img_bytes, ia_key)

        if ia_resultado and ia_resultado.get("exito"):
            d = ia_resultado["datos"]
            producto_detectado = d.get("producto")
            fecha_detectada = d.get("fecha")
            tipo_fecha_detectado = d.get("tipo_fecha")
            daños_ia = d.get("daños", [])
            confianza = d.get("confianza", "media")

            with col_ia:
                st.markdown(f"""
                <div style="padding:14px;background:#f8f8f8;font-size:0.82rem;color:#111;line-height:1.7;">
                    <span class="ia-tag">IA</span><br>
                    <b>{producto_detectado or 'No identificado'}</b><br>
                    {"📅 " + fecha_detectada if fecha_detectada else "📅 Fecha no visible"}<br>
                    {"⚠️ " + ", ".join(daños_ia) if daños_ia else "✅ Sin daños visibles"}<br>
                    <span style="color:#999;font-size:0.75rem;">Confianza: {confianza}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            with col_ia:
                err = ia_resultado.get("error","Error") if ia_resultado else "Error al analizar"
                st.warning(err)
    else:
        with col_ia:
            st.markdown("""
            <div style="padding:14px;background:#f8f8f8;font-size:0.82rem;color:#666;line-height:1.6;">
                Compara con la guía de abajo:<br><br>
                ¿Golpes, óxido o hinchazón?<br>
                ¿Sellado intacto?<br>
                ¿Humedad, manchas o insectos?
            </div>
            """, unsafe_allow_html=True)

# Imágenes de referencia (placeholder para tus Canva)
st.markdown(f"""
<div class="ref-row">
    <div class="ref-card">🟢<br>SEGURO<br><span style="font-weight:300;font-size:0.7rem;">Sin daños visibles</span></div>
    <div class="ref-card ref-card-warn">🟡<br>REVISAR<br><span style="font-weight:300;font-size:0.7rem;">Daño menor</span></div>
    <div class="ref-card ref-card-danger">🔴<br>NO CONSUMIR<br><span style="font-weight:300;font-size:0.7rem;">Daño grave</span></div>
</div>
<div style="font-size:0.72rem;color:#999;margin-bottom:8px;">← Aquí irán tus imágenes de Canva</div>
""", unsafe_allow_html=True)

preguntas = PREGUNTAS.get(tipo_empaque, PREGUNTAS["general"])
respuestas = []
for pregunta, nivel, exp in preguntas:
    r = st.checkbox(pregunta, help=exp)
    respuestas.append((r, nivel, exp, pregunta))

st.markdown("")

# ── RESULTADO ─────────────────────────────────────────────────────────────
if st.button("Ver resultado"):
    hay_danger = any(r and n == "danger" for r, n, _, _ in respuestas)
    hay_warning = any(r and n == "warning" for r, n, _, _ in respuestas)
    problemas = [(e, p) for r, n, e, p in respuestas if r]

    if hay_danger:
        decision = "danger"
    elif hay_warning and es_caducidad and dias < -30:
        decision = "danger"
    elif hay_warning or (es_caducidad and dias < 0):
        decision = "caution"
    elif not es_caducidad and dias < -365:
        decision = "caution"
    else:
        decision = "safe"

    if dias > 0:
        estado_fecha = f"Faltan {dias} días para la fecha indicada."
    elif dias == 0:
        estado_fecha = "Hoy es el último día de la fecha indicada."
    else:
        estado_fecha = f"Lleva {abs(dias)} días pasado la fecha indicada."

    tip = TIPS.get(tipo_empaque, "")
    razones = " · ".join([p for _, p in problemas]) if problemas else ""

    if decision == "safe":
        st.markdown(f"""
        <div class="result-box result-safe">
            <div class="result-verdict">✓ Puedes comerlo</div>
            <div class="result-body">{estado_fecha} El empaque está en buen estado.</div>
            <div class="result-tip">{tip}</div>
        </div>
        """, unsafe_allow_html=True)
    elif decision == "caution":
        st.markdown(f"""
        <div class="result-box result-caution">
            <div class="result-verdict">⚠ Revisa bien</div>
            <div class="result-body">{estado_fecha}{f" {razones}" if razones else ""}</div>
            <div class="result-tip">{tip}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-box result-danger">
            <div class="result-verdict">✕ No lo consumas</div>
            <div class="result-body">{estado_fecha}{f" {razones}" if razones else ""}</div>
            <div class="result-tip">💡 Antes de tirar, considera si puede compostarse.</div>
        </div>
        """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    DISCO SOPA PITIC · HERMOSILLO, SONORA · 2026<br>
    Herramienta orientativa. En caso de duda, no consumas el alimento.
</div>
""", unsafe_allow_html=True)
