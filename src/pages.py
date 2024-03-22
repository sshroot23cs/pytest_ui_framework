
from src.search import SearchPage


class Pages:

    def __init__(self, driver):
        self.search = SearchPage(driver)

