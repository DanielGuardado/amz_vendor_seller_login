from vendor_central.vendor_login import VendorLogin
from vendor_central.vendor_data_fetcher import VendorDataFetcher
from utils.webdriver_actions import WebDriverActions
from driver import get_default_driver


class VendorCentral:
    def __init__(self, driver=None):
        if driver is None:
            self.driver = get_default_driver()
        else:
            self.driver = driver
        self.driver_actions = WebDriverActions(self.driver)
        self.login_module = VendorLogin(self.driver_actions)
        self.data_fetcher = VendorDataFetcher(self.driver_actions)

    def login(self):
        return self.login_module.login()

    def fetch_vendor_data(self):
        session_cookies = self.driver_actions.get_session_cookies()
        return self.data_fetcher.fetch_vendor_data(session_cookies)
