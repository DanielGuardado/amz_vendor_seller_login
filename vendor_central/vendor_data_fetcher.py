import requests
import datetime
from config.config import (
    HEADERS,
    VENDOR_DATA_LINK,
)
from bs4 import BeautifulSoup


class VendorDataFetcher:
    CSRF_TOKEN = "csrfToken"

    def __init__(self, driver_actions):
        self.driver_actions = driver_actions
        self.csrf_token = None

    def fetch_vendor_data(self, session_cookies):
        """Fetch vendor data from the site."""
        with requests.Session() as session:
            session.cookies.update(session_cookies)

        today = datetime.date.today()

        # First day of this month
        first_day_of_this_month = today.replace(day=1)

        # Subtract 1 day from the first day of this month to get last day of previous month
        # Then replace the day with 1 to get the first day of previous month
        start_date = (first_day_of_this_month - datetime.timedelta(days=1)).replace(
            day=1
        )

        # The end date is today
        end_date = today

        data = {
            "csrfToken": self.csrf_token,
            "searchTerms": "",
            "dateStart-m": start_date.month,
            "dateStart-d": start_date.day,
            "dateStart-y": start_date.year,
            "dateEnd-m": end_date.month,
            "dateEnd-d": end_date.day,
            "dateEnd-y": end_date.year,
            "vendorCodes": "KRAMV",
            "pageSize": "1000",
        }

        response = session.post(VENDOR_DATA_LINK, headers=HEADERS, data=data)

        if response.status_code == 200:
            print("Request successful!")
            return response.text
        else:
            print(f"Request failed with status code {response.status_code}")

    def parse_vendor_data(self, html):
        """Parse the fetched vendor data."""
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select("tr.a-spacing-large.mycat-row-white")
        skus = []
        for row in rows:
            try:
                asin = row.find(
                    "dd", text=lambda x: x and "ASIN" in x.find_previous("dt").text
                ).text.strip()
                upc = row.find(
                    "dd", text=lambda x: x and "UPC" in x.find_previous("dt").text
                ).text.strip()
                sku = row.find("span", class_="mycat-productid-sku").text.strip()

                skus.append({"sku": sku, "asin": asin, "upc": upc})
            except AttributeError:
                pass

        return skus
