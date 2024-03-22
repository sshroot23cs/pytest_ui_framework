from selenium.webdriver.common.by import By

class CommonPageElements:

    def __init__(self, driver):
        self.driver = driver

    def get_page_element(self, locator):
        """
        This function will return the element based on the locator
        :param driver:
        :param locator:
        :return:
        """

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
            return self.driver.find_element(find_by, locator["value"])
        else:
            print("Invalid locator type {} for locator {}".format(locator['type'], locator['value']))
            return None

    def click_element(self, element):
        try:
            self.driver.find_element_by_id(element).click()
        except Exception as e:
            print("Exception occurred: {}".format(e))

    def enter_keys_to_element(self, element, keys):
        try:
            self.driver.find_element_by_id(element).send_keys(keys)
            return self.driver.find_element_by_id(element).get_attribute("value")
        except Exception as e:
            print("Exception occurred: {}".format(e))

