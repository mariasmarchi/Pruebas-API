import requests
import pytest
import pytest_check as check
from faker import Faker
from datetime import datetime
import logging

fake = Faker()
logger = logging.getLogger(__name__)

def validate_api_response(response, expected_status, expected_fields=None, max_time=1.0):
    """Función helper para validar respuestas API con los 5 niveles"""
    # Nivel 1: Status
    assert response.status_code == expected_status
    # Nivel 2: Headers (flexible: acepta cualquier variante con json)
    if expected_status != 204:  # 204 No Content puede no tener Content-Type
        content_type = response.headers.get('Content-Type', '')
        assert 'json' in content_type.lower()
    # Nivel 3-4: Estructura y contenido (si hay expected_fields)
    if expected_fields and response.text:
        body = response.json()
        assert expected_fields <= set(body.keys())
    # Nivel 5: Performance
    assert response.elapsed.total_seconds() < max_time
    return response.json() if response.text else {}

class TestGetUser:

    @pytest.mark.get
    def test_get_response_code(self, api_url):
        response = requests.get(api_url + "users")
        # Logging seguro
        logger.info(f"Status recibido: {response.status_code}")
        logger.info(f"Header Content-Type: {response.headers.get('Content-Type')}")
        body_preview = response.text[:200] if response.text else "<sin cuerpo>"
        logger.info(f"Body preview: {body_preview}")

        # Validación flexible con pytest-check
        check.equal(response.status_code, 200, "Esperábamos 200 en GET /users")
        check.is_true('json' in response.headers.get('Content-Type', '').lower(), "El header debe ser JSON")

    @pytest.mark.get
    def test_get_response_data(self, api_url):
        response = requests.get(api_url + "users")
        data = response.json()  # lista

        assert len(data) > 0
        assert isinstance(data, list)

        first_user = data[0]
        key_structure = ["id", "name", "username", "phone", "address", "website"]

        for i in key_structure:
            assert i in first_user, f"campo {i}, no está en {first_user}"

class TestPostUser:

    @pytest.mark.post
    def test_post_response_code(self, api_url):
        new_user = {
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number()
        }

        response = requests.post(api_url + "users", new_user)
        assert response.status_code == 201

        data = response.json()
        logger.info(f"Usuario creado: {data}")
        assert "id" in data  # verifica que el id esté en la respuesta

        if "createdAt" in data:
            created_at = data["createdAt"]
            current_year = datetime.now().year
            assert str(current_year) in created_at, f"no está en el año actual"

class TestUserWorkflow:

    def test_completo_users(self, api_url):
        logger.info("=== INICIO DEL WORKFLOW DE USUARIOS ===")

        # 1. GET: OBTENER USUARIOS
        response = requests.get(api_url + "users")
        data = response.json()
        check.equal(response.status_code, 200)
        logger.info(f"Usuarios obtenidos: {len(data)}")

        # 2. POST: CREAR UN USUARIO
        new_user = {
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number()
        }
        response = requests.post(api_url + "users", new_user)
        assert response.status_code == 201
        created_user = response.json()
        user_id = created_user.get("id")
        logger.info(f"Usuario creado con ID: {user_id}")
        assert user_id is not None

        # 3. GET: VERIFICAR QUE EL USUARIO SE CREÓ (jsonplaceholder no persiste → aceptamos 404)
        response = requests.get(api_url + f"users/{user_id}")
        check.is_true(response.status_code in [200, 404], f"Status recibido: {response.status_code}")

        # 4. PATCH: ACTUALIZAR EL USUARIO
        update_data = {"phone": fake.phone_number()}
        response = requests.patch(api_url + f"users/{user_id}", update_data)
        check.is_true(response.status_code in [200, 204])
        if response.text:
            updated_user = response.json()
            logger.info(f"Usuario actualizado: {updated_user}")

        # 5. DELETE: ELIMINAR EL USUARIO
        response = requests.delete(api_url + f"users/{user_id}")
        check.is_true(response.status_code in [200, 204, 404])
        logger.info(f"DELETE status: {response.status_code}")

        logger.info("=== FIN DEL WORKFLOW DE USUARIOS ===")

class TestUserFailures:
    @pytest.mark.get
    def test_usuario_inexistente(self, api_url, driver=None):
        """
        Prueba fallida controlada: intentamos obtener un usuario que no existe.
        Esto forzará un fallo (esperamos 200, API devuelve 404), pero usamos pytest-check
        para que el test siga corriendo y se refleje el detalle en el reporte HTML.
        """
        user_id = 99999
        logger.info(f"Intentando obtener usuario inexistente ID={user_id}")
        response = requests.get(api_url + f"users/{user_id}")

        # Fallo controlado (no corta el test)
        check.equal(response.status_code, 200, f"Esperábamos 200 en GET /users/{user_id}, recibido {response.status_code}")

        # Seguimos registrando detalles aunque falle
        content_type = response.headers.get("Content-Type", "")
        check.is_true("json" in content_type.lower(), "El header debe ser JSON")
        body_preview = response.text[:200] if response.text else "<sin cuerpo>"
        logger.info(f"Content-Type: {content_type}")
        logger.info(f"Body preview: {body_preview}")

        # Captura opcional si hay Selenium driver
        if driver:
            try:
                driver.save_screenshot("reports/fallo_usuario.png")
                logger.info("Captura de pantalla guardada: reports/fallo_usuario.png")
            except Exception as e:
                logger.error(f"No se pudo guardar la captura de pantalla: {e}")
