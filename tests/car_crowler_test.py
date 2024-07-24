import os
import csv
import json
import time
import pandas as pd
from bs4 import BeautifulSoup
from itertools import product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, JavascriptException, ElementNotInteractableException, StaleElementReferenceException