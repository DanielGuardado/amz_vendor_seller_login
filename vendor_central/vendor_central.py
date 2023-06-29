from vendor_central.vendor_login import VendorLogin
from utils.webdriver_actions import WebDriverActions
from utils.driver import ChromeDriver


class VendorCentral:
    def __init__(
        self,
        username,
        password,
        login_link,
        logged_in_element,
        sender_email,
        recipient_emails,
        chrome_driver=None,
        download_path=None,
    ):
        if chrome_driver is None:
            chrome_driver = ChromeDriver(download_path)
        self.driver_actions = WebDriverActions(chrome_driver)
        self.login_module = VendorLogin(
            self.driver_actions,
            username,
            password,
            login_link,
            logged_in_element,
            sender_email,
            recipient_emails,
        )

    def login(self):
        return self.login_module.login()
