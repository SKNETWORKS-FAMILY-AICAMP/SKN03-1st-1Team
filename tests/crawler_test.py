from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# # 브라우저 꺼짐 방지 옵션
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome()
url = "https://www.genesis.com/kr/ko/support/faq.html?anchorID=faq_tab"
driver.get(url)
driver.implicitly_wait(3)

# # 브라우저 창 최대화
# driver.maximize_window()
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

qa_elements = driver.find_elements(By.CLASS_NAME, "cp-faq__accordion-item")
for element in qa_elements:
    category = element.find_element(By.CLASS_NAME, "accordion-label")
    question = element.find_element(By.CLASS_NAME, "accordion-title")
    # answer = element.find_element(By.CLASS_NAME, "accordion-panel-inner")
    print(category.text)
    print(question.text)
    # print(answer.text)

driver.quit()

# 결과 출력
import json
print(json.dumps(faq_data, ensure_ascii=False, indent=4))
