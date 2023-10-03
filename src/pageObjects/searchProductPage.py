import time
import re
import itertools
from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from src.utils.customLogger import LogGen
import json


class SearchProductPage:
    def __init__(self, driver):
        self.driver = driver

    logger = LogGen.loggen()


    # Page Locators
    all_button = (By.XPATH, "//a[@id='nav-hamburger-menu']")
    electronics = (By.XPATH, "//div[contains(text(),'TV, Appliances, Electronics')]")
    all_electronics = (By.XPATH, "(//a[contains(text(),'All Electronics')])[2]")
    all_electronics2 = (By.XPATH, "(//ul[@class='hmenu hmenu-visible hmenu-translateX']/li)[14]")
    search_box = (By.XPATH, "//input[@id='twotabsearchtextbox']")
    min_price = (By.XPATH, "//input[@id='low-price']")
    max_price = (By.XPATH, "//input[@id='high-price']")
    go_button = (By.XPATH, "//span[@class='a-button-text'][normalize-space()='Go']")
    get_price = (By.XPATH, "//span[@class='a-price-whole']")
    second_page = (By.XPATH, "//a[@aria-label='Go to page 2']")

    # read data from json
    json_file_path = r"C:\Users\keert\PycharmProjects\UI_Automation_Amazon\tests\amazon\test_data.json"
    # Read the JSON data from the file
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # get the prices from json
    first_price_range = data["price_ranges"][0]
    min_price_value = first_price_range["min_price"]
    max_price_value = first_price_range["max_price"]

    # Page Actions
    def click_all_button(self):
        self.driver.find_element(*SearchProductPage.all_button).click()
        self.logger.info("All button is clicked")

    def move_to_element(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.logger.info(f"Moved to {element}")

    def move_to_location(self, x, y):
        self.driver.execute_script(f"window.scrollTo({x}, {y});")
        time.sleep(3)
        self.logger.info(f"Moved to location {x}, {y}")

    def scroll_down(self, pixels):
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")
        self.logger.info(f"Scrolled down to {pixels} pixels")

    def select_electronics(self):
        element = self.electronics
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(element))
        self.driver.find_element(*SearchProductPage.electronics).click()
        self.logger.info(f"Electronics got selected")
        time.sleep(2)

    def select_all_electronics(self):
        try:
            element = self.all_electronics
            wait = WebDriverWait(self.driver, 10)
            wait.until(ec.element_to_be_clickable(element))
            # self.driver.find_element(*SearchProductPage.all_electronics).click()
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(*SearchProductPage.all_electronics))
            self.logger.info(f"All Electronics got selected")
            time.sleep(2)
        except ElementClickInterceptedException as e:
            print(f"Element click intercepted while selecting all electronics link: {e}")

    def search_product(self, item):
        time.sleep(3)
        self.driver.find_element(*SearchProductPage.search_box).send_keys(item, Keys.ENTER)
        self.logger.info(f"{item} searched")

    def set_min_price(self):
        try:
            element = self.min_price
            price = self.min_price_value
            element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(element))
            element.send_keys(price)
            self.logger.info(f"Minimum price entered is: {price}")
        except Exception as e:
            print(f"Exception occurred while setting min_price: {e}")

    def set_max_price(self):
        try:
            element = self.max_price
            price = self.max_price_value
            element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(element))
            element.send_keys(price, Keys.ENTER)
            self.logger.info(f"Maximum price entered is: {price}")
        except Exception as e:
            print(f"Exception occurred while setting max_price: {e}")

    def select_go_button(self):
        try:
            element = self.go_button
            element = WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable(element))
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"Go button is selected")
        except Exception as e:
            print(f"Exception occurred while selecting go button: {e}")

    def is_price_in_range(self):
        try:
            wait = WebDriverWait(driver, 15)
            prices = wait.until(ec.presence_of_all_elements_located(
                (By.XPATH, "//span[@data-a-size='xl']/span/span[@class='a-price-whole']")))
            for price in prices:
                price = wait.until(ec.visibility_of(price))
                price = price.text
                try:
                    price_value = int(price.replace(",", ""))
                    if 30000 <= price_value <= 50000:
                        self.logger.info(f"Price is in range")
                except ValueError:
                    continue
            self.logger.info(f"All Product prices are in range")
        except Exception as e:
            print(f"Exception occurred before verifying price range: {e}")

    def go_to_page(self, page):
        try:
            time.sleep(3)
            element = self.driver.find_element(By.XPATH, "//a[@aria-label='Go to page {}']".format(page))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, "//a[@aria-label='Go to page {}']".format(page))))
            time.sleep(3)
            element.click()
            time.sleep(5)
            self.logger.info(f"Switched to page number - {page}")
        except Exception as e:
            print(f"Exception occurred while selecting switching to page: {e}")

    def add_product_if_rating_is_above_4(self):
        wait = WebDriverWait(self.driver, 15)
        products = wait.until(ec.presence_of_all_elements_located((By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")))
        ratings = wait.until(ec.presence_of_all_elements_located((By.XPATH, "//span[@class='a-icon-alt']")))
        prices = wait.until(ec.presence_of_all_elements_located((By.XPATH, "//span[@data-a-size='xl']/span/span[@class='a-price-whole']")))
        product_data = []
        zip_products = itertools.zip_longest(products, ratings, prices, fillvalue=None)
        for product, rating, price in zip_products:
            if product is not None and rating is not None and price is not None:
                try:
                    price = wait.until(ec.visibility_of(price))
                    price = price.text
                    self.logger.info(f"Product price is: {price}")
                    product = wait.until(ec.visibility_of(product))
                    product = product.text
                    product_name = str(product[0:50])
                    self.logger.info(f"Product name is: {product_name}")
                    rating = wait.until(ec.presence_of_element_located((By.XPATH, "//span[@class='a-icon-alt']")))
                    product_rating = rating.text
                    self.logger.info(f"Product rating is: {product_rating}")
                    match = re.search(r'\d+\.\d+', product_rating)
                    if match:
                        first_float_number = float(match.group())
                        product_rating = first_float_number
                        self.logger.info(f"Product rating is: {product_rating}")
                    product_price = int(price.replace(",", ""))
                    product_data.append((product_name, product_rating, product_price))
                except ValueError:
                    print("add products to list is failed")
        # self.logger.info(f"Product data list: {product_data}")
        return product_data


if __name__ == "__main__":
    driver = webdriver.Chrome()
    search_product = SearchProductPage(driver)


