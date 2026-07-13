"""
Lógica y datos de la app ¿Puedo comerlo? sin dependencia de Streamlit,
para poder probarla con pruebas unitarias normales.
"""

# ─── Datos del producto ─────────────────────────────────────────────────────
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


# ─── Funciones puras ─────────────────────────────────────────────────────────

def valor_o_none(valor):
    """La IA a veces devuelve el texto 'null' en vez de un valor vacío real."""
    if isinstance(valor, str) and valor.strip().lower() in ("null", "none", ""):
        return None
    return valor


def daño_legible(tag):
    """Convierte una etiqueta interna de daño (snake_case) a texto en español."""
    tag_norm = str(tag).strip().lower()
    return DAÑOS_ETIQUETAS.get(tag_norm, tag_norm.replace("_", " "))


def preguntas_a_marcar(tipo_empaque, daños_detectados):
    """Índices de las preguntas de Paso 3 que coinciden con los daños que la IA vio en la foto."""
    preguntas_tipo = PREGUNTAS_EMPAQUE.get(tipo_empaque, PREGUNTAS_EMPAQUE["general"])
    idxs = set()
    for daño in daños_detectados:
        tag = str(valor_o_none(daño) or "").strip().lower()
        if not tag:
            continue
        palabras_clave = DAÑOS_A_PALABRAS_CLAVE.get(tag, [tag])
        for idx, (pregunta, _, _) in enumerate(preguntas_tipo):
            pregunta_norm = pregunta.lower()
            if any(kw in pregunta_norm for kw in palabras_clave):
                idxs.add(idx)
    return idxs


def decidir(hay_danger, hay_warning, es_caducidad, dias_diferencia, es_perecedero_actual):
    """
    Devuelve "danger", "caution" o "safe" según lo marcado en Paso 3 y la fecha
    (Paso 2, que para perecederos se salta: es_caducidad=False, dias_diferencia=0).
    """
    if hay_danger:
        return "danger"
    elif hay_warning and es_caducidad and dias_diferencia < -30:
        return "danger"
    elif hay_warning:
        return "caution"
    elif es_caducidad and dias_diferencia < -14:
        return "caution"
    elif es_caducidad and dias_diferencia < 0:
        return "caution"
    elif not es_perecedero_actual and not es_caducidad and dias_diferencia < -365:
        return "caution"
    else:
        return "safe"


def mensaje_estado_fecha(es_perecedero_actual, dias_diferencia):
    """Frase sobre cuántos días faltan/pasaron de la fecha indicada (vacía para perecederos)."""
    if es_perecedero_actual:
        return ""
    elif dias_diferencia > 0:
        return f"Faltan {dias_diferencia} días para la fecha indicada."
    elif dias_diferencia == 0:
        return "Hoy es el último día de la fecha indicada."
    else:
        return f"Lleva {abs(dias_diferencia)} días pasado la fecha indicada."
