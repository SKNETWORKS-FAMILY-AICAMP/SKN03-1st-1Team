from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
url = "https://www.hyundai.com/kr/ko/e/customer/center/faq"
driver.get(url)
driver.implicitly_wait(3)

# 브라우저 창 최대화
driver.maximize_window()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

elements = driver.find_elements(By.CLASS_NAME, value="tab-menu__icon")

faq_data = {}

for elem in elements:
    try:
        category = elem.text.strip()
        
        # 스크롤 조정하여 도움말 풍선 위치 피하기
        driver.execute_script("arguments[0].scrollIntoView();", elem)

        # 빠르게 클릭 수행
        action = ActionChains(driver)
        action.move_to_element(elem).click().perform()
        print(f"Processing category: {category}")
        
        # 대기 시간 추가하여 내용이 로드될 시간 확보
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'faq-list__question'))
        )

        # 해당 카테고리의 모든 질문 요소 가져오기
        questions = driver.find_elements(By.CLASS_NAME, 'faq-list__question')
        
        qa_pairs = []
        for question in questions:
            try:
                # 질문 클릭하여 답변 표시
                action.move_to_element(question).click().perform()
                time.sleep(1)  # 답변 로드될 시간 대기

                # 질문 텍스트
                question_text = question.text.strip()

                # 답변 텍스트
                answer = question.find_element(By.XPATH, './following-sibling::div')
                answer_text = answer.text.strip()
                
                qa_pairs.append({'question': question_text, 'answer': answer_text})
            except Exception as e:
                print(f"Error processing question in category {category}: {e}")

        faq_data[category] = qa_pairs

        if category == "기타":
            break
    except Exception as e:
        print(f"Error processing category {category}: {e}")

driver.quit()

# 결과 출력
import json
print(json.dumps(faq_data, ensure_ascii=False, indent=4))
