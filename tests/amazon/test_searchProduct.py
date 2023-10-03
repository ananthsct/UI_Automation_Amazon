import time
from dotenv import load_dotenv
from src.pageObjects.searchProductPage import SearchProductPage
from tests.amazon.test_amazonLogin import test_amazon_login
from src.utils.customLogger import LogGen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
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
    searchProduct.scroll_down(900)
    time.sleep(2)
    searchProduct.set_min_price()
    time.sleep(2)
    searchProduct.set_max_price()
    time.sleep(2)
    # searchProduct.select_go_button()
    time.sleep(5)
    searchProduct.scroll_down(200)
    searchProduct.is_price_in_range()
    time.sleep(2)
    product_data_1 = searchProduct.add_product_if_rating_is_above_4()
    # logger.info(f"Product data list: {product_data_1}")
    time.sleep(2)
    searchProduct.go_to_page(2)
    time.sleep(2)
    searchProduct.scroll_down(-200)     # scroll up 200pixels
    time.sleep(2)
    searchProduct.is_price_in_range()
    product_data_2 = searchProduct.add_product_if_rating_is_above_4()
    all_product_data = product_data_1 + product_data_2
    # products_with_max_rate = [product for product in all_product_data if product[1] == 5.0]
    # logger.info(f"Product data list with maximum rating: {products_with_max_rate}")
    product_name_with_min_value = min(all_product_data, key=lambda x: x[2])
    logger.info(f"Product name with minimum value among maximum rating: {product_name_with_min_value}")
    # element = wait.until(ec.element_to_be_clickable((By.XPATH, "//span[contains(text(),{})]".format(product_name_with_min_value))))
    # driver.execute_script("arguments[0].scrollIntoView(true);", element)
    # searchProduct.scroll_down(-200)   # scroll-up 200 pixels
    # element.click()         # product link should open in new window
    # logger.info(f"Product with maximum rating and minimum value is selected and opened in new window")
    # time.sleep(4)
    # searchProduct.scroll_down(300)          # to find the wish list button
    # element = wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@id='add-to-wishlist-button']")))
    # element.click()
    # time.sleep(2)
    # driver.find_element(By.XPATH, "//a[@id='atwl-dd-create-list']").click()
    # time.sleep(2)
    # driver.find_element(By.XPATH, "//input[@id='list-name']").clear()
    # time.sleep(2)
    # driver.find_element(By.XPATH, "//input[@id='list-name']").send_keys("Wish List To test")
    # time.sleep(2)
    # driver.find_element(By.XPATH, "//span[text()='Create List']").click()
    # logger.info(f"New wish list is created")


if __name__ == '__main__':
    driver = webdriver.Chrome()
    test_product_search(driver)
