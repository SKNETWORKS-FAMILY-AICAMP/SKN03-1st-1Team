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
            time.sleep(0.75)
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

        all_combinations = []
        for category, filter_options in filters.items():
            base_combinations = expand_filter(filter_options)
            for base_combination in base_combinations:
                if category == "모델":
                    if isinstance(base_combination[2], list):
                        for brand, models in base_combination[2]:
                            for model in models:
                                if "기간별" in [sub for sub in base_combination[0]]:
                                    all_combinations.append([category, base_combination[0][0], "2023.01", brand, model])
                                else:
                                    for period in periods:
                                        all_combinations.append([category, base_combination[0][0], period, brand, model])
                    else:
                        if "기간별" in [sub for sub in base_combination[0]]:
                            for brand, models in filters["모델"][2]:
                                for model in models:
                                    all_combinations.append([category, base_combination[0][0], "2023.01", brand, model])
                        else:
                            for period in periods:
                                for brand, models in filters["모델"][2]:
                                    for model in models:
                                        all_combinations.append([category, base_combination[0][0], period, brand, model])
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
                                all_combinations.append([category, nation, period] + comb)
                elif category == "TOP10":
                    for nation in filter_options[0]:
                        for period in periods:
                            all_combinations.append([category, nation[0], period])
        return all_combinations

    def select_date(self, year, month, from_to='from'):
        date_element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, f'{from_to}Date')))
        self.driver.execute_script("arguments[0].click();", date_element)
        time.sleep(2)
        year_element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, f"//span[@id='{from_to}Year' and text()='{year}']")))
        self.driver.execute_script("arguments[0].click();", year_element)
        time.sleep(2)
        month_element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, f"//div[@id='{from_to}Month']//a[text()='{int(month)}월']")))
        self.driver.execute_script("arguments[0].click();", month_element)
        time.sleep(2)

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
                if subcategory_name == "기간별":
                    print(f"Skipping subcategory selection as it is already selected: {subcategory_name}")

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

                else:
                    subcategory_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//input[@id='model_cate2']"))
                    )
                    subcategory_element.click()
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
                nation_element.click()
                time.sleep(1)
                print(f"Selected nation: {nation}")

                for gender_or_legal in genders_and_legal:
                    if gender_or_legal:
                        gender_or_legal_element = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"//input[@id='{gender_or_legal}']"))
                        )
                        gender_or_legal_element.click()
                        time.sleep(1)
                        print(f"Selected: {gender_or_legal}")

                self.select_date(*period.split('.'), 'from')
                self.select_date(*period.split('.'), 'to')

            elif category == "TOP10":
                nation, period = subcategory, rest[0]

                nation_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//input[@id='{nation}']"))
                )
                nation_element.click()
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
            json_data_str = self.driver.execute_script("return JSON.stringify(CHART_DATA)")
            json_data = json.loads(json_data_str)
            valid_keys = ["CHART_DATA", "MAP_DATA", "MAP_DATA1", "IMAGE_DATA"]
            data = next((json_data[key] for key in valid_keys if key in json_data), None)
            if data is None:
                print("Error: No valid data key found in json_data")
                return
            df = pd.DataFrame(data)
            directory = "extracted_data"
            os.makedirs(directory, exist_ok=True)
            file_name = "_".join(filters) + ".csv"
            file_path = os.path.join(directory, file_name)
            df.to_csv(file_path, index=False)
        except Exception as e:
            print(f"Error extracting data: {e}")

    def select_filter_and_extract_data(self, filters):
        self.select_filter(filters)
        self.extract_data(filters)