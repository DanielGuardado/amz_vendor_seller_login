from utils.webdriver_actions import WebDriverActions
from utils.gmail_helper import get_code, send_email

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class Login:
    SUBMIT_BUTTON_ID = "signInSubmit"
    OTP_INPUT_ID = "input-box-otp"
    OTP_INPUT_NAME_FORMAT = "otc-%d"
    OTP_SUBMIT_BUTTON_XPATH = (
        '//input[@aria-labelledby="cvf-submit-otp-button-announce"]'
    )
    EMAIL_NAME = "email"
    PASSWORD_NAME = "password"
    SELLER_CENTRAL_ACCOUNT_SCREEN = "https://sellercentral.amazon.com/authorization/select-account?returnTo=%2Fgp%2Fssof%2Fshipping-queue.html%2Fref%253Dxx_fbashipq_dnav_xx&mons_redirect=remedy_url"
    SELLER_CENTRAL_ACCOUNT_SCREEN_COUNTRY_XPATH = (
        "//div[contains(text(),'United States')]"
    )
    SELLER_CENTRAL_ACCOUNT_SCREEN_COUNTRY_SUBMIT_XPATH = (
        "//button[normalize-space()='Select Account']"
    )

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
        self.logged_in_status = None

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
        if self.driver_actions.is_element_present(By.NAME, self.EMAIL_NAME):
            self.driver_actions.enter_text(By.NAME, self.EMAIL_NAME, self.username)

        self.driver_actions.enter_text(By.NAME, self.PASSWORD_NAME, self.password)
        self.driver_actions.click_element(By.ID, self.SUBMIT_BUTTON_ID)

        if not self.is_logged_in():
            self.handle_otp()
        else:
            print("Logged in successfully.")

    def handle_otp(self):
        """Handle OTP if required."""
        if self.type == "vendor_central":
            self.handle_vendor_central_otp()
        elif self.type == "seller_central":
            self.handle_seller_central_otp()

        if not self.is_logged_in():
            print("Login failed.")
            self.send_login_failure_email()

    def handle_vendor_central_otp(self):
        code = get_code()
        if self.driver_actions.is_element_present(By.ID, self.OTP_INPUT_ID):
            self.driver_actions.enter_text(By.ID, self.OTP_INPUT_ID, code)
        else:
            for i in range(6):
                self.driver_actions.enter_text(
                    By.NAME, self.OTP_INPUT_NAME_FORMAT % (i + 1), code[i]
                )

        self.driver_actions.click_element(By.XPATH, self.OTP_SUBMIT_BUTTON_XPATH)

    def handle_seller_central_otp(self):
        #! TODO - still need to review the criterion values
        code = input("Please enter your code: ")
        self.driver_actions.enter_text(By.NAME, "otpCode", code)
        self.driver_actions.click_element(By.NAME, "rememberDevice")
        self.driver_actions.click_element(By.XPATH, "//input[@id='auth-signin-button']")
        if self.driver_actions.current_url == self.SELLER_CENTRAL_ACCOUNT_SCREEN:
            self.select_account()

    def select_account(self):
        self.driver_actions.click_element(
            By.XPATH, self.SELLER_CENTRAL_ACCOUNT_SCREEN_COUNTRY_XPATH
        )
        self.driver_actions.click_element(
            By.XPATH, self.SELLER_CENTRAL_ACCOUNT_SCREEN_COUNTRY_SUBMIT_XPATH
        )

    def send_login_failure_email(self):
        send_email(
            "Login Failed",
            f"{self.type} Login Failed. Most likely need to sign in with otp again please try again",
            self.sender_email,
            self.recipient_emails,
        )
