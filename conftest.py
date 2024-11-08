import pytest
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

login_add = 'пчелкин'
pas_add = 'пчелкин123'
report_page = "https://fix-online.sbis.ru/page/fns"
sbis_site = 'https://fix-online.sbis.ru/'

# @pytest.fixture(scope="function")
def browser():
    print("\nstart browser for test..")
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(sbis_site)
    sleep(2)
    login = driver.find_element(By.CSS_SELECTOR,
                                '.controls-InputBase__nativeField_caretFilled.controls-InputBase__nativeField_caretFilled_theme_default')
    login.send_keys(login_add, Keys.ENTER)
    pas = driver.find_element(By.CSS_SELECTOR, '.controls-Password__nativeField_caretFilled_theme_default')
    sleep(1)
    pas.send_keys(pas_add, Keys.ENTER)
    sleep(1)
    driver.get(report_page)
