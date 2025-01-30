from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

class HTMLFetcher:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('blink-settings=imagesEnabled=false')

    def fetch_html(self, url, season, rank):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

        try:
            driver.get(url)

            # Wait for the page to load (you can adjust the sleep time if necessary)
            time.sleep(2)

            # Handle the "Heroes" page with the season filter
            if "heroes" in url:
                try:
                    season_dropdown = Select(driver.find_element(By.ID, "season_filter"))
                    season_dropdown.select_by_value(season)
                except Exception as e:
                    print(f"Error selecting season filter: {e}")

            # Select the rank filter for both pages
            try:
                # Wait for the rank dropdown to be present
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "rank-selector"))
                )

                rank_dropdown = driver.find_element(By.CLASS_NAME, "rank-selector")
                rank_dropdown.click()

                # Wait for the rank option to be clickable
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//span[text()='{rank}']"))
                )

                # Click on the rank option
                rank_option = driver.find_element(By.XPATH, f"//span[text()='{rank}']")
                rank_option.click()

            except Exception as e:
                print(f"Error selecting rank filter: {e}")

            # Wait a few seconds to let the page reload the stats
            time.sleep(2)

            # Fetch the HTML content
            return driver.page_source

        except Exception as e:
            print(f"Error fetching HTML: {e}")
        finally:
            driver.quit()