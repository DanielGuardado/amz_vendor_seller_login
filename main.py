from vendor_central.vendor_central import VendorCentral
from config.config import (
    AMZ_USERNAME,
    AMZ_PASSWORD,
    LOG_IN_LINK,
    LOGGED_IN_ELEMENT,
    SENDER_EMAIL,
    RECIPIENT_EMAILS,
)
from selenium.webdriver.common.by import By


vendor_central = VendorCentral(
    AMZ_USERNAME,
    AMZ_PASSWORD,
    LOG_IN_LINK,
    LOGGED_IN_ELEMENT,
    SENDER_EMAIL,
    RECIPIENT_EMAILS,
)
vendor_central.login()
csrf_link = "https://vendorcentral.amazon.com/hz/vendor/members/products/mycatalog?ref_=vc_xx_subNav"
token_name = "csrfToken"
token = vendor_central.driver_actions.get_csrf_token(csrf_link, By.NAME, token_name)
print("test")
