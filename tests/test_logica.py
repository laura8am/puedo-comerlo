import unittest

from logica import (
    PRODUCTOS_NO_PERECEDEROS,
    PRODUCTOS_PERECEDEROS,
    CATEGORIAS_PERECEDERAS,
    PREGUNTAS_EMPAQUE,
    TIPS_POR_PRODUCTO,
    DAÑOS_A_PALABRAS_CLAVE,
    valor_o_none,
    daño_legible,
    preguntas_a_marcar,
    decidir,
    mensaje_estado_fecha,
)


class TestValorONone(unittest.TestCase):
    def test_texto_null_se_vuelve_none(self):
        for texto in ["null", "NULL", "Null", "none", "NONE", "", "  "]:
            self.assertIsNone(valor_o_none(texto))

    def test_texto_valido_pasa_sin_cambios(self):
        self.assertEqual(valor_o_none("Plátano"), "Plátano")
        self.assertEqual(valor_o_none("2026-07-13"), "2026-07-13")

    def test_no_string_pasa_sin_cambios(self):
        self.assertIsNone(valor_o_none(None))
        self.assertEqual(valor_o_none(["moho"]), ["moho"])


class TestDañoLegible(unittest.TestCase):
    def test_etiquetas_conocidas(self):
        self.assertEqual(daño_legible("golpe_costura"), "golpe en costura")
        self.assertEqual(daño_legible("tapa_abombada"), "tapa abombada")
        self.assertEqual(daño_legible("moho"), "moho")

    def test_es_insensible_a_mayusculas_y_espacios(self):
        self.assertEqual(daño_legible("  GOLPE_COSTURA  "), "golpe en costura")

    def test_etiqueta_desconocida_usa_guiones_bajos_como_espacios(self):
        self.assertEqual(daño_legible("etiqueta_nueva_futura"), "etiqueta nueva futura")


class TestPreguntasAMarcar(unittest.TestCase):
    def test_marca_la_pregunta_que_corresponde(self):
        idxs = preguntas_a_marcar("lata", ["abombada"])
        preguntas_lata = PREGUNTAS_EMPAQUE["lata"]
        preguntas_marcadas = {preguntas_lata[i][0] for i in idxs}
        self.assertIn("¿La lata está abombada o inflada?", preguntas_marcadas)

    def test_marca_varias_preguntas_para_varios_daños(self):
        idxs = preguntas_a_marcar("carne_pescado", ["agrio", "decolorado"])
        self.assertGreaterEqual(len(idxs), 2)

    def test_daño_sin_coincidencia_no_marca_nada(self):
        idxs = preguntas_a_marcar("lata", ["algo_que_no_existe_en_ninguna_pregunta"])
        self.assertEqual(idxs, set())

    def test_lista_vacia_no_marca_nada(self):
        self.assertEqual(preguntas_a_marcar("lata", []), set())

    def test_tipo_empaque_desconocido_usa_general(self):
        # No debe lanzar KeyError aunque tipo_empaque no exista.
        idxs = preguntas_a_marcar("categoria_inventada", ["moho"])
        preguntas_general = PREGUNTAS_EMPAQUE["general"]
        preguntas_marcadas = {preguntas_general[i][0] for i in idxs}
        self.assertTrue(any("moho" in p.lower() for p in preguntas_marcadas))

    def test_ignora_daños_vacios_o_null(self):
        idxs = preguntas_a_marcar("lata", ["null", "", None])
        self.assertEqual(idxs, set())


class TestDecidir(unittest.TestCase):
    def test_cualquier_danger_marcado_gana_siempre(self):
        self.assertEqual(
            decidir(hay_danger=True, hay_warning=False, es_caducidad=False, dias_diferencia=100, es_perecedero_actual=False),
            "danger",
        )

    def test_warning_marcado_es_caution_por_defecto(self):
        self.assertEqual(
            decidir(hay_danger=False, hay_warning=True, es_caducidad=False, dias_diferencia=0, es_perecedero_actual=False),
            "caution",
        )

    def test_warning_mas_caducidad_muy_vencida_escala_a_danger(self):
        self.assertEqual(
            decidir(hay_danger=False, hay_warning=True, es_caducidad=True, dias_diferencia=-31, es_perecedero_actual=False),
            "danger",
        )

    def test_caducidad_vencida_poco_es_caution(self):
        self.assertEqual(
            decidir(hay_danger=False, hay_warning=False, es_caducidad=True, dias_diferencia=-1, es_perecedero_actual=False),
            "caution",
        )

    def test_consumo_preferente_vencido_menos_de_un_año_es_safe(self):
        self.assertEqual(
            decidir(hay_danger=False, hay_warning=False, es_caducidad=False, dias_diferencia=-300, es_perecedero_actual=False),
            "safe",
        )

    def test_consumo_preferente_vencido_mas_de_un_año_es_caution(self):
        self.assertEqual(
            decidir(hay_danger=False, hay_warning=False, es_caducidad=False, dias_diferencia=-366, es_perecedero_actual=False),
            "caution",
        )

    def test_nada_marcado_y_fecha_vigente_es_safe(self):
        self.assertEqual(
            decidir(hay_danger=False, hay_warning=False, es_caducidad=True, dias_diferencia=10, es_perecedero_actual=False),
            "safe",
        )

    def test_perecedero_sin_nada_marcado_es_safe(self):
        # Paso 2 se salta para perecederos: es_caducidad=False, dias_diferencia=0.
        self.assertEqual(
            decidir(hay_danger=False, hay_warning=False, es_caducidad=False, dias_diferencia=0, es_perecedero_actual=True),
            "safe",
        )

    def test_perecedero_con_warning_es_caution(self):
        self.assertEqual(
            decidir(hay_danger=False, hay_warning=True, es_caducidad=False, dias_diferencia=0, es_perecedero_actual=True),
            "caution",
        )

    def test_perecedero_con_danger_es_danger(self):
        self.assertEqual(
            decidir(hay_danger=True, hay_warning=False, es_caducidad=False, dias_diferencia=0, es_perecedero_actual=True),
            "danger",
        )

    def test_perecedero_nunca_usa_la_gracia_de_365_dias(self):
        # Esto no debería pasar en la práctica (Paso 2 se salta), pero si por
        # alguna razón es_caducidad/dias_diferencia trajeran valores de fecha,
        # los perecederos no deben beneficiarse de la gracia de un año.
        self.assertEqual(
            decidir(hay_danger=False, hay_warning=False, es_caducidad=False, dias_diferencia=-400, es_perecedero_actual=True),
            "safe",
        )


class TestMensajeEstadoFecha(unittest.TestCase):
    def test_perecedero_no_tiene_mensaje(self):
        self.assertEqual(mensaje_estado_fecha(True, 5), "")
        self.assertEqual(mensaje_estado_fecha(True, -5), "")

    def test_dias_positivos(self):
        self.assertEqual(mensaje_estado_fecha(False, 3), "Faltan 3 días para la fecha indicada.")

    def test_hoy_es_el_limite(self):
        self.assertEqual(mensaje_estado_fecha(False, 0), "Hoy es el último día de la fecha indicada.")

    def test_dias_pasados(self):
        self.assertEqual(mensaje_estado_fecha(False, -7), "Lleva 7 días pasado la fecha indicada.")


class TestConsistenciaDeDatos(unittest.TestCase):
    """Evita que se agregue una categoría de producto sin sus preguntas/tips."""

    def test_toda_categoria_tiene_preguntas(self):
        categorias = set(PRODUCTOS_NO_PERECEDEROS.values()) | set(PRODUCTOS_PERECEDEROS.values())
        faltantes = categorias - set(PREGUNTAS_EMPAQUE.keys())
        self.assertEqual(faltantes, set(), f"Sin preguntas en PREGUNTAS_EMPAQUE: {faltantes}")

    def test_toda_categoria_tiene_tip(self):
        categorias = set(PRODUCTOS_NO_PERECEDEROS.values()) | set(PRODUCTOS_PERECEDEROS.values())
        faltantes = categorias - set(TIPS_POR_PRODUCTO.keys())
        self.assertEqual(faltantes, set(), f"Sin tip en TIPS_POR_PRODUCTO: {faltantes}")

    def test_categorias_perecederas_coincide_con_productos_perecederos(self):
        self.assertEqual(CATEGORIAS_PERECEDERAS, set(PRODUCTOS_PERECEDEROS.values()))

    def test_cada_pregunta_tiene_nivel_valido(self):
        niveles_validos = {"danger", "warning"}
        for categoria, preguntas in PREGUNTAS_EMPAQUE.items():
            for pregunta, nivel, explicacion in preguntas:
                self.assertIn(nivel, niveles_validos, f"{categoria!r}: nivel inválido {nivel!r} en {pregunta!r}")

    def test_palabras_clave_de_daños_no_estan_vacias(self):
        for tag, palabras in DAÑOS_A_PALABRAS_CLAVE.items():
            self.assertTrue(palabras, f"Sin palabras clave para el tag {tag!r}")


if __name__ == "__main__":
    unittest.main()
