PRUEBAS-API - README
====================

Este proyecto tiene como objetivo practicar y demostrar pruebas automatizadas sobre una API pública
(`jsonplaceholder.typicode.com`). Se implementa un flujo completo de testing que incluye operaciones
GET, POST, PATCH y DELETE, validaciones de respuesta, logging detallado y generación de reportes HTML
con evidencia visual (capturas de pantalla en fallos).

Propósito del proyecto
----------------------
- Practicar pruebas automatizadas sobre APIs.
- Validar respuestas y códigos de estado.
- Generar reportes HTML y logs de ejecución.

Tecnologías utilizadas
----------------------
- Python (es necesario tener instalado Python 3.10 o superior)
- Pytest – framework de testing
- Pytest-HTML – generación de reportes HTML
- Pytest-Check – validaciones que no interrumpen la ejecución
- Faker – generación de datos aleatorios para pruebas
- Requests – librería para consumir APIs
- Selenium (opcional) – para capturas de pantalla en pruebas fallidas
- Logging (módulo estándar de Python) – registro detallado de la ejecución

Estructura del proyecto
-----------------------
Pruebas-API/
│
├── test_peticiones_http.py   # Archivo principal con las pruebas de API
├── conftest.py               # Configuración de fixtures, logging y hooks
├── pytest.ini                # Configuración de pytest y reportes HTML
├── reports/                  # Carpeta de reportes HTML y capturas
└── logs/                     # Carpeta de logs de ejecución

Instalación de dependencias
---------------------------
1. Asegurate de tener instalado **Python 3.10 o superior**.
2. Cloná el repositorio y luego instalá las dependencias necesarias:

    git clone https://github.com/mariasmarchi/Pruebas-API.git
    cd Pruebas-API
    pip install -r requirements.txt

Ejecución de pruebas
--------------------
Para ejecutar todas las pruebas:

    pytest

Los reportes HTML se generarán en la carpeta `reports/` y los logs en la carpeta `logs/`.

Notas finales
-------------
- Se utiliza Pytest con fixtures y hooks para mantener el código organizado.
- Los reportes HTML incluyen evidencia visual en caso de fallos.
- Los datos de prueba se generan dinámicamente con Faker.
