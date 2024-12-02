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
org = 'новая сверка тест'
current_dir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(current_dir, 'test-files\\case_2')
report_page = "https://fix-online.sbis.ru/page/fns"

driver = webdriver.Chrome()
driver.implicitly_wait(5)


try:
    driver.maximize_window()
    driver.get(sbis_site)
    print('ВЫВОДИМ ВСЕ принты')
    print(driver.current_url)
    sleep(2)
    login = driver.find_element(By.CSS_SELECTOR, '.controls-InputBase__nativeField_caretFilled.controls-InputBase__nativeField_caretFilled_theme_default')
    login.send_keys(login_add, Keys.ENTER)
    pas = driver.find_element(By.CSS_SELECTOR, '.controls-Password__nativeField_caretFilled_theme_default')
    sleep(1)
    pas.send_keys(pas_add, Keys.ENTER)
    sleep(5)
    driver.get(report_page)
    sleep(1)
    # filter_org = driver.find_element(By.CSS_SELECTOR, '[data-qa="FilterView__icon"]')  # клик на иконку фильтра организаций"
    # filter_org.click()
    # sleep(1)
    # reset_org_in_filter = driver.find_element(By.CSS_SELECTOR, '[data-qa="FilterViewPanel__baseEditor-cross"]')  # крестик для отмены орг в фильтре
    # reset_org_in_filter.click()
    # sleep(1)
    # apply_filter_org = driver.find_element(By.CSS_SELECTOR, '[data-qa="controls-FilterPanelPopup__applyButton"]')  # иконка применения отмененной организации
    # apply_filter_org.click()
    # sleep(1)
    # ur_org = driver.find_element(By.CSS_SELECTOR, '.controls-FilterView__text')  # клик на поле "все юр. лица"
    # ur_org.click()
    # sleep(1)
    # find_org = driver.find_elements(By.CSS_SELECTOR, '[data-qa="controls-Render__field"] input[type="text"].controls-Field')  # поле для ввода названия организации
    # find_org[0].send_keys(org)
    # sleep(2)
    # choice_org = driver.find_element(By.CSS_SELECTOR, '[data-qa="cell"].controls-padding_right-list_')  # выбираем найденную организацию"
    # choice_org.click()
    # sleep(1)
    report_rsv = driver.find_elements(By.CSS_SELECTOR, '.eoregistry-MainRegister__period')  # выбираем РСВ
    for i in report_rsv:
        if i.text == "I кв'24":
            i.click()
            sleep(8)
    discrepancies = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="structure-counter"] div span')))
    assert discrepancies.text == '6', f'Фактическое значение {discrepancies.text} \n Количество расхождений отличается от эталонного значения = 6'
    sleep(1)
    subsection_1 = driver.find_element(By.CSS_SELECTOR, '[data-qa="structure-item"][title="Подраздел 1"][data-state="created"]')  # Раздел 1 подраздел 1"
    subsection_1.click()
    sleep(2)
    run_all_calc = driver.find_element(By.CSS_SELECTOR, '[data-qa="runFedAllCalc"]')  # Запуск всех расчетов
    run_all_calc.click()
    sleep(1)
    confirm_calc = driver.find_element(By.CSS_SELECTOR, '[data-qa="controls-ConfirmationDialog__button-true"]')  # Подтверждения запуска всех расчетов
    confirm_calc.click()
    sleep(10)
    close_report = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="controls-stack-Button__close"]')))  # Закрываем отчет
    close_report.click()
    sleep(1)
    for i in report_rsv:
        if i.text == "II кв'24":
            i.click()
            sleep(8)
    discrepancies = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="structure-counter"] div span')))
    assert discrepancies.text == '4'
    subsection_1 = driver.find_element(By.CSS_SELECTOR, '[data-qa="structure-item"][title="Подраздел 1"][data-state="created"]')  # Раздел 1 подраздел 1"
    subsection_1.click()
    sleep(1)
    run_all_calc = driver.find_element(By.CSS_SELECTOR, '[data-qa="runFedAllCalc"]')  # Запуск всех расчетов
    run_all_calc.click()
    sleep(1)
    confirm_calc = driver.find_element(By.CSS_SELECTOR,  '[data-qa="controls-ConfirmationDialog__button-true"]')  # Подтверждения запуска всех расчетов
    confirm_calc.click()
    sleep(10)
    discrepancies_not = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[title="Расхождений нет"]')))
    assert discrepancies_not.text == 'Расхождений нет'
    sleep(1)
    close_report = driver.find_element(By.CSS_SELECTOR, '[data-qa="controls-stack-Button__close"]')  # Закрываем отчет
    close_report.click()
    sleep(1)

    # DownloadReports(driver).load_file_api_and_open(file_path, opened_in_new_tab=False)  # загрузка всех файлов в папке
    # file_result = FileResultWindow(driver)
    # file_result.check_all_loading_successful(2)
    # file_result.close()
    # pmo_button = driver.find_element(By.CSS_SELECTOR, '[data-qa="toggleOperationsPanel"]')
    # pmo_button.click()
    # sleep(1)
    # check_box_pmo = driver.find_element(By.CSS_SELECTOR, '[data-qa="controls-CheckboxMarker_state-false"]')
    # check_box_pmo.click()
    # sleep(1)
    # remove_button = driver.find_element(By.CSS_SELECTOR, '[data-qa="remove"].controls-Toolbar__item_horizontal-spacing_medium')
    # remove_button.click()
    # sleep(1)
    # confirm_dialog_button_true = driver.find_element(By.CSS_SELECTOR, '[data-qa="controls-ConfirmationDialog__button-true"]')
    # confirm_dialog_button_true.click()
    # sleep(1)
    # delete_report_button = driver.find_element(By.CSS_SELECTOR, '[data-name="FilterViewPanel__additional-editor_deleted"]')
    # delete_report_button.click()
    # sleep(1)
    # check_box_pmo.click()
    # sleep(1)
    # remove_button.click()
    # sleep(1)
    # confirm_dialog_button_true_del = driver.find_element(By.CSS_SELECTOR, '[data-qa="controls-ConfirmationDialog__button-true"]')
    # confirm_dialog_button_true_del.click()
    # sleep(1)
    # close_pmo = driver.find_element(By.CSS_SELECTOR, '[data-qa="controls-OperationsPanel__close"]')
    # close_pmo.click()
    # sleep(1)
    # close_delete_report_button = driver.find_element(By.CSS_SELECTOR, '[data-qa="FilterViewPanel__baseEditor-cross"]')
    # close_delete_report_button.click()
    # sleep(1)
    # delete_report()

finally:

    sleep(2)
    driver.quit()

