import pytest
import os
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from file.action import DownloadReports, FileResultWindow
from file.delete_report import delete_report
# from file.driver import *
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


sbis_site = 'https://fix-sso.sbis.ru/auth-online/?ret=fix-online.sbis.ru'
login_add = 'пчелкин'
pas_add = 'пчелкин123'
current_dir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(current_dir, 'test-files\\case_2')
report_page = "https://fix-online.sbis.ru/page/fns"

driver = webdriver.Chrome()
driver.implicitly_wait(5)


try:
    driver.maximize_window()
    driver.get(sbis_site)
    sleep(2)
    login = driver.find_element(By.CSS_SELECTOR, '.controls-InputBase__nativeField_caretFilled.controls-InputBase__nativeField_caretFilled_theme_default')
    login.send_keys(login_add, Keys.ENTER)
    pas = driver.find_element(By.CSS_SELECTOR, '.controls-Password__nativeField_caretFilled_theme_default')
    sleep(1)
    pas.send_keys(pas_add, Keys.ENTER)
    sleep(1)
    driver.get(report_page)
    sleep(1)
    # DownloadReports(driver).load_file_api_and_open(file_path, opened_in_new_tab=False)  # загрузка всех файлов в папке
    # file_result = FileResultWindow(driver)
    # file_result.check_all_loading_successful(2)
    # file_result.close()
    pmo_button = driver.find_element(By.CSS_SELECTOR, '[data-qa="toggleOperationsPanel"]')
    pmo_button.click()
    sleep(1)
    check_box_pmo = driver.find_element(By.CSS_SELECTOR, '[data-qa="controls-CheckboxMarker_state-false"]')
    check_box_pmo.click()
    sleep(1)
    remove_button = driver.find_element(By.CSS_SELECTOR, '[data-qa="remove"].controls-Toolbar__item_horizontal-spacing_medium')
    remove_button.click()
    sleep(1)
    confirm_dialog_button_true = driver.find_element(By.CSS_SELECTOR, '[data-qa="controls-ConfirmationDialog__button-true"]')
    confirm_dialog_button_true.click()
    sleep(1)
    delete_report_button = driver.find_element(By.CSS_SELECTOR, '[data-name="FilterViewPanel__additional-editor_deleted"]')
    delete_report_button.click()
    sleep(1)
    check_box_pmo.click()
    sleep(1)
    remove_button.click()
    sleep(1)
    confirm_dialog_button_true_del = driver.find_element(By.CSS_SELECTOR, '[data-qa="controls-ConfirmationDialog__button-true"]')
    confirm_dialog_button_true_del.click()
    sleep(1)
    close_pmo = driver.find_element(By.CSS_SELECTOR, '[data-qa="controls-OperationsPanel__close"]')
    close_pmo.click()
    sleep(1)
    close_delete_report_button = driver.find_element(By.CSS_SELECTOR, '[data-qa="FilterViewPanel__baseEditor-cross"]')
    close_delete_report_button.click()
    sleep(1)
    # delete_report()

finally:

    sleep(2)
    driver.quit()

