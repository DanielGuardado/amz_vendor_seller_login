import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from datetime import datetime


class ChromeDriver:
    def __init__(self, download_path=None):
        if not download_path:
            current_date_time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
            self.download_path = os.path.join(os.getcwd(), "tmp", current_date_time)
        else:
            self.download_path = download_path

        self.chrome_profile_path = os.path.join(os.getcwd(), "chrome_profile")
        self.driver = self.init_driver(self.chrome_profile_path, self.download_path)

    @staticmethod
    def find_chromedriver(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == "chromedriver.exe" or file == "chromedriver":
                    return os.path.join(root, file)
        return None

    def init_driver(self, chrome_profile_path, download_path):
        options = Options()

        # Create a new Chrome profile if the specified directory does not exist
        if not os.path.exists(chrome_profile_path):
            os.makedirs(chrome_profile_path)
            options.add_argument(
                "--no-first-run"
            )  # Skip the first-run dialog for new profiles

        options.add_argument(f"user-data-dir={chrome_profile_path}")
        options.add_argument(
            "profile-directory=Default"
        )  # Use the same profile directory

        # Create download directory if it doesn't exist
        os.makedirs(download_path, exist_ok=True)

        # Add download directory to Chrome preferences
        prefs = {"download.default_directory": download_path}
        options.add_experimental_option("prefs", prefs)

        # Find and initialize the Chrome driver
        chromedriver_path = self.find_chromedriver(os.getcwd())
        if chromedriver_path:
            driver = webdriver.Chrome(
                service=Service(chromedriver_path), options=options
            )
        else:
            chromedriver_path = ChromeDriverManager(path=os.getcwd()).install()
            driver = webdriver.Chrome(
                service=Service(chromedriver_path), options=options
            )

        return driver
