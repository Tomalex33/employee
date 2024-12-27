import pytest
from selenium import webdriver


@pytest.fixture()
def driver():
    print("\nstart browser for test..")
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    print("\nquit browser..")
    driver.quit()


# @pytest.fixture(scope="class")
# def drivers():
#     print("\nstart browser for test..")
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     yield driver
#     print("\nquit browser..")
#     driver.quit()