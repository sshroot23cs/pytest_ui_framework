import os
import allure
import pytest
from selenium import webdriver
from src.pages import Pages

SCREENSHOT_PATH = os.path.join(os.path.dirname(__file__), "../screenshots")

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Type in browser type")

@pytest.fixture(scope="session")
def browser_type(request):
    return request.config.getoption("--browser").lower()

@pytest.fixture(scope="function")
def browser(request, browser_type):
    request.node.name = request.node.name.replace(" ", "_")
    # Initialize ChromeDriver
    if browser_type == "chrome":
        driver = webdriver.Chrome()
    elif browser_type == "firefox":
        driver = webdriver.Firefox()

    # Return the driver object at the end of setup
    yield driver

    # For cleanup, quit the driver
    driver.quit()

@pytest.fixture(scope="function")
def get_pages_object(browser):
    pages_obj = Pages(browser)
    return pages_obj
