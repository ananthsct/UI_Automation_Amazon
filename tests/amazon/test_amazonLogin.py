import pytest
from dotenv import load_dotenv
import os
import time
from src.pageObjects.loginPage import AmazonLoginPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from src.utils.customLogger import LogGen
load_dotenv()


def test_amazon_login(setup):
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    google_url = os.getenv("GOOGLE_URL")
    # script_directory = os.path.dirname(os.path.abspath(__file__))
    # relative_path = "../results/search_result.txt"
    # file_path = os.path.join(script_directory, relative_path)
    driver = setup
    loginPage = AmazonLoginPage(driver)

    logger = LogGen.loggen()
    try:
        driver.get(google_url)
        driver.find_element(By.XPATH, "//textarea[@name='q']").send_keys("amazon", Keys.ENTER)    # searching amazon
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//h3")))
        search_results = driver.find_elements(By.XPATH, "//h3")
        with open(r"C:\Users\keert\PycharmProjects\UI_Automation_Amazon\results\search_result.txt", "w") as file:
            for result in search_results:
                file.write(result.text + '\n')
        driver.find_element(By.XPATH, "//h3[text()='Amazon.in']").click()
        logger.info("Clicked on amazon link from search result")
        try:
            element = "//div[@id='nav-tools']/a[contains(@href, 'signin')]"
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, element)))
            driver.find_element(By.XPATH, element).click()
            logger.info("Amazon sign-in link is clicked")
        except Exception as e:
            print("Element not found ", str(e))
            logger.error("Amazon sign-in link is not clicked")
        time.sleep(3)
        loginPage.login_to_amazon(user, password)
        loginPage.verify_login()
        logger.info("Login to Amazon successful")
    except Exception as e:
        print("Login not successful ", str(e))


if __name__ == "__main__":
    driver = webdriver.Chrome()
    test_amazon_login(driver)
