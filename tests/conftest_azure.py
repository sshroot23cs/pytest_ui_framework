# Enhanced conftest.py for Azure Container deployment
# Adds cloud-specific configurations and Azure Storage integration

import os
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from src.pages import Pages
from azure.storage.blob import BlobServiceClient
import json
from datetime import datetime

SCREENSHOT_PATH = os.path.join(os.path.dirname(__file__), "../screenshots")

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Type in browser type")
    parser.addoption("--headless", action="store_true", default=False, help="Run browser in headless mode")
    parser.addoption("--azure-upload", action="store_true", default=False, help="Upload results to Azure Storage")

@pytest.fixture(scope="session")
def browser_type(request):
    return request.config.getoption("--browser").lower()

@pytest.fixture(scope="session")
def headless_mode(request):
    return request.config.getoption("--headless") or os.getenv("HEADLESS", "false").lower() == "true"

@pytest.fixture(scope="session")
def azure_upload_enabled(request):
    return request.config.getoption("--azure-upload") or os.getenv("AZURE_UPLOAD", "false").lower() == "true"

@pytest.fixture(scope="function")
def browser(request, browser_type, headless_mode):
    request.node.name = request.node.name.replace(" ", "_")
    
    # Configure Chrome for container environment
    if browser_type == "chrome":
        chrome_options = ChromeOptions()
        
        if headless_mode:
            chrome_options.add_argument("--headless")
        
        # Container-specific Chrome arguments
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Override Chrome binary if specified
        chrome_bin = os.getenv("CHROME_BIN")
        if chrome_bin:
            chrome_options.binary_location = chrome_bin
            
        driver = webdriver.Chrome(options=chrome_options)
        
    elif browser_type == "firefox":
        firefox_options = FirefoxOptions()
        
        if headless_mode:
            firefox_options.add_argument("--headless")
            
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        
        driver = webdriver.Firefox(options=firefox_options)
    
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")

    # Return the driver object at the end of setup
    yield driver

    # For cleanup, quit the driver
    driver.quit()

@pytest.fixture(scope="function")
def get_pages_object(browser):
    pages_obj = Pages(browser)
    return pages_obj

@pytest.fixture(scope="session")
def azure_blob_client(azure_upload_enabled):
    """Azure Blob Storage client for uploading test results"""
    if not azure_upload_enabled:
        return None
        
    account_name = os.getenv("AZURE_STORAGE_ACCOUNT")
    account_key = os.getenv("AZURE_STORAGE_KEY")
    
    if account_name and account_key:
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
        return BlobServiceClient.from_connection_string(connection_string)
    
    return None

def pytest_sessionstart(session):
    """Called after the Session object has been created"""
    print(f"Starting test session in environment: {os.getenv('ENVIRONMENT', 'local')}")
    
    # Create necessary directories
    os.makedirs(SCREENSHOT_PATH, exist_ok=True)
    os.makedirs("reports/allure-results", exist_ok=True)

def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished"""
    print(f"Test session finished with exit status: {exitstatus}")
    
    # Upload results to Azure if enabled
    azure_upload_enabled = session.config.getoption("--azure-upload") or os.getenv("AZURE_UPLOAD", "false").lower() == "true"
    
    if azure_upload_enabled:
        upload_results_to_azure()

def pytest_runtest_makereport(item, call):
    """Hook to capture test results and create custom reports"""
    if call.when == "call":
        # Add environment information to Allure report
        allure.attach(
            json.dumps({
                "environment": os.getenv("ENVIRONMENT", "local"),
                "browser": item.config.getoption("--browser"),
                "headless": str(item.config.getoption("--headless") or os.getenv("HEADLESS", "false")),
                "azure_enabled": str(item.config.getoption("--azure-upload") or os.getenv("AZURE_UPLOAD", "false")),
                "timestamp": datetime.now().isoformat()
            }, indent=2),
            name="Test Environment",
            attachment_type=allure.attachment_type.JSON
        )

def upload_results_to_azure():
    """Upload test results to Azure Blob Storage"""
    try:
        account_name = os.getenv("AZURE_STORAGE_ACCOUNT")
        account_key = os.getenv("AZURE_STORAGE_KEY")
        
        if not account_name or not account_key:
            print("Azure Storage credentials not found, skipping upload")
            return
            
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
        blob_client = BlobServiceClient.from_connection_string(connection_string)
        
        container_name = "test-reports"
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        # Upload Allure results
        allure_dir = "reports/allure-results"
        if os.path.exists(allure_dir):
            for root, dirs, files in os.walk(allure_dir):
                for file in files:
                    local_path = os.path.join(root, file)
                    blob_name = f"{timestamp}/allure-results/{file}"
                    
                    blob_client_instance = blob_client.get_blob_client(
                        container=container_name,
                        blob=blob_name
                    )
                    
                    with open(local_path, "rb") as data:
                        blob_client_instance.upload_blob(data, overwrite=True)
        
        # Upload screenshots
        if os.path.exists(SCREENSHOT_PATH):
            for root, dirs, files in os.walk(SCREENSHOT_PATH):
                for file in files:
                    if file.endswith(('.png', '.jpg', '.jpeg')):
                        local_path = os.path.join(root, file)
                        blob_name = f"{timestamp}/screenshots/{file}"
                        
                        blob_client_instance = blob_client.get_blob_client(
                            container=container_name,
                            blob=blob_name
                        )
                        
                        with open(local_path, "rb") as data:
                            blob_client_instance.upload_blob(data, overwrite=True)
        
        print(f"Test results uploaded to Azure Storage: {container_name}/{timestamp}")
        
    except Exception as e:
        print(f"Failed to upload results to Azure: {str(e)}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Try to capture screenshot if browser is available
        try:
            driver = item.funcargs.get('browser')
            if driver:
                screenshot_name = f"failure_{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot_path = os.path.join(SCREENSHOT_PATH, screenshot_name)
                driver.save_screenshot(screenshot_path)
                
                # Attach to Allure report
                allure.attach.file(
                    screenshot_path,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Failed to capture screenshot: {str(e)}")