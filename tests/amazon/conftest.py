from selenium import webdriver
import pytest
from dotenv import load_dotenv
import os
import time
from src.pageObjects.loginPage import AmazonLoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from src.utils.customLogger import LogGen
load_dotenv()


@pytest.fixture(scope="class")
def setup():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(chrome_options)
    driver.implicitly_wait(5)
    driver.maximize_window()

    yield driver

