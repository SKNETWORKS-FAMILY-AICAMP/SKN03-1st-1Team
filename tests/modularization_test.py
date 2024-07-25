import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException


def setup_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    return driver


def navigate_to_url(driver, url):
    driver.get(url)
    driver.execute_script("window.scrollBy(0, 500);")


def click_category(driver, category_num):
    category = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[2]/div/div/div[3]/div/div/div[2]/div/div/div/div/ul/li[{category_num}]/button")
    category.click()
    time.sleep(5)
    return category.text


def collect_faq_data(driver, faq_data):
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
        faq_data.append({"category": category.text, "question": question.text, "answer": answer.text, "is_most": None, "brand_id": 0})


def process_category(driver, category_num, faq_data):
    category_text = click_category(driver, category_num)
    while True:
        collect_faq_data(driver, faq_data)

        # Check for the next page
        next_page = driver.find_elements(By.XPATH, "//ul[@class='paging-list']//li[@class='is-active']/following-sibling::li/a")
        if next_page:
            next_page[0].click()
            time.sleep(5)
        else:
            print(f"현재 {category_text} 카테고리 수집 완료")
            break


def save_to_csv(faq_data, csv_file, csv_columns):
    # Check if file exists to avoid writing headers again
    file_exists = os.path.isfile(csv_file)

    try:
        with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            if not file_exists:
                writer.writeheader()
            for data in faq_data:
                writer.writerow(data)
        print(f"Data successfully saved to {csv_file}")
    except IOError as e:
        print(f"Error saving to file: {e}")


def main():
    url = "https://www.kia.com/kr/customer-service/center/faq"
    csv_file = "faq_data.csv"
    csv_columns = ["category", "question", "answer", "is_most", "brand_id"]

    driver = setup_driver()
    navigate_to_url(driver, url)

    faq_data = []
    for category_num in range(1, 8):
        if category_num == 2:  # Skip the '전체' category
            continue
        process_category(driver, category_num, faq_data)

    driver.quit()

    save_to_csv(faq_data, csv_file, csv_columns)


if __name__ == "__main__":
    main()
