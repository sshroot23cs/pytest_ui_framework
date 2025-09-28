from src.common_page_elements import CommonPageElements
from src.helper import Helper
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class SearchPage(CommonPageElements):

    LOCATOR_FILE = "search_locators.yaml"

    def __init__(self, driver):
        super().__init__(driver)
        self.pageHelper = Helper()
        self.page_locators = self.pageHelper.get_locators(self.LOCATOR_FILE)
        self.wait = WebDriverWait(driver, 10)

    def check_search_element(self):
        """Check if search element is present and return the element"""
        try:
            ele = self.get_page_element(self.page_locators["search-box"])
            return ele if ele else False
        except:
            # Try alternative search input locator
            try:
                ele = self.get_page_element(self.page_locators["search-input"])
                return ele if ele else False
            except:
                return False

    def enter_text_in_search_box(self, element, text):
        """Enter text in search box using element and text"""
        self.enter_keys_to_element(element, text)
        return True

    def search_for_stock(self, stock_symbol):
        """
        Perform search for a stock symbol
        Args:
            stock_symbol (str): Stock symbol to search for (e.g., 'AAPL')
        Returns:
            bool: True if search was successful, False otherwise
        """
        try:
            # Get search element
            search_element = self.check_search_element()
            if not search_element:
                return False
            
            # Clear any existing text and enter the stock symbol
            search_element.clear()
            search_element.send_keys(stock_symbol)
            
            # Press Enter to search
            search_element.send_keys(Keys.ENTER)
            
            # Wait a moment for the search to process
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"Error during search: {e}")
            return False

    def clear_and_search_stock(self, stock_symbol):
        """
        Clear search box and search for new stock symbol
        Args:
            stock_symbol (str): Stock symbol to search for
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            search_element = self.check_search_element()
            if not search_element:
                return False
            
            # Clear the search box completely
            search_element.clear()
            search_element.send_keys(Keys.CONTROL + "a")  # Select all
            search_element.send_keys(Keys.DELETE)  # Delete selected
            
            # Enter new search term
            search_element.send_keys(stock_symbol)
            search_element.send_keys(Keys.ENTER)
            
            return True
            
        except Exception as e:
            print(f"Error during clear and search: {e}")
            return False

    def clear_search_box(self):
        """
        Clear the search box
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            search_element = self.check_search_element()
            if not search_element:
                return False
            
            search_element.clear()
            return True
            
        except Exception as e:
            print(f"Error clearing search box: {e}")
            return False

    def get_search_results(self):
        """
        Get search results elements
        Returns:
            list: List of search result elements or empty list if none found
        """
        try:
            results_locator = self.page_locators.get("search-results")
            if results_locator:
                # Wait for results to appear
                self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, results_locator["value"])
                ))
                return self.driver.find_elements(
                    By.CSS_SELECTOR, results_locator["value"]
                )
            return []
        except:
            return []

    def verify_stock_information_displayed(self):
        """
        Verify that stock information is displayed on the page
        Returns:
            bool: True if stock information is found, False otherwise
        """
        try:
            # Check for stock price element
            price_element = self.get_page_element(self.page_locators.get("stock-price", {}))
            
            # Check for stock symbol element
            symbol_element = self.get_page_element(self.page_locators.get("stock-symbol", {}))
            
            # Return True if either price or symbol is found
            return bool(price_element or symbol_element)
            
        except:
            return False

    def wait_for_search_suggestions(self, timeout=5):
        """
        Wait for search suggestions to appear
        Args:
            timeout (int): Timeout in seconds
        Returns:
            bool: True if suggestions appear, False otherwise
        """
        try:
            suggestions_locator = self.page_locators.get("search-suggestions")
            if suggestions_locator:
                element = self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, suggestions_locator["value"])
                    ),
                    timeout
                )
                return bool(element)
            return False
        except:
            return False

