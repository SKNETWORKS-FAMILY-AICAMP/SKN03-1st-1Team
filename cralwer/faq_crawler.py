from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import time
import csv
import os

class BaseCrawler:
    def __init__(self, url) -> None:
        self.url = url
        self.faq_data = []
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.implicitly_wait(5)

    def set_scroll(self) -> None:
        pass
    
    def collect_qa_data(self) -> None:
        pass

    def save_faq_data(self, data_lst) -> None:
        self.data_lst = data_lst
        # 현재 실행 파일의 디렉토리 경로 가져오기
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # CSV 파일로 저장
        csv_file = os.path.join(current_directory, "../data/faq_data_bf_preprocessing.csv")
        csv_columns = ["category", "question", "answer", "is_most", "brand_id"]

        # 새로 저장할  csv 파일 경로
        file_exists = os.path.isfile(csv_file)

        try:
            with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                # 새로 저장할 csv 파일 경로 존재하지 않으면, 생성
                if not file_exists:
                    writer.writeheader()
                for data in self.data_lst:
                    writer.writerow(data)
            print(f"Data successfully saved to {csv_file}")
        except IOError as e:
            print(f"Error saving to file: {e}")

class KiaCrawler(BaseCrawler):
    def collect_qa_data(self) -> str:
        self.driver.execute_script("window.scrollBy(0, 500);")
        question_elements = self.driver.find_elements(By.CLASS_NAME, "cmp-accordion__item")
        question_num = 0

        for element in question_elements:
            question = element.find_element(By.ID, f"accordion-item{question_num}-button")
            question_num += 1

            try:
                question.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                self.driver.implicitly_wait(10)
                question.click()

            answer = self.driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[2]/div/div/div[3]/div/div/div[3]/div/div/div[{question_num}]/div/div/div")
        return question.text, answer.text

    def collect_category_data(self) -> list:
        for category_num in range(1, 8):
            # '전체' 카테고리는 건너뜀
            if category_num == 2:
                continue
            else:
                category = self.driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[2]/div/div/div[3]/div/div/div[2]/div/div/div/div/ul/li[{category_num}]/button")
                category.click()
                time.sleep(5)

            # 페이지 순환
            while True:
                question_txt, answer_txt = self.collect_qa_data()

                # 다음 페이지가 있는지 확인
                next_page = self.driver.find_elements(By.XPATH, "//ul[@class='paging-list']//li[@class='is-active']/following-sibling::li/a")
                if next_page:
                    next_page[0].click()
                    time.sleep(5)  # 페이지 로딩 대기
                else:
                    category_txt = category.text
                    print(f"현재 {category_txt} 카테고리 수집 완료")
                self.faq_data.append({"category": category_txt, "question": question_txt, "answer": answer_txt, "is_most": None, "brand_id": 1})
                break
        # 브라우저 종료
        self.driver.quit()
        return self.faq_data

class GenesisCralwer(BaseCrawler):
    def collect_qa_data(self) -> list:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        qa_elements = self.driver.find_elements(By.CLASS_NAME, "cp-faq__accordion-item")
        total_num = len(qa_elements)

        for idx, element in enumerate(qa_elements):
            answer_button = element.find_element(By.CLASS_NAME, "accordion-btn")

            try:
                answer_button.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                self.driver.implicitly_wait(30)
                answer_button.click()
            
            question_txt = element.find_element(By.CLASS_NAME, "accordion-title").text
            answer_txt = element.find_element(By.CLASS_NAME, "accordion-panel-inner").text
            category_txt = element.find_element(By.CLASS_NAME, "accordion-label").text
            
            self.faq_data.append({"category": category_txt, "question": question_txt, "answer": answer_txt, "is_most": None, "brand_id": 2})
            print(f"현재 데이터 {idx+1}/{total_num} 수집 완료")

        # 브라우저 종료
        self.driver.quit()

        return self.faq_data

if __name__ == "__main__":
    kia_url = "https://www.kia.com/kr/customer-service/center/faq"
    genesis_url = "https://www.genesis.com/kr/ko/support/faq.html?anchorID=faq_tab"

    # kia_crawler = KiaCrawler(url=kia_url)
    # kia_data = kia_crawler.collect_category_data()
    # kia_crawler.save_faq_data(kia_data)

    genesis_crawler = GenesisCralwer(url=genesis_url)
    genesis_data = genesis_crawler.collect_qa_data()
    genesis_crawler.save_faq_data(genesis_data)