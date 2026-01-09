import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Enable headless mode
options.add_argument('--disable-gpu')  # Optional, recommended for Windows

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

try:
	top_10 = []
	driver.get("https://owasp.org/www-project-top-ten/")
	access_to_top_10 = driver.find_element(By.XPATH, "//*[@id = 'sec-main']/p[1]/a").get_attribute("href")
	driver.get(access_to_top_10)
	list_top_10 = driver.find_elements(By.XPATH, "//article[contains (@class, md-content__inner)]/ol/li")
	for item in list_top_10:
		temp_dict = {}
		temp_dict["Title"] = item.text
		temp_dict["Link"] = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
		top_10.append(temp_dict)
	print(top_10)
	top_10_df = pd.DataFrame(top_10)
	top_10_df.to_csv("owasp_top_10.csv", index = False)

	print(top_10)
except Exception as e:
	print("Unable to open the url provided.")
	print(f"Exception: {type(e).__name__} {e}")

driver.quit()
 
