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
            wait = WebDriverWait(self.driver, 15)
            prices = wait.until(ec.presence_of_all_elements_located((By.XPATH, "//span[@data-a-size='xl']/span/span[@class='a-price-whole']")))
            for price in prices:
                price = wait.until(ec.visibility_of(price))
                price = price.text
                try:
                    price_value = int(price.replace(",", ""))
                    if self.min_price_value <= price_value <= self.max_price_value:
                        self.logger.info(f"Price is in range")
                except ValueError:
                    continue
            self.logger.info(f"All Product prices are in range")
        except Exception as e:
            print(f"Exception occurred before verifying price range: {e}")

    def go_to_page(self, page):
        try:
            time.sleep(3)
            wait = WebDriverWait(self.driver, 10)
            element = self.driver.find_element(By.XPATH, "//a[@aria-label='Go to page {}']".format(page))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(2)
            self.driver.execute_script(f"window.scrollBy(0, -200);")
            wait.until(ec.element_to_be_clickable((By.XPATH, "//a[@aria-label='Go to page {}']".format(page))))
            element.click()
            time.sleep(3)
            self.logger.info(f"Switched to page number - {page}")
        except Exception as e:
            print(f"Exception occurred while selecting switching to page: {e}")

    # def add_product_to_list(self):
    #     wait = WebDriverWait(self.driver, 15)
    #     products = wait.until(ec.presence_of_all_elements_located((By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")))
    #     ratings = wait.until(ec.presence_of_all_elements_located((By.XPATH, "//span//a//i//span[@class='a-icon-alt' and contains(text(), 'out of')]")))
    #     prices = wait.until(ec.presence_of_all_elements_located((By.XPATH, "//span[@data-a-size='xl']/span/span[@class='a-price-whole']")))
    #     product_data = []
    #     # zip_products = itertools.zip_longest(products, ratings, prices, fillvalue=None)
    #     for product, rating, price in zip(products, ratings, prices):
    #         try:
    #             product = wait.until(ec.visibility_of(product))
    #             product = product.text
    #             product_name = str(product[0:50])
    #             self.logger.info(f"Product name is: {product_name}")
    #
    #             price = wait.until(ec.visibility_of(price))
    #             price = price.text
    #             product_price = int(price.replace(",", ""))
    #             self.logger.info(f"Product price is: {price}")
    #
    #             # product_rating = rating.get_attribute("innerHTML")
    #             # self.logger.info(f"Product rating using innerHTML: {product_rating}")
    #             product_rating = rating.get_attribute("textContent")
    #             # self.logger.info(f"Product rating using textContent : {product_rating}")
    #             match = re.search(r'\d+\.\d+', product_rating)
    #             if match:
    #                 first_float_number = float(match.group())
    #                 product_rating = first_float_number
    #                 self.logger.info(f"Product rating is: {product_rating}")
    #
    #             product_data.append((product_name, product_rating, product_price))
    #
    #         except ValueError:
    #             print("add products to list is failed")
    #     # self.logger.info(f"Product data list: {product_data}")
    #     return product_data

    def add_product_to_list(self):
        wait = WebDriverWait(self.driver, 15)
        parent_xpath = "//div[@data-component-type='s-search-result']"
        parent_elements = wait.until(ec.presence_of_all_elements_located((By.XPATH, parent_xpath)))

        product_data = []
        self.logger.info(f"Total search results: {len(parent_elements)}")
        for parent_element in parent_elements:
            try:
                # Find child elements within the parent element
                product_xpath = ".//span[@class='a-size-medium a-color-base a-text-normal']"
                product_elements = WebDriverWait(parent_element, 10).until(ec.presence_of_all_elements_located((By.XPATH, product_xpath)))

                rating_xpath = ".//span//a//i//span[@class='a-icon-alt' and contains(text(), 'out of')]"
                rating_elements = WebDriverWait(parent_element, 10).until(ec.presence_of_all_elements_located((By.XPATH, rating_xpath)))

                price_xpath = ".//span[@data-a-size='xl']/span/span[@class='a-price-whole']"
                price_elements = WebDriverWait(parent_element, 10).until(ec.presence_of_all_elements_located((By.XPATH, price_xpath)))
                # Check if the child elements are present within the parent element
                if product_elements and rating_elements and price_elements:

                    for product_element, rating_element, price_element in zip(product_elements, rating_elements, price_elements):
                        product_text = wait.until(ec.visibility_of(product_element))
                        product_text = product_text.text
                        product_name = str(product_text[0:50])
                        self.logger.info(f"Product name is: {product_name}")

                        rating_text = rating_element.get_attribute("textContent")
                        match = re.search(r'\d+\.\d+', rating_text)
                        if match:
                            product_rating = float(match.group())
                            self.logger.info(f"Product rating is: {product_rating}")
                        else:
                            product_rating = None

                        price_text = wait.until(ec.visibility_of(price_element))
                        price_text = price_text.text.replace(",", "").strip()
                        product_price = int(price_text)
                        self.logger.info(f"Product price is: {price_text}")

                        product_data.append((product_name, product_rating, product_price))
                else:
                    self.logger.warning("One or more child elements are missing in the parent element")
            except Exception as e:
                self.logger.error(f"Error processing product: {str(e)}")
        # self.logger.info(f"Product data list: {product_data}")

        return product_data

    def select_rating(self, rating):
        try:
            # rating should be between 2 and 4
            element = self.driver.find_element(By.XPATH, "//section[@aria-label='{} Stars & Up']".format(rating))
            element = WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable(element))
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"Rating {rating} is selected successfully")
        except Exception as e:
            print(f"Exception occurred while selecting rating button: {e}")

    def select_brand(self, brand):
        try:
            # rating should be between 2 and 4
            element = self.driver.find_element(By.XPATH, "//span[text()='{}']".format(brand))
            element = WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable(element))
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"Brand name '{brand}' is selected successfully")
        except Exception as e:
            print(f"Exception occurred while selecting brand name: {e}")

    def create_wish_list(self, list_name):
        try:
            wait = WebDriverWait(self.driver, 15)
            actions = ActionChains(self.driver)
            element = self.driver.find_element(By.XPATH, "//span[@class='nav-line-2 ' and text()='Account & Lists']")
            wait.until(ec.visibility_of(element))
            actions.move_to_element(element).perform()  # hover over 'Account & Lists'
            element = self.driver.find_element(By.XPATH, "//span[@class='nav-text' and text()='Your Wish List']")
            wait.until(ec.visibility_of(element))
            actions.move_to_element(element).click().perform()  # hover over and click on 'Your Wish List'
            element = self.driver.find_element(By.XPATH, "//a[@id='createList']")
            wait.until(ec.visibility_of(element))
            actions.move_to_element(element).click().perform()  # click on Create List
            element = self.driver.find_element(By.XPATH, "//input[@id='list-name']")
            wait.until(ec.visibility_of(element))
            element.clear()  # clear input field
            time.sleep(2)
            self.logger.info(f"Input field of wish list creation panel is cleared")
            element = self.driver.find_element(By.XPATH, "//input[@id='list-name']")
            wait.until(ec.visibility_of(element))
            element.send_keys(list_name)  # Enter wish list name and click button
            time.sleep(2)
            self.logger.info(f"New wish list name is entered")
            child_element = self.driver.find_element(By.XPATH, "//span[@class='a-button-text' and text()='Create List']")
            wait.until(ec.visibility_of(child_element))
            actions.move_to_element(child_element).click().perform()
            # parent_element = driver.find_element(By.XPATH, "//input[@fdprocessedid='c4iso']")
            try:
                self.driver.find_element(By.XPATH, "//span[contains(text(), '{}')]".format(list_name))
                self.logger.info(f"New wish list is created with name '{list_name}' successfully")
            except Exception as e:
                print(f"Exception occurred while finding new wish list: {e}")
        except Exception as e:
            print(f"Exception occurred while creating new wish list: {e}")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    search_product = SearchProductPage(driver)


