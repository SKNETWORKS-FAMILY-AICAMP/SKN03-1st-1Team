from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import os
import csv
import time

driver = webdriver.Chrome()
url = "https://www.hyundai.com/kr/ko/e/customer/center/faq"
driver.get(url)
driver.implicitly_wait(5)
driver.execute_script("window.scrollBy(0, 1000);")
time.sleep(5)

# 브라우저 종료
driver.quit()