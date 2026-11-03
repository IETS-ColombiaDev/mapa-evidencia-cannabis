"""
Pruebas para la funcionalidad de medicamentos aprobados por INVIMA en Colombia
y su integración en el Mapa de Evidencia.
"""

import unittest
from app import app
from database import get_conn


class TestAprobadosColombia(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_api_datos_incluye_aprobados_colombia(self):
        resp = self.client.get("/api/datos")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data.get("ok"))
        self.assertIn("aprobados_colombia", data)
        aprobados = data["aprobados_colombia"]
        self.assertEqual(len(aprobados), 9)

        # Verificar los cruces clave
        cruces = {(m["intervencion_codigo"], m["desenlace_codigo"]) for m in aprobados}
        self.assertIn(("I2", "O2"), cruces)  # Sativex (espasticidad)
        self.assertIn(("I1", "O4"), cruces)  # Neviot, Cannepi, etc. (crisis epilépticas)
        self.assertIn(("I3", "O3"), cruces)  # Laxenol (náuseas y vómitos)

    def test_api_aprobados_colombia_endpoint(self):
        resp = self.client.get("/api/aprobados-colombia")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data.get("ok"))
        self.assertIn("medicamentos", data)
        self.assertEqual(len(data["medicamentos"]), 9)

        # Verificar estructura de campos
        primer = data["medicamentos"][0]
        for campo in ["producto", "registro_sanitario", "principio_activo", "indicaciones", "intervencion_codigo", "desenlace_codigo"]:
            self.assertIn(campo, primer)
            self.assertTrue(primer[campo])

    def test_html_index_elementos_aprobados(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        # Botón de resaltar aprobados
        self.assertIn('id="btn-aprobados"', html)
        self.assertIn("Aprobados en Colombia", html)

        # Elemento en la leyenda
        self.assertIn("insignia-invima-leyenda", html)
        self.assertIn("Aprobación INVIMA", html)

        # Contenedor de alerta en el modal
        self.assertIn('id="modal-invima-alerta"', html)

    def test_base_datos_medicamentos_aprobados(self):
        with get_conn() as conn:
            filas = conn.execute("SELECT * FROM medicamentos_aprobados ORDER BY orden").fetchall()
            self.assertEqual(len(filas), 9)

            # Verificar Sativex
            sativex = [dict(f) for f in filas if "sativex" in f["producto"].lower()][0]
            self.assertEqual(sativex["intervencion_codigo"], "I2")
            self.assertEqual(sativex["desenlace_codigo"], "O2")
            self.assertIn("2022M-0017373", sativex["registro_sanitario"])

            # Verificar Laxenol
            laxenol = [dict(f) for f in filas if "laxenol" in f["producto"].lower()][0]
            self.assertEqual(laxenol["intervencion_codigo"], "I3")
            self.assertEqual(laxenol["desenlace_codigo"], "O3")
            self.assertIn("2025M-0022380", laxenol["registro_sanitario"])

            # Verificar Neviot / Cannabidiol
            cbd_meds = [dict(f) for f in filas if f["intervencion_codigo"] == "I1" and f["desenlace_codigo"] == "O4"]
            self.assertEqual(len(cbd_meds), 7)


if __name__ == "__main__":
    unittest.main()

