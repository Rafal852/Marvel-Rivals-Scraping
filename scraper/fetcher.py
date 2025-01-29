from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class HTMLFetcher:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")

    def fetch_html(self, url, season, rank):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

        try:
            driver.get(url)

            # Wait for the page to load
            time.sleep(2)

            # Select the season filter
            season_dropdown = Select(driver.find_element(By.ID, "season_filter"))
            season_dropdown.select_by_value(season)

            # Select the rank filter
            rank_dropdown = driver.find_element(By.CLASS_NAME, "rank-selector")
            rank_dropdown.click()

            # Click on the rank options to select a rank
            rank_option = driver.find_element(By.XPATH, f"//span[text()='{rank}']")
            rank_option.click()

            # Wait for the page to reload the stats
            time.sleep(2)

            # Fetch the HTML content
            return driver.page_source
        finally:
            driver.quit()