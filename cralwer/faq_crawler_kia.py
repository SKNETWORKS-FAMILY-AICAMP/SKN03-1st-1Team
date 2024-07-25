from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import os
import csv
import time

def initialize_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    return driver

def navigate_to_url(driver, url):
    driver.get(url)
    driver.execute_script("window.scrollBy(0, 500);")

def collect_faq_data(driver, faq_data, category_text):
    question_elements = driver.find_elements(By.CLASS_NAME, "cmp-accordion__item")
    question_num = 0

    for element in question_elements:
        question = element.find_element(By.ID, f"accordion-item{question_num}-button")
        question_num += 1

        try:
            question.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            driver.implicitly_wait(10)
            question.click()

        answer = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[2]/div/div/div[3]/div/div/div[3]/div/div/div[{question_num}]/div/div/div")
        faq_data.append({"category": category_text, "question": question.text, "answer": answer.text, "is_most": None, "brand_id": 1})

def save_faq_data(faq_data, file_path):
    keys = faq_data[0].keys()
    with open(file_path, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(faq_data)

def main():
    url = "https://www.kia.com/kr/customer-service/center/faq"
    file_path = os.path.join(os.path.dirname(__file__), 'faq_data.csv')
    faq_data = []
    
    driver = initialize_driver()
    navigate_to_url(driver, url)
    
    for category_num in range(1, 8):
        if category_num == 2:
            continue
        else:
            category = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[2]/div/div/div[3]/div/div/div[2]/div/div/div/div/ul/li[{category_num}]/button")
            category_text = category.text
            category.click()
            time.sleep(5)
        
        while True:
            collect_faq_data(driver, faq_data, category_text)
            
            next_page = driver.find_elements(By.XPATH, "//ul[@class='paging-list']//li[@class='is-active']/following-sibling::li/a")
            if next_page:
                next_page[0].click()
                time.sleep(5)
            else:
                print(f"Category '{category_text}' collection complete.")
                break
    
    driver.quit()
    save_faq_data(faq_data, file_path)
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    main()
