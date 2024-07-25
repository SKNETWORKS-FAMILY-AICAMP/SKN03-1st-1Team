from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import csv
import os

def initialize_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    return driver

def navigate_to_url(driver, url):
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def collect_faq_data(driver, faq_data):
    qa_elements = driver.find_elements(By.CLASS_NAME, "cp-faq__accordion-item")
    total_num = len(qa_elements)

    for idx, element in enumerate(qa_elements):
        answer_button = element.find_element(By.CLASS_NAME, "accordion-btn")

        try:
            answer_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            driver.implicitly_wait(10)
            answer_button.click()
        
        category = element.find_element(By.CLASS_NAME, "accordion-label")
        question = element.find_element(By.CLASS_NAME, "accordion-title")
        answer = element.find_element(By.CLASS_NAME, "accordion-panel-inner")

        faq_data.append({"category": category.text, "question": question.text, "answer": answer.text, "is_most": None, "brand_id": 2})
        print(f"Data collection progress: {idx+1}/{total_num}")

def save_faq_data(faq_data, file_path):
    csv_columns = ["category", "question", "answer", "is_most", "brand_id"]
    file_exists = os.path.isfile(file_path)

    try:
        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            if not file_exists:
                writer.writeheader()
            for data in faq_data:
                writer.writerow(data)
        print(f"Data successfully saved to {file_path}")
    except IOError as e:
        print(f"Error saving to file: {e}")

def main():
    url = "https://www.genesis.com/kr/ko/support/faq.html?anchorID=faq_tab"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'faq_data.csv')
    faq_data = []

    driver = initialize_driver()
    navigate_to_url(driver, url)
    collect_faq_data(driver, faq_data)
    driver.quit()
    save_faq_data(faq_data, file_path)

if __name__ == "__main__":
    main()
