from time import sleep
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import pytest
import os
from pages.login_page import LoginPage
from pages.report_page import ReportPage
from file.action import DownloadReports, FileResultWindow


link_fix = 'https://fix-sso.sbis.ru/auth-online/?ret=fix-online.sbis.ru'
link_report_fns = 'https://fix-online.sbis.ru/page/fns'
file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test-files\\case_2')


def test_1(driver):
    page = LoginPage(driver, link_fix)
    page.open()
    page.should_be_login_button()
    sleep(1)
    page.authorization()
    report_fns = ReportPage(driver, link_report_fns)
    report_fns.should_be_report_button()
    report_fns.open()
    sleep(1)
    # report_fns.check_basket_close()
    report_fns.check_filter_org()
    # DownloadReports(driver).load_file_api_and_open(file_path, opened_in_new_tab=False)  # загрузка всех файлов в папке
    # file_result = FileResultWindow(driver)
    # file_result.check_all_loading_successful(2)
    # file_result.close()
    # sleep(2)
    # report_fns.delete_all_report()
    sleep(1)
