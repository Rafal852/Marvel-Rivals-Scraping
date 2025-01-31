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
            time.sleep(2)

            # Handle possible consent popup
            try:
                # Switch to the iframe if it exists
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'Consent')]"))
                )
                consent_iframe = driver.find_element(By.XPATH, "//iframe[contains(@title, 'Consent')]")
                driver.switch_to.frame(consent_iframe)
                
                # Click the "Accept" or "Reject" button (adjust selector based on site)
                try:
                    accept_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
                    )
                    accept_button.click()
                except:
                    reject_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Reject')]"))
                    )
                    reject_button.click()
                
                driver.switch_to.default_content()  # Switch back to the main page
                time.sleep(1)
                
            except Exception as e:
                print(f"No consent popup found or failed to close it: {e}")

            # Remove iframe (if still causing issues)
            driver.execute_script("""
                var iframe = document.querySelector("iframe[src*='privacy-mgmt']");
                if (iframe) iframe.remove();
            """)
            time.sleep(1)

            # Handle the "Heroes" page with the season filter
            if "heroes" in url:
                try:
                    season_dropdown = Select(driver.find_element(By.ID, "season_filter"))
                    season_dropdown.select_by_value(season)
                except Exception as e:
                    print(f"Error selecting season filter: {e}")

            # Select the rank filter
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "rank-selector"))
                ).click()

                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//span[text()='{rank}']"))
                ).click()

            except Exception as e:
                print(f"Error selecting rank filter: {e}")

            time.sleep(2)
            return driver.page_source

        except Exception as e:
            print(f"Error fetching HTML: {e}")
        finally:
            driver.quit()