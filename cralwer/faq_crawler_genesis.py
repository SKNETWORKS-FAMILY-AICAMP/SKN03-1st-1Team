from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import csv
import os

driver = webdriver.Chrome()
url = "https://www.genesis.com/kr/ko/support/faq.html?anchorID=faq_tab"
driver.get(url)
driver.implicitly_wait(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

faq_data = []
qa_elements = driver.find_elements(By.CLASS_NAME, "cp-faq__accordion-item")
total_num = len(qa_elements)

for idx, element in enumerate(qa_elements):
    answer_button = element.find_element(By.CLASS_NAME, "accordion-btn")

    try:
        answer_button.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.implicitly_wait(30)
        answer_button.click()
    
    category = element.find_element(By.CLASS_NAME, "accordion-label")
    question = element.find_element(By.CLASS_NAME, "accordion-title")
    answer = element.find_element(By.CLASS_NAME, "accordion-panel-inner")

    faq_data.append({"category": category.text, "question": question.text, "answer": answer.text, "is_most": None, "brand_id": 1})
    print(f"현재 데이터 {idx+1}/{total_num} 수집 완료")

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
