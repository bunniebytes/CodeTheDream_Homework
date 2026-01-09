import pandas as pd
import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Enable headless mode
options.add_argument('--disable-gpu')  # Optional, recommended for Windows

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

def main():
    # Task 3 Part 2
    try:
        data = []
        prev_data = None
        page = 1
        new_data = data
        while True:
            prev_data = new_data
            new_data = get_data(f"https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart&page={page}")
            page += 1
            sleep(2)
            if prev_data == new_data:
                break
            data += new_data
        df = pd.DataFrame(data)
        print(df)
            
        # Task 4 Part 2
        write_to_csv(df, "get_books.csv")
        write_to_json(data, "get_books.json")
        
            
    except Exception as e:
        print("Unable to open the url provided.")
        print(f"Exception: {type(e).__name__} {e}")

    driver.quit()


# Task 3 Part 1
def get_data(link):
    driver.get(link)
    results = []
    search_results = driver.find_elements(By.CSS_SELECTOR, "li.row.cp-search-result-item")
    for result in search_results:
        temp_dict = {}
        title = result.find_element(By.CSS_SELECTOR, "span.title-content").text
        temp_dict["Title"] = title
        
        authors_data = result.find_elements(By.CSS_SELECTOR, "a.author-link")
        author = ";".join([authors.text for authors in authors_data])
        temp_dict["Author"] = author
        
        format_year = result.find_element(By.CSS_SELECTOR, "span.display-info-primary").text
        temp_dict["Format-Year"] = format_year
        results.append(temp_dict)
    return results
   
# Task 4 Part 1
def write_to_csv(dataframe, file_name):
    dataframe.to_csv(file_name, index = False)
    print(f"Successfully wrote dataframe to {file_name}")

def write_to_json(data, file_name):
    try:
        with open(file_name, 'w') as json_file:
            json.dump(data, json_file, indent = 4)
        print(f"Successfully wrote the list to {file_name}")

    except IOError as e:
        print(f"Error writing to file: {e}")
        
def go_to_next_page(driver, df):
    next_page = driver.find_element(By.CSS_SELECTOR, "li.cp-pagination-item:nth-child(9) > a:nth-child(1)").get_attribute("href")

 
# Task 2   
# list, class= "row cp-search-result-item" - result
# span, class= title-content - title
# a, class = "author-link" - author cp-author-link (for multiple authors?)
# span, class = "display-info-primary"

if __name__ == "__main__":
    main()