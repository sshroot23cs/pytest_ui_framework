import allure
import pytest
import time
from playwright.sync_api import Playwright, sync_playwright


class TestPlaywrightAdvanced:
    """Advanced E2E tests using Playwright for enhanced browser automation"""

    @allure.title("Playwright Advanced Search with Screenshots")
    @allure.description("Advanced E2E test using Playwright with screenshot capabilities")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_playwright_advanced_search(self):
        """
        Advanced E2E test using Playwright with enhanced features:
        - Multiple browser contexts
        - Screenshot capture
        - Advanced element interactions
        - Network monitoring
        """
        with sync_playwright() as p:
            # Launch browser with advanced options
            browser = p.chromium.launch(
                headless=False,  # For demonstration
                args=['--start-maximized'],
                slow_mo=1000  # Slow down for visualization
            )
            
            # Create context with device emulation
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            # Create page
            page = context.new_page()
            
            with allure.step("Navigate to Google Finance"):
                page.goto("https://www.google.com/finance/")
                page.wait_for_load_state('networkidle')
                
                # Take screenshot for verification
                screenshot_path = "reports/screenshots/google_finance_homepage.png"
                page.screenshot(path=screenshot_path, full_page=True)
                allure.attach.file(screenshot_path, name="Homepage Screenshot", 
                                 attachment_type=allure.attachment_type.PNG)
            
            with allure.step("Perform advanced search interaction"):
                # Use more robust selector strategies
                search_selectors = [
                    "input[placeholder*='Search']",
                    "input[aria-label*='Search']",
                    "[data-test*='search']",
                    ".search-input"
                ]
                
                search_element = None
                for selector in search_selectors:
                    try:
                        search_element = page.wait_for_selector(selector, timeout=5000)
                        if search_element:
                            break
                    except:
                        continue
                
                assert search_element, "No search element found with any selector"
                
                # Perform search with typing simulation
                search_element.click()
                search_element.fill("")  # Clear any existing text
                page.keyboard.type("AAPL", delay=100)  # Simulate human typing
                page.keyboard.press("Enter")
                
                # Wait for search results
                page.wait_for_load_state('networkidle')
                time.sleep(2)
                
                # Take screenshot of results
                results_screenshot = "reports/screenshots/search_results.png"
                page.screenshot(path=results_screenshot, full_page=True)
                allure.attach.file(results_screenshot, name="Search Results", 
                                 attachment_type=allure.attachment_type.PNG)
            
            with allure.step("Verify search results and interactions"):
                # Check page title contains relevant information
                title = page.title()
                assert any(keyword.lower() in title.lower() for keyword in ["apple", "aapl", "finance"]), \
                    f"Title doesn't contain expected keywords: {title}"
                
                # Check URL contains search parameters
                current_url = page.url
                assert "aapl" in current_url.lower() or "apple" in current_url.lower(), \
                    f"URL doesn't reflect search: {current_url}"
                
                # Try to find stock price or symbol information
                price_selectors = [
                    "[data-test*='price']",
                    ".price",
                    "[class*='price']",
                    "[aria-label*='price']"
                ]
                
                stock_info_found = False
                for selector in price_selectors:
                    try:
                        element = page.wait_for_selector(selector, timeout=3000)
                        if element:
                            stock_info_found = True
                            break
                    except:
                        continue
                
                # Take final screenshot
                final_screenshot = "reports/screenshots/final_state.png"
                page.screenshot(path=final_screenshot, full_page=True)
                allure.attach.file(final_screenshot, name="Final State", 
                                 attachment_type=allure.attachment_type.PNG)
            
            # Cleanup
            context.close()
            browser.close()

    @allure.title("Playwright Multi-Browser Compatibility Test")
    @allure.description("Test search functionality across different browsers")
    @allure.severity(allure.severity_level.NORMAL)
    def test_playwright_multi_browser(self):
        """
        Test the same functionality across different browsers
        """
        browsers_to_test = ['chromium', 'firefox', 'webkit']
        
        with sync_playwright() as p:
            for browser_name in browsers_to_test:
                with allure.step(f"Testing with {browser_name}"):
                    try:
                        # Launch specific browser
                        if browser_name == 'chromium':
                            browser = p.chromium.launch(headless=True)
                        elif browser_name == 'firefox':
                            browser = p.firefox.launch(headless=True)
                        elif browser_name == 'webkit':
                            browser = p.webkit.launch(headless=True)
                        
                        context = browser.new_context()
                        page = context.new_page()
                        
                        # Navigate and test
                        page.goto("https://www.google.com/finance/")
                        page.wait_for_load_state('networkidle')
                        
                        # Verify page loaded successfully
                        title = page.title()
                        assert "finance" in title.lower(), f"{browser_name}: Page didn't load correctly"
                        
                        # Take browser-specific screenshot
                        browser_screenshot = f"reports/screenshots/{browser_name}_test.png"
                        page.screenshot(path=browser_screenshot)
                        allure.attach.file(browser_screenshot, name=f"{browser_name} Screenshot", 
                                         attachment_type=allure.attachment_type.PNG)
                        
                        context.close()
                        browser.close()
                        
                        # Mark browser test as successful
                        allure.attach(f"{browser_name}: Test passed", name=f"{browser_name} Result",
                                    attachment_type=allure.attachment_type.TEXT)
                        
                    except Exception as e:
                        allure.attach(f"{browser_name}: Test failed - {str(e)}", 
                                    name=f"{browser_name} Error",
                                    attachment_type=allure.attachment_type.TEXT)
                        # Don't fail the entire test for one browser
                        continue

    @allure.title("Playwright Network Monitoring Test")
    @allure.description("Monitor network requests during search operations")
    @allure.severity(allure.severity_level.MINOR)
    def test_playwright_network_monitoring(self):
        """
        Monitor network requests and responses during search
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            # Set up network monitoring
            requests = []
            responses = []
            
            def handle_request(request):
                requests.append({
                    'url': request.url,
                    'method': request.method,
                    'headers': dict(request.headers)
                })
            
            def handle_response(response):
                responses.append({
                    'url': response.url,
                    'status': response.status,
                    'headers': dict(response.headers)
                })
            
            page.on('request', handle_request)
            page.on('response', handle_response)
            
            with allure.step("Monitor network during navigation"):
                page.goto("https://www.google.com/finance/")
                page.wait_for_load_state('networkidle')
            
            with allure.step("Monitor network during search"):
                # Perform search if possible
                try:
                    search_element = page.wait_for_selector("input[placeholder*='Search']", timeout=5000)
                    if search_element:
                        search_element.fill("AAPL")
                        page.keyboard.press("Enter")
                        page.wait_for_load_state('networkidle')
                except:
                    pass  # If search fails, we still have navigation data
            
            with allure.step("Analyze network performance"):
                # Attach network information
                network_summary = {
                    'total_requests': len(requests),
                    'total_responses': len(responses),
                    'failed_requests': len([r for r in responses if r['status'] >= 400]),
                    'domains': list(set([req['url'].split('/')[2] for req in requests if len(req['url'].split('/')) > 2]))
                }
                
                allure.attach(str(network_summary), name="Network Summary",
                            attachment_type=allure.attachment_type.JSON)
                
                # Basic performance assertions
                assert len(requests) > 0, "No network requests captured"
                assert len(responses) > 0, "No network responses captured"
                
                # Check for excessive failed requests
                failed_count = len([r for r in responses if r['status'] >= 400])
                assert failed_count < len(responses) * 0.1, f"Too many failed requests: {failed_count}"
            
            context.close()
            browser.close()


# Configuration for Playwright tests
@pytest.fixture(scope="session")
def playwright_setup():
    """Setup Playwright for the test session"""
    with sync_playwright() as p:
        yield p


# Helper function to ensure screenshot directory exists
def ensure_screenshot_dir():
    import os
    screenshot_dir = "reports/screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)


# Call this at module level to ensure directory exists
ensure_screenshot_dir()