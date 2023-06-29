from utils.webdriver_actions import WebDriverActions
from utils.gmail_helper import get_code, send_email

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class Login:
    SUBMIT_BUTTON = '//input[@type="submit"][@id="signInSubmit"]'
    OTP_INPUT_CLASS = "a-input-text"
    OTP_INPUT_NAME_FORMAT = "otc-%d"

    def __init__(
        self,
        driver_actions: WebDriverActions,
        username,
        password,
        login_link,
        logged_in_element,
        sender_email,
        recipient_emails,
        type,
    ):
        self.driver_actions = driver_actions
        self.username = username
        self.password = password
        self.login_link = login_link
        self.logged_in_element = logged_in_element
        self.sender_email = sender_email
        self.recipient_emails = recipient_emails
        self.type = type

    def login(self):
        """Login to the Vendor Central site."""
        self.driver_actions.get(self.login_link)
        if self.is_logged_in():
            print("Already logged in.")
        else:
            self.perform_login()
        return self.is_logged_in()

    def is_logged_in(self):
        """Check if we're already logged in."""
        try:
            self.driver_actions.wait.until(
                EC.presence_of_element_located((By.XPATH, self.logged_in_element))
            )
            return True
        except TimeoutException:
            return False

    def perform_login(self):
        """Perform the actual login operation."""
        self.driver_actions.enter_text(By.NAME, "email", self.username)
        self.driver_actions.enter_text(By.NAME, "password", self.password)
        self.driver_actions.click_element(By.XPATH, self.SUBMIT_BUTTON)

        if not self.is_logged_in():
            self.handle_otp()
        else:
            print("Logged in successfully.")

    def handle_otp(self):
        """Handle OTP if required."""
        if self.type == "vendor_central":
            code = get_code()
            try:
                for i in range(6):
                    self.driver_actions.enter_text(
                        By.NAME, self.OTP_INPUT_NAME_FORMAT % (i + 1), code[i]
                    )
            except TimeoutException:
                self.driver_actions.enter_text(
                    By.CLASS_NAME, self.OTP_INPUT_CLASS, code
                )
            self.driver_actions.click_element(
                By.XPATH, '//input[@type="submit"][@class="a-button-input"]', index=1
            )
        elif self.type == "seller_central":
            code = input("Please enter your code: ")
            self.driver_actions.enter_text(By.NAME, "otpCode", code)
            self.driver_actions.click_element(By.NAME, "rememberDevice")
            self.driver_actions.click_element(
                By.XPATH, "//input[@id='auth-signin-button']"
            )

        if (
            self.driver_actions.current_url
            == "https://sellercentral.amazon.com/authorization/select-account?returnTo=%2Fgp%2Fssof%2Fshipping-queue.html%2Fref%253Dxx_fbashipq_dnav_xx&mons_redirect=remedy_url"
        ):
            self.driver_actions.click_element(
                By.XPATH, "//div[contains(text(),'United States')]"
            )
            self.driver_actions.click_element(
                By.XPATH, "//button[normalize-space()='Select Account']"
            )

        if not self.is_logged_in():
            print("Login failed.")
            send_email(
                "Login Failed",
                "Vendor Central Login Failed. Most likely need to sign in with otp again please try again",
                self.sender_email,
                self.recipient_emails,
            )
