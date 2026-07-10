"""
Ilustraciones SVG para la app ¿Puedo comerlo?
Una por cada tipo de empaque (lata, empaque flexible, botella, frasco, caja)
en tres estados: ok, warn, danger
"""

def svg_card(svg_content, estado, label, sublabel):
    """Envuelve una ilustración SVG en una tarjeta de color según el estado."""
    colores = {
        "ok":     {"bg": "#dcfce7", "border": "#16a34a", "text": "#15803d"},
        "warn":   {"bg": "#fef3c7", "border": "#d97706", "text": "#92400e"},
        "danger": {"bg": "#fee2e2", "border": "#dc2626", "text": "#991b1b"},
    }
    c = colores[estado]
    iconos = {"ok": "🟢", "warn": "🟡", "danger": "🔴"}
    estilo = f"background:{c['bg']};border:2px solid {c['border']};border-radius:12px;padding:12px 8px 10px 8px;text-align:center;flex:1;min-width:130px;"
    etiqueta_estilo = f"font-size:0.8rem;font-weight:600;color:{c['text']};margin-top:6px;"
    sub_estilo = f"font-size:0.72rem;color:{c['text']};opacity:0.85;margin-top:2px;line-height:1.3;"
    return f'<div style="{estilo}">{svg_content}<div style="{etiqueta_estilo}">{iconos[estado]} {label}</div><div style="{sub_estilo}">{sublabel}</div></div>'


def wrap_row(cards_html):
    """Envuelve las tarjetas en un flex row."""
    return f"""
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin:10px 0 6px 0;">
        {cards_html}
    </div>"""


# ─── LATAS ──────────────────────────────────────────────────────────────────

LATA_OK = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <rect x="16" y="18" width="48" height="58" rx="4" fill="#94a3b8"/>
  <rect x="12" y="12" width="56" height="10" rx="4" fill="#64748b"/>
  <rect x="12" y="72" width="56" height="10" rx="4" fill="#64748b"/>
  <rect x="18" y="20" width="44" height="54" rx="2" fill="#cbd5e1" opacity="0.3"/>
</svg>"""

LATA_WARN = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <rect x="16" y="18" width="48" height="58" rx="4" fill="#94a3b8"/>
  <path d="M16,50 L28,42 L40,52 L16,52 Z" fill="#64748b"/>
  <rect x="12" y="12" width="56" height="10" rx="4" fill="#64748b"/>
  <rect x="12" y="72" width="56" height="10" rx="4" fill="#64748b"/>
</svg>"""

LATA_DANGER = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <rect x="16" y="22" width="48" height="54" rx="4" fill="#94a3b8"/>
  <path d="M12,12 Q40,2 68,12 L68,22 Q40,14 12,22 Z" fill="#64748b"/>
  <rect x="12" y="72" width="56" height="10" rx="4" fill="#64748b"/>
  <circle cx="36" cy="45" r="7" fill="#b45309"/>
  <circle cx="48" cy="55" r="5" fill="#b45309"/>
  <circle cx="28" cy="58" r="4" fill="#92400e"/>
</svg>"""


# ─── EMPAQUES FLEXIBLES (pasta, arroz, harina) ──────────────────────────────

EMPAQUE_OK = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <rect x="14" y="16" width="52" height="62" rx="6" fill="#bfdbfe"/>
  <rect x="10" y="10" width="60" height="10" rx="4" fill="#60a5fa"/>
  <rect x="10" y="74" width="60" height="10" rx="4" fill="#60a5fa"/>
  <rect x="18" y="18" width="44" height="58" rx="2" fill="#dbeafe" opacity="0.4"/>
</svg>"""

EMPAQUE_WARN = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <path d="M14,16 Q8,40 14,78 L66,78 Q72,40 66,16 Z" fill="#bfdbfe"/>
  <rect x="10" y="10" width="60" height="10" rx="4" fill="#60a5fa"/>
  <rect x="10" y="74" width="60" height="10" rx="4" fill="#60a5fa"/>
</svg>"""

EMPAQUE_DANGER = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <rect x="14" y="16" width="52" height="62" rx="6" fill="#bfdbfe"/>
  <path d="M38,10 L28,45 L42,45 L32,84" stroke="#dc2626" stroke-width="2.5" fill="none"/>
  <ellipse cx="22" cy="54" rx="8" ry="5" fill="#93c5fd" opacity="0.7"/>
  <ellipse cx="54" cy="64" rx="6" ry="4" fill="#93c5fd" opacity="0.6"/>
  <rect x="10" y="10" width="60" height="10" rx="4" fill="#60a5fa"/>
  <rect x="10" y="74" width="60" height="10" rx="4" fill="#60a5fa"/>
</svg>"""


# ─── BOTELLAS ───────────────────────────────────────────────────────────────

BOTELLA_OK = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <path d="M30,30 L30,20 Q40,16 50,20 L50,30 Q58,42 58,72 L22,72 Q22,42 30,30 Z" fill="#6ee7b7"/>
  <rect x="30" y="12" width="20" height="12" rx="4" fill="#34d399"/>
  <rect x="28" y="26" width="24" height="6" rx="2" fill="#059669" opacity="0.4"/>
  <rect x="22" y="72" width="36" height="8" rx="3" fill="#34d399"/>
</svg>"""

BOTELLA_WARN = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <path d="M30,30 L30,20 Q40,16 50,20 L50,30 Q58,42 58,72 L22,72 Q22,42 30,30 Z" fill="#6ee7b7"/>
  <rect x="30" y="12" width="20" height="12" rx="4" fill="#34d399"/>
  <path d="M28,26 L36,26 L40,32 L52,26 L52,32 L28,32 Z" fill="#fcd34d" opacity="0.9"/>
  <rect x="22" y="72" width="36" height="8" rx="3" fill="#34d399"/>
</svg>"""

BOTELLA_DANGER = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <path d="M30,30 L30,20 Q40,16 50,20 L50,30 Q58,42 58,72 L22,72 Q22,42 30,30 Z" fill="#6ee7b7"/>
  <path d="M30,12 Q40,4 50,12 L50,24 Q40,16 30,24 Z" fill="#f87171"/>
  <ellipse cx="40" cy="55" rx="14" ry="8" fill="#78716c" opacity="0.35"/>
  <rect x="22" y="72" width="36" height="8" rx="3" fill="#34d399"/>
</svg>"""


# ─── FRASCOS ────────────────────────────────────────────────────────────────

FRASCO_OK = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <rect x="18" y="26" width="44" height="54" rx="8" fill="#fde68a"/>
  <rect x="22" y="14" width="36" height="16" rx="6" fill="#f59e0b"/>
  <ellipse cx="40" cy="15" rx="9" ry="3.5" fill="#d97706"/>
  <rect x="20" y="26" width="40" height="8" rx="2" fill="#fbbf24" opacity="0.4"/>
</svg>"""

FRASCO_WARN = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <rect x="18" y="26" width="44" height="54" rx="8" fill="#fde68a"/>
  <rect x="22" y="14" width="36" height="16" rx="6" fill="#f59e0b"/>
  <circle cx="32" cy="34" r="6" fill="#065f46" opacity="0.75"/>
  <circle cx="46" cy="40" r="5" fill="#065f46" opacity="0.65"/>
  <circle cx="36" cy="44" r="4" fill="#064e3b" opacity="0.55"/>
</svg>"""

FRASCO_DANGER = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <rect x="18" y="26" width="44" height="54" rx="8" fill="#fde68a"/>
  <path d="M22,14 Q40,4 58,14 L58,30 Q40,20 22,30 Z" fill="#f87171"/>
  <rect x="20" y="26" width="40" height="6" rx="2" fill="#fca5a5" opacity="0.4"/>
</svg>"""


# ─── CAJAS (cereal, avena) ──────────────────────────────────────────────────

CAJA_OK = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <rect x="16" y="14" width="48" height="64" rx="4" fill="#fde68a"/>
  <rect x="16" y="14" width="48" height="10" rx="2" fill="#fbbf24"/>
  <rect x="16" y="68" width="48" height="10" rx="2" fill="#fbbf24"/>
  <rect x="20" y="26" width="40" height="40" rx="2" fill="#fef9c3" opacity="0.5"/>
</svg>"""

CAJA_WARN = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <rect x="16" y="14" width="48" height="64" rx="4" fill="#fde68a"/>
  <rect x="16" y="14" width="48" height="10" rx="2" fill="#fbbf24"/>
  <rect x="16" y="68" width="48" height="10" rx="2" fill="#fbbf24"/>
  <ellipse cx="30" cy="48" rx="9" ry="6" fill="#93c5fd" opacity="0.65"/>
  <ellipse cx="50" cy="58" rx="7" ry="5" fill="#93c5fd" opacity="0.55"/>
</svg>"""

CAJA_DANGER = """
<svg viewBox="0 0 80 90" width="80" height="90" xmlns="http://www.w3.org/2000/svg">
  <rect x="16" y="14" width="48" height="64" rx="4" fill="#fde68a"/>
  <rect x="16" y="14" width="48" height="10" rx="2" fill="#fbbf24"/>
  <rect x="16" y="68" width="48" height="10" rx="2" fill="#fbbf24"/>
  <path d="M40,14 L32,42 L46,42 L38,78" stroke="#dc2626" stroke-width="2.5" fill="none"/>
  <ellipse cx="26" cy="55" rx="5" ry="2.5" fill="#44403c"/>
  <ellipse cx="54" cy="45" rx="4" ry="2" fill="#44403c"/>
</svg>"""


# ─── FUNCIÓN PRINCIPAL ──────────────────────────────────────────────────────

def get_ilustraciones(tipo_empaque):
    """
    Devuelve HTML con las 3 ilustraciones de referencia para el tipo de empaque dado.
    """
    mapeo = {
        "lata": (
            (LATA_OK,      "ok",     "Lata segura",       "Tapa plana · Sin óxido"),
            (LATA_WARN,    "warn",   "Revisar",           "Golpe en cuerpo · Sin perforar"),
            (LATA_DANGER,  "danger", "No consumir",       "Inflada o con óxido"),
        ),
        "empaque_seco": (
            (EMPAQUE_OK,      "ok",     "Empaque seguro",    "Sellado · Sin humedad"),
            (EMPAQUE_WARN,    "warn",   "Revisar",           "Aplastado · Sin rotura"),
            (EMPAQUE_DANGER,  "danger", "No consumir",       "Roto o húmedo"),
        ),
        "empaque_flexible": (
            (EMPAQUE_OK,      "ok",     "Empaque seguro",    "Sellado · Sin humedad"),
            (EMPAQUE_WARN,    "warn",   "Revisar",           "Aplastado · Sin rotura"),
            (EMPAQUE_DANGER,  "danger", "No consumir",       "Roto o húmedo"),
        ),
        "botella": (
            (BOTELLA_OK,      "ok",     "Botella segura",    "Sello intacto · Olor normal"),
            (BOTELLA_WARN,    "warn",   "Revisar",           "Sello levantado"),
            (BOTELLA_DANGER,  "danger", "No consumir",       "Tapa abombada · Turbio"),
        ),
        "frasco": (
            (FRASCO_OK,      "ok",     "Frasco seguro",     "Botón abajo · Vacío"),
            (FRASCO_WARN,    "warn",   "Revisar",           "Moho en superficie"),
            (FRASCO_DANGER,  "danger", "No consumir",       "Tapa abombada arriba"),
        ),
        "caja": (
            (CAJA_OK,      "ok",     "Caja íntegra",      "Bolsa interior sellada"),
            (CAJA_WARN,    "warn",   "Revisar",           "Caja mojada"),
            (CAJA_DANGER,  "danger", "No consumir",       "Rota o con insectos"),
        ),
        "general": (
            (EMPAQUE_OK,      "ok",     "Intacto",           "Sin daños visibles"),
            (EMPAQUE_WARN,    "warn",   "Revisar",           "Algún daño menor"),
            (EMPAQUE_DANGER,  "danger", "No consumir",       "Dañado o contaminado"),
        ),
    }

    tipo = tipo_empaque if tipo_empaque in mapeo else "general"
    items = mapeo[tipo]
    cards = "".join(svg_card(svg, est, lbl, sub) for svg, est, lbl, sub in items)
    return wrap_row(cards)
