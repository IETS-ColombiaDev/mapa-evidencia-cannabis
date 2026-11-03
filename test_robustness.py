"""
Pruebas integrales de robustez, seguridad y casos de borde para el Mapa de Evidencia.
"""

import io
import unittest
from app import app
from database import get_conn, init_db, verificar_usuario, crear_usuario


class TestRobustez(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_idempotencia_init_db(self):
        # Ejecutar init_db múltiples veces consecutivas no debe duplicar ni corromper datos
        init_db()
        init_db()
        with get_conn() as conn:
            n_admin = conn.execute("SELECT COUNT(*) AS n FROM usuarios WHERE username='admin'").fetchone()["n"]
            self.assertEqual(n_admin, 1)
            n_aprob = conn.execute("SELECT COUNT(*) AS n FROM medicamentos_aprobados").fetchone()["n"]
            self.assertEqual(n_aprob, 9)

    def test_seguridad_rutas_protegidas_sin_autenticacion(self):
        # Todos los métodos de mutación deben rechazar peticiones no autorizadas
        endpoints = [
            ("POST", "/api/estudios", {"titulo": "Prueba XSS", "tipo_estudio": "Revisión sistemática"}),
            ("PUT", "/api/estudios/1", {"titulo": "Actualizado"}),
            ("DELETE", "/api/estudios/1", None),
            ("POST", "/api/intervenciones", {"nombre": "Int", "categoria_id": 1}),
            ("PUT", "/api/intervenciones/1", {"nombre": "Int", "categoria_id": 1}),
            ("DELETE", "/api/intervenciones/1", None),
            ("POST", "/api/desenlaces", {"nombre": "Des", "dominio_id": 1}),
            ("PUT", "/api/desenlaces/1", {"nombre": "Des", "dominio_id": 1}),
            ("DELETE", "/api/desenlaces/1", None),
            ("POST", "/api/categorias", {"nombre": "Cat"}),
            ("PUT", "/api/categorias/1", {"nombre": "Cat"}),
            ("DELETE", "/api/categorias/1", None),
            ("POST", "/api/dominios", {"nombre": "Dom"}),
            ("PUT", "/api/dominios/1", {"nombre": "Dom"}),
            ("DELETE", "/api/dominios/1", None),
            ("POST", "/api/importar", {"estudios": [{"titulo": "E1"}]}),
        ]
        for metodo, url, payload in endpoints:
            if metodo == "POST":
                resp = self.client.post(url, json=payload)
            elif metodo == "PUT":
                resp = self.client.put(url, json=payload)
            elif metodo == "DELETE":
                resp = self.client.delete(url)
            self.assertEqual(resp.status_code, 401, f"Falló protección en {metodo} {url}")
            data = resp.get_json()
            self.assertFalse(data.get("ok"))
            self.assertIn("Acceso no autorizado", data.get("error", ""))

    def test_seguridad_vista_admin_redirecciona_a_login(self):
        resp = self.client.get("/admin")
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp.headers.get("Location", ""))

    def test_verificar_usuario_resistencia(self):
        # Credenciales nulas, vacías o con espacios no deben producir excepciones
        self.assertIsNone(verificar_usuario("", ""))
        self.assertIsNone(verificar_usuario(None, None))
        self.assertIsNone(verificar_usuario("   ", "   "))
        self.assertIsNone(verificar_usuario("admin", "clave_totalmente_invalida"))
        self.assertIsNone(verificar_usuario("usuario_inexistente", "cualquiera"))

    def test_datos_api_consistencia_poblacion_general(self):
        resp = self.client.get("/api/datos")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data.get("ok"))
        estudios = data.get("estudios", [])
        self.assertGreater(len(estudios), 0)

        for e in estudios:
            # Nunca debe ser None o vacío; si no tiene poblacion_especial debe ser 'Población general'
            pob = e.get("poblacion")
            self.assertTrue(pob and isinstance(pob, str) and pob.strip())
            pob_esp = (e.get("poblacion_especial") or "").strip()
            if not pob_esp:
                self.assertEqual(pob, "Población general")

    def test_datos_api_aprobados_colombia_consistencia(self):
        resp = self.client.get("/api/datos")
        data = resp.get_json()
        aprobados = data.get("aprobados_colombia", [])
        self.assertEqual(len(aprobados), 9)

        # Verificar que todos los registros tengan códigos de taxonomía válidos
        codigos_int_validos = {i["codigo"] for i in data["intervenciones"]}
        codigos_des_validos = {d["codigo"] for d in data["desenlaces"]}

        for med in aprobados:
            self.assertIn(med["intervencion_codigo"], codigos_int_validos)
            self.assertIn(med["desenlace_codigo"], codigos_des_validos)
            self.assertTrue(med["producto"].strip())
            self.assertTrue(med["registro_sanitario"].strip())
            self.assertTrue(med["indicaciones"].strip())


if __name__ == "__main__":
    unittest.main()

