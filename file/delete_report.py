from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from file.driver import driver



def delete_report():

    pmo_button = driver.find_element(By.CSS_SELECTOR, '[data-qa="toggleOperationsPanel"]')
    pmo_button.click()
    sleep(1)
    check_box_pmo = driver.find_element(By.CSS_SELECTOR, '[data-qa="controls-CheckboxMarker_state-false"]')
    check_box_pmo.click()
    sleep(1)
    remove_button = driver.find_element(By.CSS_SELECTOR,
                                        '[data-qa="remove"].controls-Toolbar__item_horizontal-spacing_medium')
    remove_button.click()
    sleep(1)
    confirm_dialog_button_true = driver.find_element(By.CSS_SELECTOR,
                                                     '[data-qa="controls-ConfirmationDialog__button-true"]')
    confirm_dialog_button_true.click()
    sleep(1)
    delete_report_button = driver.find_element(By.CSS_SELECTOR,
                                               '[data-name="FilterViewPanel__additional-editor_deleted"]')
    delete_report_button.click()
    sleep(1)
    check_box_pmo.click()
    sleep(1)
    remove_button.click()
    sleep(1)
    confirm_dialog_button_true_del = driver.find_element(By.CSS_SELECTOR,
                                                         '[data-qa="controls-ConfirmationDialog__button-true"]')
    confirm_dialog_button_true_del.click()
    sleep(1)
    close_pmo = driver.find_element(By.CSS_SELECTOR, '[data-qa="controls-OperationsPanel__close"]')
    close_pmo.click()
    sleep(1)
    close_delete_report_button = driver.find_element(By.CSS_SELECTOR, '[data-qa="FilterViewPanel__baseEditor-cross"]')
    close_delete_report_button.click()
    sleep(1)
