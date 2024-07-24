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

questions = driver.find_elements(By.CLASS_NAME, value="accordion-title")

faq_data = {}
for question in questions:
    try:
        # 대기 시간 추가하여 내용이 로드될 시간 확보
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'accordion-label'))
        )
        # 해당 카테고리의 모든 질문-답변 가져오기
        category = driver.find_element(By.CLASS_NAME, 'accordion-label')
        # questions = driver.find_element(By.CLASS_NAME, 'accordion-title')

        # 대기 시간 추가하여 내용이 로드될 시간 확보
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'accordion-panel-inner'))
        )

        answer = driver.find_element(By.CLASS_NAME, 'accordion-panel-inner')

        print(category.text)
        print(question.text)
        print(answer.text)
        # qa_pairs = []
        # for c, q, a in zip(category, questions, answers):
        #     category_text = c.text.strip()
        #     question_text = q.text.strip()
        #     answer_text = a.text.strip()
        #     qa_pairs.append({'question': question_text, 'answer': answer_text})
        #     faq_data[c] = qa_pairs

        # if category == "기타":
        #     break
    except Exception as e:
        print(f"Error processing category {category}: {e}")

driver.quit()

# 결과 출력
import json
print(json.dumps(faq_data, ensure_ascii=False, indent=4))
