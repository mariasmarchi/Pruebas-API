import requests
import pytest
import pytest_check as check
from faker import Faker
from datetime import datetime

fake =Faker()

def validate_api_response(response, expected_status,expected_fields=None, max_time=1.0):
    """Función helper para validar respuestas API con los 5 niveles"""
    # Nivel 1: Status
    assert response.status_code == expected_status
    # Nivel 2: Headers
    if expected_status != 204: # 204 No Content puede no tener Content-Type
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
        respose = requests.get(api_url + "users")
        data = validate_api_response(
            response= respose,
            expected_status=200,
            expected_fields=[],
            max_time=2.0
        )

        #assert respose.status_code ==200

    @pytest.mark.get
    def test_get_response_data(self, api_url):
        response = requests.get(api_url + "users")
        data = response.json()  #lista
        
        assert len(data) > 0
        assert isinstance(data, list)

        first_user = data[0]
        key_structure = ["id", "name", "username", "phone", "address", "website"]

        for i in key_structure:
            assert i in first_user , f"campo {i}, no esta en {first_user}"





class TestPostUser:


    @pytest.mark.post
    def test_post_response_code(self, api_url):
        new_user = {
            "name":fake.name(),
            "email" : fake.email(),
            "phone": fake.phone_number()
            #"createdAt": fake.date_time_this_year()
        }

        response = requests.post(api_url + "users", new_user)
        assert response.status_code == 201

        data = response.json()
        print(data)
        assert "id" in data  #verifica que el id este en la respuesta

        if "createdAt" in data:
            created_at = data["createdAt"]
            current_year = datetime.now().year
            assert str(current_year) in created_at, f"no esta en el año actual"
           

class TestUserWorkflow:

    def test_completo_users(self, api_url):
        print("TESTS ENCANDENADOS: GET, POST, GET, PATCH, DELETE")
        print("1. GET OBTENER USUARIOS")
        #GET:OBTENER LOS USUARIOS
        respose = requests.get(api_url + "users")
        data = respose.json()  
        check.equal(respose.status_code, 200)
        check.is_true(len(data) > 0)
        print("2. POST CREAR USUARIO") #esto no se visualiza
        #CREAR UN USUARIO  
        new_user = {
            "name":fake.name(),
            "email" : fake.email(),
            "phone": fake.phone_number()
            #"createdAt": fake.date_time_this_year()
        }

        response = requests.post(api_url + "users", new_user)
        assert response.status_code == 201