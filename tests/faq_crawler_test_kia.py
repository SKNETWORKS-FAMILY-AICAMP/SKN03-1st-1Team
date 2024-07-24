# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# import csv
# import json

# # Chrome 옵션 설정
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)  # 브라우저 꺼짐 방지

# driver = webdriver.Chrome(options=chrome_options)
# url = "https://www.kia.com/kr/customer-service/center/faq"
# driver.get(url)
# driver.implicitly_wait(5)

# # 브라우저 창 최대화
# driver.maximize_window()
# driver.execute_script("window.scrollBy(0, 500);")
# driver.implicitly_wait(20)

# for idx in range(7):
#     if idx == 1:
#         continue
#     else:
#         total_elements = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[2]/div/div/div[3]/div/div/div[2]/div/div/div/div/ul/li[{idx+1}]/button")
#         total_elements.click()
#         driver.implicitly_wait(5)

#     question_elements = driver.find_elements(By.CLASS_NAME, "cmp-accordion__item")

#     for element in question_elements:
#         # 버튼 요소를 찾음
#         button_element = element.find_element(By.CLASS_NAME, "cmp-accordion__button cmp-accordion__button--hidden")
#         driver.implicitly_wait(5)
#         data_link_label = button_element.get_attribute("data-link-label")

#         # '_' 앞의 단어 추출
#         category = data_link_label.split('_')[0]
#         print(f"Category: {category}, Question: {element.text}")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
import csv
import json
import time

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 브라우저 꺼짐 방지

driver = webdriver.Chrome(options=chrome_options)
url = "https://www.kia.com/kr/customer-service/center/faq"
driver.get(url)
driver.implicitly_wait(5)

# 브라우저 창 최대화
driver.maximize_window()
driver.execute_script("window.scrollBy(0, 500);")
driver.implicitly_wait(20)

faq_data = []

for idx in range(7):
    if idx == 1:
        continue
    else:
        total_elements = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[2]/div/div/div[3]/div/div/div[2]/div/div/div/div/ul/li[{idx+1}]/button")
        total_elements.click()
        time.sleep(2)  # 로딩 대기

    question_elements = driver.find_elements(By.CLASS_NAME, "cmp-accordion__item")

    for element in question_elements:
        button_element = element.find_element(By.CSS_SELECTOR, ".cmp-accordion__button")
        driver.implicitly_wait(5)
        data_link_label = button_element.get_attribute("data-link-label")

        # '_' 앞의 단어 추출
        category = data_link_label.split('_')[0]
        
        try:
            button_element.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].scrollIntoView(true);", button_element)
            time.sleep(2)
            button_element.click()

        question = button_element.text
        # answer_element = element.find_element(By.CSS_SELECTOR, f"#{button_element.get_attribute('aria-controls')}")
        # answer = answer_element.text
        faq_data.append({"category": category, "question": question})
        print(f"Category: {category}, Question: {question}")
        # faq_data.append({"category": category, "question": question, "answer": answer})
        # print(f"Category: {category}, Question: {question}, Answer: {answer}")

# 브라우저 종료
# driver.quit()

# 결과 출력
print(json.dumps(faq_data, ensure_ascii=False, indent=4))

# # CSV 파일로 저장
# csv_file = "faq_data.csv"
# csv_columns = ["category", "question", "answer"]

# try:
#     with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#         writer.writeheader()
#         for data in faq_data:
#             writer.writerow(data)
#     print(f"Data successfully saved to {csv_file}")
# except IOError as e:
#     print(f"Error saving to file: {e}")
