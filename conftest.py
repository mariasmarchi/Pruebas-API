import pytest
import logging
import pathlib
from selenium import webdriver
from pytest_html import extras

# Carpeta de reportes
reports_dir = pathlib.Path("reports")
reports_dir.mkdir(exist_ok=True)

# Carpeta de logs
logs_dir = pathlib.Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configuración de logging
logging.basicConfig(
    filename=logs_dir / "historial.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# Fixture para la URL base
@pytest.fixture
def api_url(request):
    logger.info(f"Inicializando fixture api_url para el test: {request.node.name}")
    return "https://jsonplaceholder.typicode.com/"

# Hook para título del reporte HTML
def pytest_html_report_title(report):
    report.title = "TalentoLab - Reporte de Testing"

# Hook para registrar resultado de cada test
def pytest_runtest_logreport(report):
    if report.when == "call":  # solo fase de ejecución
        if report.passed:
            logger.info(f"Test '{report.nodeid}' PASSED en {report.duration:.2f}s")
        elif report.failed:
            logger.error(f"Test '{report.nodeid}' FAILED en {report.duration:.2f}s")
        elif report.skipped:
            logger.warning(f"Test '{report.nodeid}' SKIPPED")

# Hook para capturas de pantalla en fallos
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot_path = reports_dir / f"{item.name}.png"
            driver.save_screenshot(str(screenshot_path))
            if "pytest_html" in item.config.pluginmanager.plugins:
                extra = getattr(rep, "extra", [])
                extra.append(extras.image(str(screenshot_path)))
                rep.extra = extra

# Ejemplo de fixture opcional para Selenium
# @pytest.fixture
# def driver():
#     d = webdriver.Chrome()
#     yield d
#     d.quit()
