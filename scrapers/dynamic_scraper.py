class DynamicScraper:
    """Optional Selenium demonstration. Selenium Manager resolves supported drivers."""
    def extract_text_xpath(self, url, xpath):
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            options=webdriver.ChromeOptions(); options.add_argument('--headless=new'); options.add_argument('--no-sandbox')
            driver=webdriver.Chrome(options=options)
            try:
                driver.get(url); return [e.text for e in driver.find_elements(By.XPATH,xpath)]
            finally: driver.quit()
        except Exception as exc:
            return []  # callers can present available results if browser/driver is unavailable
