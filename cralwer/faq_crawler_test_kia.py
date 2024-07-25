from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import os
import csv
import time

driver = webdriver.Chrome()
url = "https://www.kia.com/kr/customer-service/center/faq"
driver.get(url)
driver.implicitly_wait(5)
driver.execute_script("window.scrollBy(0, 500);")

def collect_faq_data(faq_data: list):
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

faq_data = []
for category_num in range(1, 8):
    # '전체' 카테고리는 건너뜀
    if category_num == 2:
        continue
    else:
        category = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[2]/div/div/div[3]/div/div/div[2]/div/div/div/div/ul/li[{category_num}]/button")
        category.click()
        time.sleep(5)

    # 페이지 순환
    while True:
        collect_faq_data(faq_data)

        # 다음 페이지가 있는지 확인
        next_page = driver.find_elements(By.XPATH, "//ul[@class='paging-list']//li[@class='is-active']/following-sibling::li/a")
        if next_page:
            next_page[0].click()
            time.sleep(5)  # 페이지 로딩 대기
        else:
            print(f"현재 {category.text} 카테고리 수집 완료")
            break

# 브라우저 종료
driver.quit()

# 현재 실행 파일의 디렉토리 경로 가져오기
current_directory = os.path.dirname(os.path.abspath(__file__))

# CSV 파일로 저장
csv_file = os.path.join(current_directory, "faq_data.csv")
csv_columns = ["category", "question", "answer", "is_most", "brand_id"]

# 새로 저장할  csv 파일 경로
file_exists = os.path.isfile(csv_file)

try:
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        # 새로 저장할 csv 파일 경로 존재하지 않으면, 생성
        if not file_exists:
            writer.writeheader()
        for data in faq_data:
            writer.writerow(data)
    print(f"Data successfully saved to {csv_file}")
except IOError as e:
    print(f"Error saving to file: {e}")