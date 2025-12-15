import pytest
import logging
import pathlib
import time
from selenium import webdriver
from pytest_html import extras



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


logging.basicConfig(
    filename= path_dir/ "historial.log",
    level= logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s – %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger()

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