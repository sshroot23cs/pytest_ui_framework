import allure

class TestSample001:

    @allure.title("First Test Case")
    def test_sample_001(self, browser, get_pages_object):

        browser.get("https://www.google.com/finance/")
        browser.maximize_window()
        get_pages_object.search.check_search_element()
        assert "Google Finance - Stock Market Prices, Real-time Quotes & Business News" in browser.title, "Title is not matching"




