import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

delay = 3  # seconds


def initialize_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver


# Step 1 - Navigate to the following URL https://www.saucedemo.com/

def navigate_to_url(driver):
    driver.get("https://www.saucedemo.com/")


# Step 2: - Login using the following details (username: standard_user, password: secret_sauce)

def login(driver, username, password):
    navigate_to_url(driver)

    login_button = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.ID, "login-button"))
    )

    username_input = driver.find_element(By.ID, "user-name")
    password_input = driver.find_element(By.ID, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()


# Step 3: - Select the highest price item (Please do not use the “Sort By” option on the page)

def select_highest_price_item(driver):
    items = WebDriverWait(driver, delay).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )
    highest_price = 0
    highest_price_item = None

    for item in items:
        price = item.find_element(
            By.CLASS_NAME, "inventory_item_price")
        price = float(price.text.replace("$", ""))
        if price > highest_price:
            highest_price = price
            highest_price_item = item

    return highest_price_item


# Step 4: - Add the selected highest price item to the cart

def add_to_cart(item):
    add_to_cart_btn = item.find_element(By.CLASS_NAME, "btn_inventory")
    add_to_cart_btn.click()


def verify_item_added_to_cart(driver):
    cart_badge = WebDriverWait(driver, delay).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "shopping_cart_badge"), "1")
    )
    return cart_badge


def main():
    driver = initialize_driver()
    try:
        login(driver, "standard_user", "secret_sauce")
        highest_price_item = select_highest_price_item(driver)
        if highest_price_item:
            add_to_cart(highest_price_item)
            assert verify_item_added_to_cart(
                driver), "Item was not added to the cart"
    finally:
        driver.quit()


if __name__ == "__main__":
    main()


@pytest.fixture
def driver():
    driver = initialize_driver()
    yield driver
    driver.quit()


def test_navigate(driver):
    navigate_to_url(driver)
    assert "saucedemo.com" in driver.current_url


def test_login(driver):
    login(driver, "standard_user", "secret_sauce")
    assert "inventory.html" in driver.current_url


def test_select_highest_price_item(driver):
    login(driver, "standard_user", "secret_sauce")
    item = select_highest_price_item(driver)
    assert item is not None


def test_add_to_cart(driver):
    login(driver, "standard_user", "secret_sauce")
    item = select_highest_price_item(driver)
    add_to_cart(item)
    assert verify_item_added_to_cart(driver)
