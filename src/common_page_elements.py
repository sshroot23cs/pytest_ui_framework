from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CommonPageElements:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_page_element(self, locator):
        """
        This function will return the element based on the locator
        :param locator: Dictionary with 'type' and 'value' keys
        :return: WebElement or None
        """
        if not locator or not isinstance(locator, dict):
            print("Invalid locator format")
            return None

        find_by = None
        if locator["type"] == "id":
            find_by = By.ID
        elif locator["type"] == "xpath":
            find_by = By.XPATH
        elif locator["type"] == "css":
            find_by = By.CSS_SELECTOR
        elif locator["type"] == "name":
            find_by = By.NAME
        elif locator["type"] == "class":
            find_by = By.CLASS_NAME
        elif locator["type"] == "link_text":
            find_by = By.LINK_TEXT
        elif locator["type"] == "partial_link_text":
            find_by = By.PARTIAL_LINK_TEXT
        elif locator["type"] == "tag_name":
            find_by = By.TAG_NAME

        if find_by:
            try:
                return self.driver.find_element(find_by, locator["value"])
            except Exception as e:
                print(f"Element not found with locator {locator}: {e}")
                return None
        else:
            print("Invalid locator type {} for locator {}".format(locator['type'], locator['value']))
            return None

    def get_page_elements(self, locator):
        """
        This function will return multiple elements based on the locator
        :param locator: Dictionary with 'type' and 'value' keys
        :return: List of WebElements or empty list
        """
        if not locator or not isinstance(locator, dict):
            print("Invalid locator format")
            return []

        find_by = None
        if locator["type"] == "id":
            find_by = By.ID
        elif locator["type"] == "xpath":
            find_by = By.XPATH
        elif locator["type"] == "css":
            find_by = By.CSS_SELECTOR
        elif locator["type"] == "name":
            find_by = By.NAME
        elif locator["type"] == "class":
            find_by = By.CLASS_NAME
        elif locator["type"] == "link_text":
            find_by = By.LINK_TEXT
        elif locator["type"] == "partial_link_text":
            find_by = By.PARTIAL_LINK_TEXT
        elif locator["type"] == "tag_name":
            find_by = By.TAG_NAME

        if find_by:
            try:
                return self.driver.find_elements(find_by, locator["value"])
            except Exception as e:
                print(f"Elements not found with locator {locator}: {e}")
                return []
        else:
            print("Invalid locator type {} for locator {}".format(locator['type'], locator['value']))
            return []

    def click_element(self, element):
        """
        Click an element (accepts both locator dict and WebElement)
        :param element: WebElement or locator dictionary
        """
        try:
            if isinstance(element, dict):
                # It's a locator, find the element first
                web_element = self.get_page_element(element)
                if web_element:
                    web_element.click()
                else:
                    print(f"Could not find element to click: {element}")
            else:
                # It's already a WebElement
                element.click()
        except Exception as e:
            print("Exception occurred while clicking: {}".format(e))

    def enter_keys_to_element(self, element, keys):
        """
        Send keys to an element (accepts both locator dict and WebElement)
        :param element: WebElement or locator dictionary
        :param keys: Text to send to the element
        :return: The value attribute of the element or None
        """
        try:
            if isinstance(element, dict):
                # It's a locator, find the element first
                web_element = self.get_page_element(element)
                if web_element:
                    web_element.send_keys(keys)
                    return web_element.get_attribute("value")
                else:
                    print(f"Could not find element to send keys: {element}")
                    return None
            else:
                # It's already a WebElement
                element.send_keys(keys)
                return element.get_attribute("value")
        except Exception as e:
            print("Exception occurred while sending keys: {}".format(e))
            return None

    def wait_for_element_to_be_clickable(self, locator, timeout=10):
        """
        Wait for element to be clickable
        :param locator: Dictionary with 'type' and 'value' keys
        :param timeout: Maximum time to wait in seconds
        :return: WebElement or None
        """
        try:
            find_by = self._get_by_type(locator["type"])
            if find_by:
                return self.wait.until(
                    EC.element_to_be_clickable((find_by, locator["value"]))
                )
        except Exception as e:
            print(f"Element not clickable within {timeout} seconds: {e}")
            return None

    def wait_for_element_visible(self, locator, timeout=10):
        """
        Wait for element to be visible
        :param locator: Dictionary with 'type' and 'value' keys
        :param timeout: Maximum time to wait in seconds
        :return: WebElement or None
        """
        try:
            find_by = self._get_by_type(locator["type"])
            if find_by:
                return self.wait.until(
                    EC.visibility_of_element_located((find_by, locator["value"]))
                )
        except Exception as e:
            print(f"Element not visible within {timeout} seconds: {e}")
            return None

    def _get_by_type(self, locator_type):
        """
        Helper method to get By type from string
        :param locator_type: String representation of locator type
        :return: By type or None
        """
        locator_map = {
            "id": By.ID,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "name": By.NAME,
            "class": By.CLASS_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "tag_name": By.TAG_NAME
        }
        return locator_map.get(locator_type)

