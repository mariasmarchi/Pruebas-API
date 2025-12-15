import pytest
import logging
import pathlib
import time
from selenium import webdriver
from pytest_html import extras

# Carpeta de reportes
path_dir = pathlib.Path("reports")
path_dir.mkdir(exist_ok=True)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Ejecuta el test
    outcome = yield
    rep = outcome.get_result()

    # Solo si falla en la fase de ejecución
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot_path = path_dir / f"{item.name}.png"
            driver.save_screenshot(str(screenshot_path))
            # Adjuntar al reporte HTML
            if "pytest_html" in item.config.pluginmanager.plugins:
                extra = getattr(rep, "extra", [])
                from pytest_html import extras
                extra.append(extras.image(str(screenshot_path)))
                rep.extra = extra


@pytest.fixture
def api_url():
    return 'https://jsonplaceholder.typicode.com/'



#ef pytest_html_summers(prefix):

#     prefix.extend([
#         '<h2>MISION IMPOSIBLE CUMPLIDA</h2>',
#         '<div style="background:gold"></div>'
#     ])


def pytest_html_report_title(report):
    """Cambia el título de la pestaña del navegador"""
    report.title = "TalentoLab - Reporte de Testing"

path_dir = pathlib.Path('logs')
path_dir.mkdir(exist_ok=True)

# Carpeta de logs
path_dir = pathlib.Path("logs")
path_dir.mkdir(exist_ok=True)

logging.basicConfig(
    filename=path_dir / "historial.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

logger = logging.getLogger(__name__)

@pytest.fixture
def api_url(request):
    logger.info(f"Inicializando fixture api_url para el test: {request.node.name}")
    return "https://jsonplaceholder.typicode.com/"

# Hook para registrar resultado de cada test sin íconos
def pytest_runtest_logreport(report):
    if report.when == "call":  # solo en ejecución
        if report.passed:
            logger.info(f"Test '{report.nodeid}' PASSED en {report.duration:.2f}s")
        elif report.failed:
            logger.error(f"Test '{report.nodeid}' FAILED en {report.duration:.2f}s")
        elif report.skipped:
            logger.warning(f"Test '{report.nodeid}' SKIPPED")



#@pytest.fixture
#def api_url():
#    logger.info("Fixture api_url inicializado")
#    return 'https://jsonplaceholder.typicode.com/'

#def test_api(api_url):
#    logger.info("Ejecutando test_api con URL: %s", api_url)
#    assert "https" in api_url

# 1. Carpeta para screenshots
#target = pathlib.Path('reports/screens')
#target.mkdir(parents=True, exist_ok=True)

# 2. Fixture simple
#@pytest.fixture
#def driver():
#    """Fixture para Chrome"""
#    d = webdriver.Chrome()
#    d.get("https://google.com")
#    time.sleep(2)  # Espera a que cargue
#    yield d
#    d.quit()

#@pytest.hookimpl(hookwrapper=True)
#def pytest_runtest_makereport(item, call):
#    outcome = yield
#    report = outcome.get_result()#

 #   if report.when == 'call' and report.failed:
#        if 'driver' in item.fixturenames:
#            driver = item.funcargs['driver']

#            file_name = target / f"{item.name}.png"
#            driver.save_screenshot(str(file_name))

#            report.extra = getattr(report, 'extra', [])

#            report.extra.append(extras.png(str(file_name)))