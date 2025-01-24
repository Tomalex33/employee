import pytest
from selenium import webdriver


@pytest.fixture(scope='class', autouse=True)
def driver():
    print("\nstart browser for test..")
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    print("\nquit browser..")
    driver.quit()


# @pytest.fixture(scope='function', autouse=True)
# def print_name():
#     print("\nФИКСТУРА ВЫПОЛНЯЕТСЯ ПЕРЕД ФУНКЦИЕЙ")
#
#
# @pytest.fixture(scope='function')
# def print_name1():
#     print("\nФИКСТУРА ВЫПОЛНЯЕТСЯ ПОСЛЕ ФУНКЦИИ")


# @pytest.fixture(scope='class', autouse=True)
# def print_name2():
#     print("\nФИКСТУРА ВЫПОЛНЯЕТСЯ ПЕРЕД КЛАССОМ")
#
#
# @pytest.fixture(scope='class')
# def print_name3():
#     print("\nФИКСТУРА ВЫПОЛНЯЕТСЯ ПОСЛЕ КЛАССА")
