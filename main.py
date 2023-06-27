from vendor_central.vendor_central import VendorCentral
from config.config import (
    AMZ_USERNAME,
    AMZ_PASSWORD,
    LOG_IN_LINK,
    LOGGED_IN_ELEMENT,
    SENDER_EMAIL,
    RECIPIENT_EMAILS,
)


vendor_central = VendorCentral(
    AMZ_USERNAME,
    AMZ_PASSWORD,
    LOG_IN_LINK,
    LOGGED_IN_ELEMENT,
    SENDER_EMAIL,
    RECIPIENT_EMAILS,
)
vendor_central.login()
print("test")
