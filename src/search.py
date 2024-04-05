from src.common_page_elements import CommonPageElements
from src.helper import Helper
class SearchPage(CommonPageElements):

    LOCATOR_FILE = "search_locators.yaml"

    def __init__(self, driver):
        super().__init__(driver)
        self.pageHelper = Helper()
        self.page_locators = self.pageHelper.get_locators(self.LOCATOR_FILE)

    def check_search_element(self):
        ele = self.get_page_element(self.page_locators["search-box"])
        return ele if ele else False

    def enter_text_in_search_box(self, element, text):
        self.enter_keys_to_element(element, text)
        return True

