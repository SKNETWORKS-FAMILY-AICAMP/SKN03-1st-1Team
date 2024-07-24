from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
url = "https://www.genesis.com/kr/ko/support/faq.html?anchorID=faq_tab"
driver.get(url)
driver.implicitly_wait(3)

# 브라우저 창 최대화
driver.maximize_window()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

faq_data = []
question_elements = driver.find_elements(By.CLASS_NAME, "cp-faq__accordion-item")

for element in question_elements:
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    driver.implicitly_wait(10)

    answer_button = element.find_element(By.CLASS_NAME, "accordion-btn")
    answer_button.click()

    # category = element.find_element(By.CLASS_NAME, "accordion-label")
    # question = element.find_element(By.CLASS_NAME, "accordion-title")
    # answer = element.find_element(By.CLASS_NAME, "accordion-panel-inner")
    # print(answer.text)
    
    # faq_data.append({"category": category.text, "question": question.text})

driver.quit()

# 결과 출력
import json
print(json.dumps(faq_data, ensure_ascii=False, indent=4))