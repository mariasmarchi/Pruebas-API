import requests
import pytest
import pytest_check as check
from faker import Faker
from datetime import datetime

fake = Faker()

def validate_api_response(response, expected_status, expected_fields=None, max_time=1.0):
    """Función helper para validar respuestas API con los 5 niveles"""
    # Nivel 1: Status
    assert response.status_code == expected_status
    # Nivel 2: Headers
    if expected_status != 204:  # 204 No Content puede no tener Content-Type
        assert 'application/json' in response.headers.get('Content-Type', '')
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
        data = validate_api_response(
            response=response,
            expected_status=200,
            expected_fields=[],
            max_time=2.0
        )

    @pytest.mark.get
    def test_get_response_data(self, api_url):
        response = requests.get(api_url + "users")
        data = response.json()  # lista

        assert len(data) > 0
        assert isinstance(data, list)

        first_user = data[0]
        key_structure = ["id", "name", "username", "phone", "address", "website"]

        for i in key_structure:
            assert i in first_user, f"campo {i}, no esta en {first_user}"


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
        print(data)
        assert "id" in data  # verifica que el id esté en la respuesta

        if "createdAt" in data:
            created_at = data["createdAt"]
            current_year = datetime.now().year
            assert str(current_year) in created_at, f"no está en el año actual"


class TestUserWorkflow:

    def test_completo_users(self, api_url):
        print("TESTS ENCANDENADOS: GET, POST, GET, PATCH, DELETE")

        # 1. GET: OBTENER USUARIOS
        response = requests.get(api_url + "users")
        data = response.json()
        check.equal(response.status_code, 200)
        check.is_true(len(data) > 0)

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
        assert user_id is not None

        # 3. GET: VERIFICAR QUE EL USUARIO SE CREÓ
        response = requests.get(api_url + f"users/{user_id}")
        # Como jsonplaceholder no guarda el usuario, esperamos 404
        assert response.status_code in [200, 404]


        # 4. PATCH: ACTUALIZAR EL USUARIO
        update_data = {"phone": fake.phone_number()}
        response = requests.patch(api_url + f"users/{user_id}", update_data)
        assert response.status_code in [200, 204]
        if response.text:
            updated_user = response.json()
            assert updated_user.get("phone") == update_data["phone"]

        # 5. DELETE: ELIMINAR EL USUARIO
        response = requests.delete(api_url + f"users/{user_id}")
        assert response.status_code in [200, 204, 404]

        # 6. GET: VERIFICAR QUE YA NO EXISTE
        response = requests.get(api_url + f"users/{user_id}")
        assert response.status_code in [404, 204]

class TestUserFailures:

    @pytest.mark.get
    def test_usuario_inexistente(self, api_url, driver=None):
        """
        Prueba fallida controlada: intentamos obtener un usuario que no existe.
        Esto forzará un fallo (esperamos 404), pero usamos pytest-check para que
        el test siga corriendo y se refleje en el reporte HTML.
        """
        # GET de un usuario inexistente
        response = requests.get(api_url + "users/99999")

        # Forzamos la verificación a fallar
        check.equal(response.status_code, 200, "Esperábamos 200 pero la API devuelve 404")

        # Seguimos ejecutando más checks aunque el anterior falle
        check.is_true("json" in response.headers.get("Content-Type", ""), "El header debe ser JSON")

        # Capturamos pantalla en caso de fallo
        if driver:
            driver.save_screenshot("reports/fallo_usuario.png")