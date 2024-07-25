from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.action_chains import ActionChains

import os
import csv
import time

driver = webdriver.Chrome()
url = "https://www.hyundai.com/kr/ko/e/customer/center/faq"
driver.get(url)
driver.implicitly_wait(5)
driver.execute_script("window.scrollBy(0, 1000);")
time.sleep(3)

def collect_faq_data(faq_data: list):
    question_elements = driver.find_elements(By.CLASS_NAME, "list-item   ")

    for element in question_elements:
        question_button = element.find_element(By.CLASS_NAME, "list-title")
        question = element.find_element(By.CLASS_NAME, "list-content")

        try:
            question_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            driver.implicitly_wait(10)
            question_button.click()
        
        driver.implicitly_wait(5)
        answer = driver.find_element(By.CLASS_NAME, "conts")
        faq_data.append({"category": category.text, "question": question.text, "answer": answer.text})
        print({"category": category.text, "question": question.text, "answer": answer.text})

faq_data = []
category_elements = driver.find_elements(By.CLASS_NAME, "tab-menu__icon")

num = 1
for element in category_elements:
    category = element.find_element(By.XPATH, f"/html/body/div/div/div/div[3]/section/div[2]/div/div[2]/section/div/div[1]/div[1]/ul/li[{num}]/button")
    category.click()

    time.sleep(5)

    collect_faq_data(faq_data)
    num += 1

# 브라우저 종료
driver.quit()