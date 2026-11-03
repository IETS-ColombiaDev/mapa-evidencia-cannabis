import unittest
import io
import openpyxl
from app import app
from database import init_db, get_conn

class TestExcelImport(unittest.TestCase):
    def setUp(self):
        init_db()
        self.client = app.test_client()
        # Login as admin
        self.client.post('/login', data={'usuario': 'admin', 'clave': 'AdminIETS2025!'})

    def test_import_unauthorized_when_no_session(self):
        anon_client = app.test_client()
        resp = anon_client.post('/api/importar-excel', data={})
        self.assertEqual(resp.status_code, 401)

    def test_import_with_insumos_format(self):
        # Create an in-memory Excel file simulating the insumos format
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Respuestas de formulario 1"
        ws.append([
            'Marca temporal', 'Título ', 'Año', 'Revista', 'Volumen', 'Número',
            'Tipo de estudio', '¿El estudio tuvo en cuenta alguna población especial?',
            'Dominio general de la indicación clínica', 'Indicación como los autores la describen',
            'Intervención (Cannabis) como los autores la describen',
            'Desenlaces evaluados (no resultados) como los autores los describen',
            'Autor (apellido primer autor)', 'ID del estudio', 'Dirección de correo electrónico'
        ])
        ws.append([
            '2026-09-11', 'Estudio Insumos Test para Sueño y Dolor', 2026, 'Revista Test', '1', '2',
            'Ensayo clínico', 'Adultos', 'Salud mental', 'Insomnio',
            'Cannabidiol purificado Epidiolex', 'Calidad del sueño y dolor crónico',
            'Pérez', 9999, 'test@iets.org.co'
        ])
        bio = io.BytesIO()
        wb.save(bio)
        bio.seek(0)

        data = {
            'archivo': (bio, 'test_insumos.xlsx')
        }
        resp = self.client.post('/api/importar-excel', data=data, content_type='multipart/form-data')
        self.assertEqual(resp.status_code, 200)
        json_resp = resp.get_json()
        self.assertTrue(json_resp['ok'])
        self.assertEqual(json_resp['creados'], 1)

        # Verify it was inserted and mapped
        with get_conn() as conn:
            estudio = conn.execute("SELECT id, codigo, titulo, tipo_estudio FROM estudios WHERE titulo = ?", 
                                  ('Estudio Insumos Test para Sueño y Dolor',)).fetchone()
            self.assertIsNotNone(estudio)
            
            # Check mappings
            intervenciones = conn.execute("SELECT * FROM estudio_intervencion WHERE estudio_id = ?", (estudio['id'],)).fetchall()
            desenlaces = conn.execute("SELECT * FROM estudio_desenlace WHERE estudio_id = ?", (estudio['id'],)).fetchall()
            self.assertGreater(len(intervenciones), 0)
            self.assertGreater(len(desenlaces), 0)

            # Clean up test row
            conn.execute("DELETE FROM estudios WHERE id = ?", (estudio['id'],))

if __name__ == '__main__':
    unittest.main()

