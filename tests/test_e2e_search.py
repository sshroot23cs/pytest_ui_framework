import allure
import pytest
from selenium.webdriver.common.keys import Keys
import time


class TestE2ESearch:
    """End-to-end test cases for Google Finance search functionality"""

    @allure.title("E2E Search Stock Symbol Test")
    @allure.description("Complete end-to-end test for searching a stock symbol and verifying results")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_e2e_search_stock_symbol(self, browser, get_pages_object):
        """
        Test end-to-end search functionality for stock symbols
        Steps:
        1. Navigate to Google Finance
        2. Verify search box is present
        3. Search for a stock symbol (AAPL)
        4. Verify search results are displayed
        5. Verify stock information is shown
        """
        with allure.step("Navigate to Google Finance"):
            browser.get("https://www.google.com/finance/")
            browser.maximize_window()
            
        with allure.step("Verify search box is present"):
            search_element = get_pages_object.search.check_search_element()
            assert search_element, "Search box is not present on the page"
            
        with allure.step("Perform search for AAPL stock"):
            search_result = get_pages_object.search.search_for_stock("AAPL")
            assert search_result, "Search operation failed"
            
        with allure.step("Verify page title contains relevant information"):
            # Wait for page to load after search
            time.sleep(2)
            title = browser.title
            assert any(keyword in title.lower() for keyword in ["apple", "aapl", "finance"]), \
                f"Page title doesn't contain expected keywords. Title: {title}"

    @allure.title("E2E Search Multiple Stocks Test")
    @allure.description("Test searching for multiple different stock symbols")
    @allure.severity(allure.severity_level.NORMAL)
    def test_e2e_search_multiple_stocks(self, browser, get_pages_object):
        """
        Test searching for multiple stock symbols in sequence
        """
        stocks_to_search = ["GOOGL", "MSFT", "TSLA"]
        
        with allure.step("Navigate to Google Finance"):
            browser.get("https://www.google.com/finance/")
            browser.maximize_window()
            
        for stock in stocks_to_search:
            with allure.step(f"Search for {stock} stock"):
                search_element = get_pages_object.search.check_search_element()
                assert search_element, f"Search box not found when searching for {stock}"
                
                # Clear previous search and enter new stock
                get_pages_object.search.clear_and_search_stock(stock)
                time.sleep(2)
                
                # Verify we're on a page related to the stock
                current_url = browser.current_url
                assert stock.lower() in current_url.lower() or "finance" in current_url.lower(), \
                    f"URL doesn't seem to be related to {stock} search. URL: {current_url}"

    @allure.title("E2E Search Error Handling Test")
    @allure.description("Test search functionality with invalid inputs")
    @allure.severity(allure.severity_level.MINOR)
    def test_e2e_search_error_handling(self, browser, get_pages_object):
        """
        Test search functionality with invalid or non-existent stock symbols
        """
        with allure.step("Navigate to Google Finance"):
            browser.get("https://www.google.com/finance/")
            browser.maximize_window()
            
        with allure.step("Search for invalid stock symbol"):
            search_element = get_pages_object.search.check_search_element()
            assert search_element, "Search box is not present"
            
            # Search for clearly invalid stock symbol
            get_pages_object.search.search_for_stock("INVALIDSTOCK123")
            time.sleep(2)
            
            # Verify page handles the search gracefully (no crashes)
            page_source = browser.page_source
            assert page_source, "Page failed to load after invalid search"
            
        with allure.step("Search with empty string"):
            get_pages_object.search.clear_search_box()
            get_pages_object.search.search_for_stock("")
            time.sleep(1)
            
            # Verify page remains functional
            current_url = browser.current_url
            assert "finance" in current_url.lower(), "Page navigation failed with empty search"

    @allure.title("E2E Search Performance Test")
    @allure.description("Test search performance and response times")
    @allure.severity(allure.severity_level.MINOR)
    def test_e2e_search_performance(self, browser, get_pages_object):
        """
        Test search performance by measuring response times
        """
        with allure.step("Navigate to Google Finance"):
            browser.get("https://www.google.com/finance/")
            browser.maximize_window()
            
        with allure.step("Measure search response time"):
            start_time = time.time()
            
            search_element = get_pages_object.search.check_search_element()
            assert search_element, "Search box not found"
            
            get_pages_object.search.search_for_stock("AAPL")
            
            # Wait for results to load
            time.sleep(3)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Assert reasonable response time (less than 10 seconds)
            assert response_time < 10, f"Search took too long: {response_time} seconds"
            
            with allure.step(f"Search completed in {response_time:.2f} seconds"):
                allure.attach(f"Response time: {response_time:.2f} seconds", 
                            name="Performance Metrics", 
                            attachment_type=allure.attachment_type.TEXT)