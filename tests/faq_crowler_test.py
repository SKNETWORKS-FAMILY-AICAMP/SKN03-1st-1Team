from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import json
import csv

driver = webdriver.Chrome()
# url = "https://www.genesis.com/kr/ko/support/faq.html?anchorID=faq_tab"
url = "https://www.kia.com/kr/customer-service/center/faq"
driver.get(url)
driver.implicitly_wait(5)

# 브라우저 창 최대화
driver.maximize_window()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

faq_data = []
question_elements = driver.find_elements(By.CLASS_NAME, "cp-faq__accordion-item")
total_num = len(question_elements)

for num, element in enumerate(question_elements):
    answer_button = element.find_element(By.CLASS_NAME, "accordion-btn")

    try:
        answer_button.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.implicitly_wait(20)
        answer_button.click()
    
    category = element.find_element(By.CLASS_NAME, "accordion-label")
    question = element.find_element(By.CLASS_NAME, "accordion-title")
    answer = element.find_element(By.CLASS_NAME, "accordion-panel-inner")
    
    faq_data.append({"category": category.text, "question": question.text, "answer": answer.text})
    print(f"현재 {total_num} 중 {num+1}번째 데이터 수집 완료")

driver.quit()

# CSV 파일로 저장
csv_file = "faq_data.csv"
csv_columns = ["category", "question", "answer"]

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in faq_data:
            writer.writerow(data)
    print(f"Data successfully saved to {csv_file}")
except IOError as e:
    print(f"Error saving to file: {e}")

# 결과 출력
print(json.dumps(faq_data, ensure_ascii=False, indent=4))