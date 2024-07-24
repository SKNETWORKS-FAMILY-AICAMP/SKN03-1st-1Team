from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import json

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
total_elements = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[3]/div/div/div[2]/div/div/div/div/ul/li[2]/button")
total_elements.click()
driver.implicitly_wait(5)

question_elements = driver.find_elements(By.CLASS_NAME, "cmp-accordion__item")
for i in question_elements:
    print(i.text)