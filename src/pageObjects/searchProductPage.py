import time
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
    go_button = (By.XPATH, "//span[@id='a-autoid-1']")
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
            element = self.all_electronics2
            WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(element))
            self.driver.find_element(*SearchProductPage.all_electronics2).click()
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
            element.send_keys(price)
            self.logger.info(f"Maximum price entered is: {price}")
        except Exception as e:
            print(f"Exception occurred while setting max_price: {e}")

    def select_go_button(self):
        try:
            element = self.go_button
            element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(element))
            element.click()
            self.logger.info(f"Go button is selected")
        except Exception as e:
            print(f"Exception occurred while selecting go button: {e}")

    def is_price_in_range(self):
        try:
            time.sleep(10)
            # element = self.get_price
            prices = self.driver.find_elements(By.XPATH, "//span[@data-a-size='xl']/span/span[@class='a-price-whole']")
            for price in prices:
                price = price.text
                try:
                    price_value = int(price.replace(",", ""))
                    if self.min_price_value <= price_value <= self.max_price_value:
                        pass
                except ValueError:
                    continue
            self.logger.info(f"All Product prices are in range")
            return False
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
        time.sleep(2)
        # element = self.get_price
        products = self.driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
        ratings = self.driver.find_elements(By.XPATH, "//span[@class='a-size-base puis-normal-weight-text']")
        prices = self.driver.find_elements(By.XPATH, "//span[@data-a-size='xl']/span/span[@class='a-price-whole']")
        # self.logger.info(f"{products}")
        # self.logger.info(f"{ratings}")
        # self.logger.info(f"{prices}")

        # zip_products = itertools.zip_longest(products, ratings, prices, fillvalue=None)
        # max_rating = 0
        # min_price = 50000
        product_data = []
        # with open(file_path, 'w') as file:
        for product, rating, price in zip(products, ratings, prices):
            try:
                product_name = product.text
                product_rating = float(rating.text)
                product_price = price.text
                # file.write(f'\nProduct Name: {product_name}\nProduct rating:{product_rating}\nProduct Price:{product_price}')
                product_data.append((product_name, product_rating, product_price))
                # if 4 <= product_rating <= 5:
                #     file.write(f'\nProduct Name: {product_name}\nProduct rating:{product_rating}\nProduct Price:{product_price}')
                #     self.logger.info(f"Product Name: {product_name}, Rating: {product_rating}, Price: {product_price}")
                #     product_data.append((product_name, product_rating, product_price))
                # if product_rating >= max_rating:
                #     max_rating = product_rating
                #     self.logger.info(f"Updated max_rating: {max_rating}")
                # if float(product_price) <= min_price:
                #     min_price = float(product_price)
                #     self.logger.info(f"Updated min_price: {min_price}")
            except ValueError:
                print("add products to file is failed")
            # self.logger.info(f"Maximum rating of product: {max_rating} and Minimum price of Product: {min_price}")
            # self.logger.info(f"{len(products)}-Products above rating 4 are added to {file_path}")

        # result = [(product, rating, price) for product, rating, price in product_data if rating == max_rating and price == min_price]
        return product_data


if __name__ == "__main__":
    driver = webdriver.Chrome()
    search_product = SearchProductPage(driver)


