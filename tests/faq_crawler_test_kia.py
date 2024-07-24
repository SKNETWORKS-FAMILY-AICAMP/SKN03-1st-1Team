from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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

driver.execute_script("window.scrollBy(0, 500);")
driver.implicitly_wait(5)

for idx in range(1, 8):
    if idx == 2:
        continue
    else:
        category_elements = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[2]/div/div/div[3]/div/div/div[2]/div/div/div/div/ul/li[{idx}]/button")
        category_elements.click()
        category = category_elements.text
        time.sleep(5)

    question_elements = driver.find_elements(By.CLASS_NAME, "cmp-accordion__item")
    for element in question_elements:
        question_element = element.find_element(By.CLASS_NAME, "cmp-accordion__header")
        driver.implicitly_wait(5)
        print(f"현재 {category} 데이터 수집 완료")

        print(f"Category: {category}, Question: {element.text}")

# 브라우저 종료
driver.quit()
