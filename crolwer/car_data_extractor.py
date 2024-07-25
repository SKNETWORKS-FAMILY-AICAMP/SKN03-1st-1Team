import os
import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, JavascriptException, ElementNotInteractableException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

class CarDataExtractor:
    def __init__(self, data_directory="tests/extracted_data"):
        self.data_directory = data_directory
        self.driver = self.initialize_chrome_driver()
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

    def initialize_chrome_driver(self):
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def get_brand_and_model_lists(self):
        brand_model_map = {}
        brand_select = Select(self.driver.find_element(By.ID, 'brandList'))
        brands = [option.get_attribute("value") for option in brand_select.options if option.get_attribute("value")]

        for brand_value in brands:
            if not brand_value.strip():
                continue
            self.driver.execute_script(f"arguments[0].value = '{brand_value}'; arguments[0].dispatchEvent(new Event('change'))", brand_select._el)
            time.sleep(1)
            model_select = Select(self.driver.find_element(By.ID, 'modelList'))
            models = [option.get_attribute("value") for option in model_select.options if option.get_attribute("value")]
            brand_model_map[brand_value] = models

        return brand_model_map

    @staticmethod
    def generate_combinations(filters, periods):
        def expand_filter(filter_list, current=[]):
            if not filter_list:
                return [current]
            if isinstance(filter_list[0], list):
                expanded = []
                for option in filter_list[0]:
                    expanded.extend(expand_filter([option] + filter_list[1:], current))
                return expanded
            else:
                return expand_filter(filter_list[1:], current + [filter_list[0]])

        all_combinations = set()  # 중복 제거를 위한 set 사용
        for category, filter_options in filters.items():
            base_combinations = expand_filter(filter_options)
            for base_combination in base_combinations:
                if category == "모델":
                    if isinstance(base_combination[2], list):
                        for brand, models in base_combination[2]:
                            for model in models:
                                if "기간별" in [sub for sub in base_combination[0]]:
                                    all_combinations.add(tuple([category, base_combination[0][0], "2023.01", brand, model]))
                                else:
                                    for period in periods:
                                        all_combinations.add(tuple([category, base_combination[0][0], period, brand, model]))
                    else:
                        if "기간별" in [sub for sub in base_combination[0]]:
                            for brand, models in filters["모델"][2]:
                                for model in models:
                                    all_combinations.add(tuple([category, base_combination[0][0], "2023.01", brand, model]))
                        else:
                            for period in periods:
                                for brand, models in filters["모델"][2]:
                                    for model in models:
                                        all_combinations.add(tuple([category, base_combination[0][0], period, brand, model]))
                elif category == "브랜드":
                    for nation in filter_options[0]:
                        for period in periods:
                            base_combination_without_nation = base_combination[1:]
                            gender_legal_combinations = [
                                [],
                                [base_combination_without_nation[0]],
                                [base_combination_without_nation[1]],
                                [base_combination_without_nation[2]],
                                [base_combination_without_nation[0], base_combination_without_nation[1]],
                                [base_combination_without_nation[0], base_combination_without_nation[2]],
                                [base_combination_without_nation[1], base_combination_without_nation[2]],
                                base_combination_without_nation
                            ]
                            for comb in gender_legal_combinations:
                                all_combinations.add(tuple([category, nation, period] + comb))
                elif category == "TOP10":
                    for nation in filter_options[0]:
                        for period in periods:
                            all_combinations.add(tuple([category, nation[0], period]))
        return [list(comb) for comb in all_combinations]  # list of lists for processing

    def select_date(self, year, month, from_to='from'):
        try:
            date_element = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, f'{from_to}Date'))
            )
            self.driver.execute_script("arguments[0].click();", date_element)
            time.sleep(2)

            # 현재 선택된 연도를 가져옴
            current_year_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f"//span[@id='{from_to}Year']"))
            )
            current_year = int(current_year_element.text)
            print(f"Current year: {current_year}")

            # 연도가 맞지 않으면 JavaScript로 year_prev 또는 year_next 버튼 클릭
            while current_year != int(year):
                if current_year < int(year):
                    self.driver.execute_script(f"document.querySelector('.cal.{from_to}Cal .year_next').click();")
                else:
                    self.driver.execute_script(f"document.querySelector('.cal.{from_to}Cal .year_prev').click();")
                time.sleep(1)
                current_year_element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, f"//span[@id='{from_to}Year']"))
                )
                current_year = int(current_year_element.text)
                print(f"Updated current year: {current_year}")

            # 월 선택
            month_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@id='{from_to}Month']//a[text()='{int(month)}월']"))
            )
            self.driver.execute_script("arguments[0].click();", month_element)
            time.sleep(2)
            print(f"Selected {from_to} date: {year}-{month}")
        except Exception as e:
            print(f"Failed to select {from_to} date: {e}")

    def select_filter(self, filters):
        try:
            # 필터 선택 화면으로 이동
            menu_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'btn_menu'))
            )
            self.driver.execute_script("arguments[0].click();", menu_button)
            time.sleep(1)
            print("Clicked menu button")

            category, subcategory, period, *rest = filters

            # 카테고리 선택
            category_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[@data-cate='{category}']"))
            )
            self.driver.execute_script("arguments[0].click();", category_element)
            time.sleep(1)
            print(f"Selected category: {category}")

            if category == "모델":
                subcategory_name, brand, model = subcategory, rest[0], rest[1]
                if subcategory_name in ["기간별", "지역별"]:
                    subcategory_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//input[@id='model_cate4']"))
                    )
                    self.driver.execute_script("arguments[0].click();", subcategory_element)
                    time.sleep(1)
                    print(f"Selected subcategory: {subcategory_name}")

                    # 브랜드 선택
                    brand_select = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, 'brandList'))
                    )
                    brand_select = Select(brand_select)
                    brand_select.select_by_visible_text(brand)
                    time.sleep(1)
                    print(f"Selected brand: {brand}")

                    # 차종 선택
                    model_select = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, 'modelList'))
                    )
                    model_select = Select(model_select)
                    model_select.select_by_visible_text(model)
                    time.sleep(1)
                    print(f"Selected model: {model}")

                    if subcategory_name == "기간별":
                        self.select_date(*period.split('.'), 'from')
                        self.select_date(*period.split('.'), 'to')

                else:
                    subcategory_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//input[@id='{subcategory_name}']"))
                    )
                    self.driver.execute_script("arguments[0].click();", subcategory_element)
                    time.sleep(1)
                    print(f"Selected subcategory: {subcategory_name}")

                    brand_select = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, 'brandList'))
                    )
                    brand_select = Select(brand_select)
                    brand_select.select_by_visible_text(brand)
                    time.sleep(1)
                    print(f"Selected brand: {brand}")

                    model_select = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, 'modelList'))
                    )
                    model_select = Select(model_select)
                    model_select.select_by_visible_text(model)
                    time.sleep(1)
                    print(f"Selected model: {model}")

                    self.select_date(*period.split('.'), 'from')
                    self.select_date(*period.split('.'), 'to')

            elif category == "브랜드":
                nation, period, *genders_and_legal = subcategory, rest[0], rest[1:]

                nation_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//input[@id='{nation}']"))
                )
                self.driver.execute_script("arguments[0].click();", nation_element)
                time.sleep(1)
                print(f"Selected nation: {nation}")

                for gender_or_legal in genders_and_legal:
                    if gender_or_legal:
                        gender_or_legal_element = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"//input[@id='{gender_or_legal}']"))
                        )
                        self.driver.execute_script("arguments[0].click();", gender_or_legal_element)
                        time.sleep(1)
                        print(f"Selected: {gender_or_legal}")

                self.select_date(*period.split('.'), 'from')
                self.select_date(*period.split('.'), 'to')

            elif category == "TOP10":
                nation, period = subcategory, rest[0]

                nation_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//input[@id='{nation}']"))
                )
                self.driver.execute_script("arguments[0].click();", nation_element)
                time.sleep(1)
                print(f"Selected nation: {nation}")

                self.select_date(*period.split('.'), 'from')
                self.select_date(*period.split('.'), 'to')

            complete_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'selectChart'))
            )
            self.driver.execute_script("arguments[0].click();", complete_button)
            time.sleep(5)
            print("Clicked complete button")

        except Exception as e:
            print(f"Exception: {e}")
            # 특정 요소 상태 확인 (디버깅 목적)
            try:
                element_state = self.driver.find_element(By.ID, 'CHART_DATA').get_attribute('innerText')
                print(f"chart_data element innerText: {element_state}")
            except Exception as inner_e:
                print(f"Error accessing chart_data element: {inner_e}")

    def extract_data(self, filters):
        try:
            # JavaScript로 CHART_DATA 변수 확인
            chart_data_script = "return typeof CHART_DATA !== 'undefined' && CHART_DATA ? CHART_DATA : null;"
            chart_data = self.driver.execute_script(chart_data_script)

            if not chart_data:
                print(f"No data found for filters: {filters}")
                self.driver.back()  # 이전 페이지로 이동
                time.sleep(1)
                return

            # 데이터 추출
            json_data_str = json.dumps(chart_data)
            json_data = json.loads(json_data_str)
            
            # JSON 데이터 확인
            #print(f"json_data: {json_data}")

            # 유효한 데이터 키 목록
            valid_keys = ["CHART_DATA", "MAP_DATA", "MAP_DATA1", "IMAGE_DATA"]

            # 유효한 데이터 키 찾기
            for key in valid_keys:
                if key in json_data:
                    data = json_data[key]
                    break
            else:
                print("Error: No valid data key found in json_data")
                return

            # 데이터프레임으로 변환
            df = pd.DataFrame(data)
            
            # 디렉토리 생성
            directory = "extracted_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            # CSV 파일로 저장
            file_name = "_".join(filters) + ".csv"
            file_path = os.path.join(directory, file_name)
            df.to_csv(file_path, index=False)
            print(f"Data extracted and saved to {file_path}")
        except Exception as e:
            print(f"Error extracting data: {e}")

    def select_filter_and_extract_data(self, filters):
        self.select_filter(filters)
        try:
            # 경고창이 나타날 때까지 대기
            WebDriverWait(self.driver, 10).until(
                EC.alert_is_present()
            )

            # 경고창이 나타나면 데이터가 없다고 간주
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            print(f"Alert text: {alert_text}")
            alert.accept()
            print(f"No data available for filters: {filters}")
            self.driver.back()  # 이전 페이지로 이동
            time.sleep(1)
            return  # 데이터가 없는 경우 함수 종료

        except TimeoutException:
            # 경고창이 나타나지 않으면 데이터가 있다고 간주하고 진행
            try:
                # 데이터 추출
                self.extract_data(filters)
            except (NoSuchElementException, TimeoutException) as e:
                print(f"No data found for filters: {filters}, Exception: {e}")
                self.driver.back()  # 이전 페이지로 이동
                time.sleep(1)
            except Exception as e:
                print(f"Error extracting data: {e}")
                # 페이지 소스 출력 (디버깅 목적)
                print(self.driver.page_source)
                self.driver.back()  # 이전 페이지로 이동
                time.sleep(1)
