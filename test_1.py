import pytest
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys


sbis_site = 'https://fix-sso.sbis.ru/auth-online/?ret=fix-online.sbis.ru'
driver = webdriver.Chrome()
driver.implicitly_wait(5)
report_page = "https://fix-online.sbis.ru/page/fns"

login_add = 'пчелкин'
pas_add = 'пчелкин123'

try:
    # driver.maximize_window()
    driver.get(sbis_site)
    sleep(1)
    login = driver.find_element(By.CSS_SELECTOR, '.controls-InputBase__nativeField_caretFilled.controls-InputBase__nativeField_caretFilled_theme_default')
    login.send_keys(login_add, Keys.ENTER)
    pas = driver.find_element(By.CSS_SELECTOR, '.controls-Password__nativeField_caretFilled_theme_default')
    sleep(1)
    pas.send_keys(pas_add, Keys.ENTER)
    sleep(1)
    driver.get(report_page)
    sleep(1)
    button_load = driver.find_element(By.CSS_SELECTOR, '[data-qa="mainLoadButton"]')
    button_load.click()
    load_file_PC = driver.find_elements(By.CSS_SELECTOR, '[data-qa="item"]')

    # load_file_PC[0].click()
    # sleep(1)
    # load_file_PC[0].send_keys(r"C:\Users\ap.tomchik\PycharmProjects\test_employee\test-files\case_2\*.xml")

    sleep(3)

finally:
    sleep(2)
    driver.quit()

