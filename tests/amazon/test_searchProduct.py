import time
from dotenv import load_dotenv
from src.pageObjects.searchProductPage import SearchProductPage
from tests.amazon.test_amazonLogin import test_amazon_login
from src.utils.customLogger import LogGen
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
load_dotenv()


def test_product_search(setup):
    driver = setup
    wait = WebDriverWait(driver, 10)
    test_amazon_login(driver)
    searchProduct = SearchProductPage(driver)
    logger = LogGen.loggen()
    searchProduct.click_all_button()
    searchProduct.select_electronics()
    searchProduct.select_all_electronics()
    time.sleep(4)
    searchProduct.search_product("Dell Laptop")
    time.sleep(5)
    searchProduct.scroll_down(200)
    time.sleep(4)
    searchProduct.select_rating(4)          # rating should be between 2 and 4
    time.sleep(4)
    searchProduct.select_brand('Dell')
    time.sleep(2)
    searchProduct.scroll_down(600)
    time.sleep(2)
    searchProduct.set_min_price()
    time.sleep(2)
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
    searchProduct.create_wish_list("Wish List To test")             # enter name of wish list to be created
    product_name = product_name_with_min_value[0]
    searchProduct.search_product(product_name)
    time.sleep(5)
    product_name = product_name[0:42]
    logger.info(f"Product name after slicing is: {product_name}")
    searchProduct.add_product_to_wish_list(product_name)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    test_product_search(driver)
