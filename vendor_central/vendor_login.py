from utils.webdriver_actions import WebDriverActions
from utils.email_helper import send_email
from utils.email_reader import get_code
from config.config import (
    AMZ_USERNAME,
    AMZ_PASSWORD,
    LOG_IN_LINK,
    LOGGED_IN_ELEMENT,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class VendorLogin:
    SUBMIT_BUTTON = '//input[@type="submit"][@id="signInSubmit"]'
    OTP_INPUT_CLASS = "a-input-text"
    OTP_INPUT_NAME_FORMAT = "otc-%d"

    def __init__(self, driver_actions: WebDriverActions):
        self.driver_actions = driver_actions

    def login(self):
        """Login to the Vendor Central site."""
        self.driver_actions.driver.get(LOG_IN_LINK)
        if self.is_logged_in():
            print("Already logged in.")
        else:
            self.perform_login()
        return self.is_logged_in()

    def is_logged_in(self):
        """Check if we're already logged in."""
        try:
            self.driver_actions.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, LOGGED_IN_ELEMENT))
            )
            return True
        except TimeoutException:
            return False

    def perform_login(self):
        """Perform the actual login operation."""
        self.driver_actions.enter_text(By.NAME, "email", AMZ_USERNAME)
        self.driver_actions.enter_text(By.NAME, "password", AMZ_PASSWORD)
        self.driver_actions.click_element(By.XPATH, self.SUBMIT_BUTTON)

        if not self.is_logged_in():
            self.handle_otp()
        else:
            print("Logged in successfully.")

    def handle_otp(self):
        """Handle OTP if required."""
        code = get_code()
        try:
            for i in range(6):
                self.driver_actions.enter_text(
                    By.NAME, self.OTP_INPUT_NAME_FORMAT % (i + 1), code[i]
                )
        except TimeoutException:
            self.driver_actions.enter_text(By.CLASS_NAME, self.OTP_INPUT_CLASS, code)
        self.driver_actions.click_element(
            By.XPATH, '//input[@type="submit"][@class="a-button-input"]', index=1
        )

        if not self.is_logged_in():
            print("Login failed.")
            send_email(
                "Login Failed",
                "Vendor Central Login Failed. Most likely need to sign in with otp again please try again",
            )
