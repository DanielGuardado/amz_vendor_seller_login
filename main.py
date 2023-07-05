from amazon_services.amazon_manager import AmazonManager
from config.config import VENDOR_CENTRAL_CONFIG, SELLER_CENTRAL_CONFIG
from selenium.webdriver.common.by import By
from time import sleep

vendor_central = AmazonManager(
    VENDOR_CENTRAL_CONFIG["amazon_login"]["username"],
    VENDOR_CENTRAL_CONFIG["amazon_login"]["password"],
    VENDOR_CENTRAL_CONFIG["amazon_links"]["login_link"],
    VENDOR_CENTRAL_CONFIG["amazon_xpaths"]["logged_in_xpath"],
    VENDOR_CENTRAL_CONFIG["gmail_config"]["sender_email"],
    VENDOR_CENTRAL_CONFIG["gmail_config"]["recipient_emails"],
    VENDOR_CENTRAL_CONFIG["type"],
)

vendor_central.login()
token = vendor_central.driver_actions.get_csrf_token(
    VENDOR_CENTRAL_CONFIG["csrf_config"]["csrf_link"],
    By.NAME,
    VENDOR_CENTRAL_CONFIG["csrf_config"]["token_name"],
)

# print(token)

# print("test")
# sleep(5)
# vendor_central.driver_actions.quit()
# sleep(5)

seller_central = AmazonManager(
    SELLER_CENTRAL_CONFIG["amazon_login"]["username"],
    SELLER_CENTRAL_CONFIG["amazon_login"]["password"],
    SELLER_CENTRAL_CONFIG["amazon_links"]["login_link"],
    SELLER_CENTRAL_CONFIG["amazon_xpaths"]["logged_in_xpath"],
    SELLER_CENTRAL_CONFIG["gmail_config"]["sender_email"],
    SELLER_CENTRAL_CONFIG["gmail_config"]["recipient_emails"],
    SELLER_CENTRAL_CONFIG["type"],
)

seller_central.login()
sleep(5)
