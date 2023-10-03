import time
from dotenv import load_dotenv
from src.pageObjects.searchProductPage import SearchProductPage
from tests.amazon.test_amazonLogin import test_amazon_login
from src.utils.customLogger import LogGen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import itertools
load_dotenv()


def test_product_search(setup):
    driver = setup
    wait = WebDriverWait(driver, 10)
    test_amazon_login(driver)
    searchProduct = SearchProductPage(driver)
    logger = LogGen.loggen()
    searchProduct.click_all_button()
    try:
        element = (By.XPATH, "//a[contains(text(), 'Amazon miniTV- FREE entertainment')]")
        wait.until(ec.visibility_of_element_located(element))
        element = driver.find_element(element)
        searchProduct.move_to_element(element)
    except Exception as e:
        print(f"Exception occurred while moving to an element: {e}")
    searchProduct.scroll_down(200)
    time.sleep(2)
    searchProduct.select_electronics()
    time.sleep(2)
    searchProduct.scroll_down(200)
    searchProduct.select_all_electronics()
    time.sleep(4)
    searchProduct.search_product("Dell Laptop")
    time.sleep(5)
    searchProduct.scroll_down(200)
    time.sleep(4)
    searchProduct.select_rating(4)          # rating should be between 2 and 4
    time.sleep(4)
    searchProduct.scroll_down(600)
    searchProduct.set_min_price()
    searchProduct.set_max_price()
    # searchProduct.select_go_button()      # using ENTER key instead of selecting go button
    time.sleep(5)
    searchProduct.scroll_down(200)
    searchProduct.is_price_in_range()
    time.sleep(2)
    product_list_1 = searchProduct.add_product_to_list()
    time.sleep(2)
    searchProduct.go_to_page(2)
    time.sleep(2)
    searchProduct.scroll_down(-200)     # scroll up 200pixels
    time.sleep(2)
    searchProduct.is_price_in_range()
    product_list_2 = searchProduct.add_product_to_list()
    all_product_list = product_list_1 + product_list_2
    products_with_max_rate = [product for product in all_product_list if product[1] == 5.0]
    logger.info(f"Product data list with maximum rating: {products_with_max_rate}")
    product_name_with_min_value = min(products_with_max_rate, key=lambda x: x[2])
    logger.info(f"Product name with minimum value among maximum rating: {product_name_with_min_value}")
    product_name = product_name_with_min_value[0]
    searchProduct.search_product(product_name)
    time.sleep(5)
    # product_name = product_name[0:31]
    # element = wait.until(ec.presence_of_element_located((By.XPATH, "//a//span[contains(text(),{})]".format(product_name))))
    # driver.execute_script("arguments[0].scrollIntoView(true);", element)
    # time.sleep(3)
    # searchProduct.scroll_down(-200)   # scroll-up 200 pixels
    # time.sleep(2)
    # element.click()         # product link should open in new window
    # logger.info(f"Product with maximum rating and minimum value is selected and opened in new window")
    # time.sleep(4)
    # searchProduct.scroll_down(300)          # to find the wish list button
    # element = wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@id='add-to-wishlist-button']")))
    # element.click()
    # time.sleep(2)
    actions = ActionChains(driver)
    element = driver.find_element(By.XPATH, "//span[@class='nav-line-2 ' and text()='Account & Lists']")
    wait.until(ec.visibility_of(element))
    actions.move_to_element(element).perform()      # hover over 'Account & Lists'
    element = driver.find_element(By.XPATH, "//span[@class='nav-text' and text()='Your Wish List']")
    wait.until(ec.visibility_of(element))
    actions.move_to_element(element).click().perform()  # hover over and click on 'Your Wish List'
    element = driver.find_element(By.XPATH, "//a[@id='createList']")
    wait.until(ec.visibility_of(element))
    actions.move_to_element(element).click().perform()      # click on Create List
    element = driver.find_element(By.XPATH, "//input[@id='list-name']")
    wait.until(ec.visibility_of(element))
    element.clear()             # clear input field
    time.sleep(2)
    element = driver.find_element(By.XPATH, "//input[@id='list-name']")
    wait.until(ec.visibility_of(element))
    element.send_keys("Wish List To test")      # Enter wish list name
    time.sleep(2)
    input_field = (By.XPATH, "//span[text()='Create List']")
    wait.until(ec.element_to_be_clickable(input_field))
    for _ in range(3):
        actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.ENTER)       # Click on create button
    logger.info(f"New wish list is created")


if __name__ == '__main__':
    driver = webdriver.Chrome()
    test_product_search(driver)
