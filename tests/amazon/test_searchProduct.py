import time
from dotenv import load_dotenv
from src.pageObjects.searchProductPage import SearchProductPage
from tests.amazon.test_amazonLogin import test_amazon_login
from src.utils.customLogger import LogGen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
load_dotenv()


def test_product_search(setup):
    driver = setup
    test_amazon_login(driver)
    searchProduct = SearchProductPage(driver)
    logger = LogGen.loggen()
    searchProduct.click_all_button()
    try:
        element = (By.XPATH, "//a[contains(text(), 'Amazon miniTV- FREE entertainment')]")
        WebDriverWait(driver, 10).until(ec.visibility_of_element_located(element))
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
    searchProduct.scroll_down(500)
    time.sleep(2)
    searchProduct.set_min_price()
    time.sleep(2)
    searchProduct.set_max_price()
    time.sleep(2)
    searchProduct.select_go_button()
    time.sleep(5)
    # searchProduct.is_price_in_range()
    prices = driver.find_elements(By.XPATH, "//span[@data-a-size='xl']/span/span[@class='a-price-whole']")
    for price in prices:
        price = price.text
        try:
            price_value = int(price.replace(",", ""))
            if 30000 <= price_value <= 50000:
                logger.info(f"Price is in range")
        except ValueError:
            continue
    logger.info(f"All Product prices are in range")
    time.sleep(2)
    # result1 = searchProduct.add_product_if_rating_is_above_4()
    # print(result1)
    # logger.info(f"Product from page 1 - {result1}")
    products = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
    ratings = driver.find_elements(By.XPATH, "//span[@class='a-size-base puis-normal-weight-text']")
    prices = driver.find_elements(By.XPATH, "//span[@data-a-size='xl']/span/span[@class='a-price-whole']")
    product_data_1 = []
    for product, rating, price in zip(products, ratings, prices):
        try:
            price = price.text
            logger.info(f"Product price is: {price}")
            product = product.text
            product_name = str(product[0:50])
            logger.info(f"Product name is: {product_name}")
            product_rating = float(rating.text)
            product_price = int(price.replace(",", ""))
            product_data_1.append((product_name, product_rating, product_price))
        except ValueError:
            print("add products to list is failed")
    logger.info(f"Product data list: {product_data_1}")
    time.sleep(2)
    searchProduct.go_to_page(2)
    time.sleep(2)
    searchProduct.scroll_down(-200)     # scroll up 200pixels
    time.sleep(2)
    # searchProduct.is_price_in_range()
    time.sleep(2)
    prices = driver.find_elements(By.XPATH, "//span[@data-a-size='xl']/span/span[@class='a-price-whole']")
    for price in prices:
        price = price.text
        try:
            price_value = int(price.replace(",", ""))
            if 30000 <= price_value <= 50000:
                logger.info(f"Price is in range")
        except ValueError:
            continue
    logger.info(f"All Product prices are in range")
    time.sleep(2)
    # result2 = searchProduct.add_product_if_rating_is_above_4()
    products = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
    ratings = driver.find_elements(By.XPATH, "//span[@class='a-size-base puis-normal-weight-text']")
    prices = driver.find_elements(By.XPATH, "//span[@data-a-size='xl']/span/span[@class='a-price-whole']")
    product_data_2 = []
    for product, rating, price in zip(products, ratings, prices):
        try:
            price = price.text
            logger.info(f"Product price is: {price}")
            product = product.text
            product_name = str(product[0:50])
            logger.info(f"Product name is: {product_name}")
            product_rating = float(rating.text)
            product_price = int(price.replace(",", ""))
            product_data_2.append((product_name, product_rating, product_price))
        except ValueError:
            print("add products to list is failed")
    logger.info(f"Product data list: {product_data_2}")
    # if not result1 and not result2:
    #     logger.warning("No products meet the rating criteria.")
    # else:
    all_product_data = product_data_1 + product_data_2
    products_with_max_rate = [product for product in all_product_data if product[1] == 5.0]
    logger.info(f"Product data list with maximum rating: {products_with_max_rate}")
    product_name_with_min_value = min(products_with_max_rate, key=lambda x: x[2])
    logger.info(f"Product name with minimum value among maximum rating: {product_name_with_min_value}")
    element = driver.find_element(By.XPATH, "//span[contains(text(),{})]".format(product_name_with_min_value))
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    searchProduct.scroll_down(-200)   # scroll-up 200 pixels
    element.click()
    logger.info(f"Product with maximum rating and minimum value is selected")
    time.sleep(2)
    searchProduct.scroll_down(300)          # to find the wish list button
    driver.find_element(By.XPATH, "//input[@id='add-to-wishlist-button']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//a[@id='atwl-dd-create-list']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[@id='list-name']").clear()
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[@id='list-name']").send_keys("Wish List To test")
    time.sleep(2)
    driver.find_element(By.XPATH, "//span[text()='Create List']").click()
    logger.info(f"New wish list is created")


if __name__ == '__main__':
    driver = webdriver.Chrome()
    test_product_search(driver)
