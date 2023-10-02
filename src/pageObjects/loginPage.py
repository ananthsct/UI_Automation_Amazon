from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from src.utils.customLogger import LogGen


class AmazonLoginPage:
    def __init__(self, driver):
        self.driver = driver

    logger = LogGen.loggen()

    # Page Locators
    username = (By.XPATH, "//input[@id='ap_email']")
    continue_button = (By.XPATH, "//input[@id='continue']")
    password = (By.XPATH, "//input[@id='ap_password']")
    signin_button = (By.XPATH, "//input[@id='signInSubmit']")
    error_message = (By.XPATH, "//span[contains(text(),'Your password is incorrect')]")
    verify_signin = (By.XPATH, "//div[@id='nav-tools']/a[contains(@href, 'amazon')]/div/span[text()='Hello, ANANTH']")

    # Page Actions
    def get_username(self):
        return self.driver.find_element(*AmazonLoginPage.username)

    def get_continue_button(self):
        return self.driver.find_element(*AmazonLoginPage.continue_button)

    def get_password(self):
        return self.driver.find_element(*AmazonLoginPage.password)

    def get_signin_button(self):
        return self.driver.find_element(*AmazonLoginPage.signin_button)

    def get_error_message(self):
        return self.driver.find_element(*AmazonLoginPage.error_message)

    def login_to_amazon(self, user, pwd):
        self.get_username().send_keys(user)
        self.get_continue_button().click()
        self.get_password().send_keys(pwd)
        self.get_signin_button().click()

    def verify_login(self):
        try:
            element = self.verify_signin
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(element))
        except Exception as e:
            print("Element is not present:", str(e))
