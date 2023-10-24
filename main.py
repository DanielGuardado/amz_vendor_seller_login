from amazon_services.amazon_manager import AmazonManager
from config.config import VENDOR_CENTRAL_CONFIG, SELLER_CENTRAL_CONFIG
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime, timedelta

# Get today's date
current_date = datetime.today()

# Calculate the date 6 months from today
six_months_before = current_date - timedelta(
    days=1 * 30
)  # Assuming an average month length of 30 days

# Convert to string in the format MM/DD/YYYY
date_string = six_months_before.strftime("%m/%d/%Y")


# vendor_central = AmazonManager(
#     VENDOR_CENTRAL_CONFIG["amazon_login"]["username"],
#     VENDOR_CENTRAL_CONFIG["amazon_login"]["password"],
#     VENDOR_CENTRAL_CONFIG["amazon_links"]["login_link"],
#     VENDOR_CENTRAL_CONFIG["amazon_xpaths"]["logged_in_xpath"],
#     VENDOR_CENTRAL_CONFIG["gmail_config"]["sender_email"],
#     VENDOR_CENTRAL_CONFIG["gmail_config"]["recipient_emails"],
#     VENDOR_CENTRAL_CONFIG["type"],
# )

# vendor_central.login()
# token = vendor_central.driver_actions.get_csrf_token(
#     VENDOR_CENTRAL_CONFIG["csrf_config"]["csrf_link"],
#     By.NAME,
#     VENDOR_CENTRAL_CONFIG["csrf_config"]["token_name"],
# )

# print(token)

# print("test")
# sleep(5)
# vendor_central.driver_actions.quit()
# sleep(5)

seller_central = AmazonManager(
    SELLER_CENTRAL_CONFIG["amazon_login"]["username"],
    SELLER_CENTRAL_CONFIG["amazon_login"]["password"],
    SELLER_CENTRAL_CONFIG["amazon_links"]["login_link"],
    SELLER_CENTRAL_CONFIG["amazon_xpaths"],
    SELLER_CENTRAL_CONFIG["gmail_config"]["sender_email"],
    SELLER_CENTRAL_CONFIG["gmail_config"]["recipient_emails"],
    SELLER_CENTRAL_CONFIG["type"],
)
seller_central.login()

# seller_central.driver_actions.get(
#     "https://sellercentral.amazon.com/reportcentral/REMOVAL_ORDER_DETAIL/1"
# )
# seller_central.driver_actions.interact_with_element_inside_shadow_root(
#     By.CSS_SELECTOR,
#     ".daily-time-picker-kat-dropdown-normal",
#     'kat-option[value="-1"]',
#     action="click",
#     open_first=True,
# )

# seller_central.driver_actions.interact_with_element_inside_shadow_root(
#     By.CSS_SELECTOR,
#     "kat-date-range-picker",
#     "kat-date-picker",
#     action="send_keys",
#     text=date_string,
# )

# seller_central.driver_actions.interact_with_element_inside_shadow_root(
#     By.CSS_SELECTOR,
#     "kat-date-range-picker",
#     "kat-date-picker",
#     action="send_keys",
#     text=date_string,
# )

# seller_central.driver_actions.interact_with_element_inside_shadow_root(
#     By.TAG_NAME,  # Using ID as the selector type since the host element has an ID
#     "kat-button",
#     "button",
#     action="click",
# )

# progress_element_parent = seller_central.driver_actions.get_element(
#     By.XPATH, "//*[text()='In Progress']/.."
# )

# descendant_elements = progress_element_parent.find_elements(By.XPATH, ".//*")

# # descendant_elements[0].click()

# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# class children_changed(object):
#     """An expectation to check if the children of the provided element have changed."""

#     def __init__(self, element, initial_state):
#         self.element = element
#         self.initial_state = initial_state

#     def __call__(self, driver):
#         current_state = [
#             child.text for child in self.element.find_elements(By.XPATH, "./*")
#         ]
#         return current_state != self.initial_state


# # Get the initial state of the child elements
# initial_state = [
#     child.text for child in progress_element_parent.find_elements(By.XPATH, "./*")
# ]

# # Wait for the child elements to change
# WebDriverWait(seller_central.driver_actions.driver, 300).until(
#     children_changed(progress_element_parent, initial_state)
# )
# descendant_elements = progress_element_parent.find_elements(By.XPATH, ".//*")
# # Once the change is detected, click on the desired descendant
# descendant_elements[0].click()


# sleep(5)
