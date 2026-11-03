import unittest
from app import app
from database import init_db

class TestAdminSecurity(unittest.TestCase):
    def setUp(self):
        init_db()
        self.client = app.test_client()

    def test_public_routes_accessible(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        # Verify open admin link is removed from public nav
        self.assertNotIn('<a href="/admin">Administración</a>', html)
        self.assertIn('Mapa interactivo', html)
        self.assertIn('Acceso administrativo', html)

        # Public APIs
        self.assertEqual(self.client.get('/api/datos').status_code, 200)
        self.assertEqual(self.client.get('/api/catalogos').status_code, 200)
        self.assertEqual(self.client.get('/api/salud').status_code, 200)

    def test_admin_panel_requires_login(self):
        resp = self.client.get('/admin')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login', resp.headers['Location'])

    def test_upload_endpoints_rejected_when_unauthenticated(self):
        # Excel import
        resp = self.client.post('/api/importar-excel', data={})
        self.assertEqual(resp.status_code, 401)
        self.assertIn('Acceso no autorizado', resp.get_json()['error'])

        # JSON batch import
        resp = self.client.post('/api/importar', json={'estudios': [{'titulo': 'Test'}]})
        self.assertEqual(resp.status_code, 401)

        # Study mutation
        resp = self.client.post('/api/estudios', json={'titulo': 'Test'})
        self.assertEqual(resp.status_code, 401)

    def test_login_flow_and_authenticated_access(self):
        # Bad login
        resp = self.client.post('/login', data={'usuario': 'admin', 'clave': 'wrongpass'})
        self.assertEqual(resp.status_code, 401)

        # Successful login
        resp = self.client.post('/login', data={'usuario': 'admin', 'clave': 'AdminIETS2025!'}, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        # Check authenticated status
        resp = self.client.get('/api/auth/estado')
        self.assertTrue(resp.get_json()['autenticado'])
        self.assertEqual(resp.get_json()['usuario'], 'admin')

        # Now /admin is accessible
        resp = self.client.get('/admin')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Administrar el mapa', resp.get_data(as_text=True))
        self.assertIn('Cerrar sesión', resp.get_data(as_text=True))

        # Logout
        resp = self.client.get('/logout')
        self.assertEqual(resp.status_code, 302)

        # Post-logout admin is protected again
        resp = self.client.get('/admin')
        self.assertEqual(resp.status_code, 302)

    def test_retired_dimensions_not_in_ui(self):
        # 1. Check index.html does not contain retired filters or view mode
        resp = self.client.get('/')
        html = resp.get_data(as_text=True)
        self.assertNotIn('data-filtro="certeza"', html)
        self.assertNotIn('data-filtro="hallazgo"', html)
        self.assertNotIn('data-filtro="ambito"', html)
        self.assertNotIn('data-vista="certeza"', html)
        # Poblacion filter is present for general/especial population
        self.assertIn('data-filtro="poblacion"', html)

        # 2. Check admin.html modal form does not contain retired fields
        self.client.post('/login', data={'usuario': 'admin', 'clave': 'AdminIETS2025!'})
        admin_resp = self.client.get('/admin')
        admin_html = admin_resp.get_data(as_text=True)
        self.assertNotIn('id="f-certeza"', admin_html)
        self.assertNotIn('id="f-hallazgo"', admin_html)
        self.assertNotIn('id="f-ambito"', admin_html)
        self.assertNotIn('id="f-pais"', admin_html)

        # 3. Check mapa.js CAMPOS_FILTRO includes poblacion and not certeza/hallazgo/ambito
        with open('static/js/mapa.js', 'r', encoding='utf-8') as f:
            mapa_js = f.read()
        self.assertIn('const CAMPOS_FILTRO = ["tipo_estudio", "poblacion", "decada"];', mapa_js)
        self.assertNotIn('"certeza"', mapa_js[:100])
        self.assertNotIn('mejorCerteza', mapa_js)

    def test_editor_login_and_access(self):
        # Successful editor login
        resp = self.client.post('/login', data={'usuario': 'editor', 'clave': 'EditorIETS2025!'}, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        # Check authenticated status shows editor role
        resp = self.client.get('/api/auth/estado')
        data = resp.get_json()
        self.assertTrue(data['autenticado'])
        self.assertEqual(data['usuario'], 'editor')
        self.assertEqual(data['rol'], 'editor')

        # Admin panel is accessible
        resp = self.client.get('/admin')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Editor', resp.get_data(as_text=True))

        # Logout
        self.client.get('/logout')

    def test_poblacion_general_rule(self):
        # Check /api/datos populates "Población general" when poblacion_especial is empty
        resp = self.client.get('/api/datos')
        self.assertEqual(resp.status_code, 200)
        datos = resp.get_json()
        self.assertTrue(datos['ok'])
        estudios = datos['estudios']
        
        # Check that empty poblacion_especial resolves to Población general
        for e in estudios:
            raw = (e.get('poblacion_especial') or '').strip()
            if not raw:
                self.assertEqual(e['poblacion'], 'Población general')
            else:
                self.assertEqual(e['poblacion'], raw)

if __name__ == '__main__':
    unittest.main()

