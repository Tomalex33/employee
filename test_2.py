from time import sleep
import pytest
import os
from pages.login_page import LoginPage
from pages.report_page import ReportPage
from file.action import DownloadReports, FileResultWindow

name_org = "Новая сверка тест"
period_1 = "I кв'24"
period_2 = "II кв'24"
link_fix = 'https://fix-sso.sbis.ru/auth-online/?ret=fix-online.sbis.ru'
link_report_fns = 'https://fix-online.sbis.ru/page/fns'
file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test-files\\case_2')
disc_number_test_1_1 = '6'
disc_number_test_1_2 = '4'


def test_case_sym2(driver):
    page = LoginPage(driver, link_fix)
    page.open()
    page.should_be_login_button()
    page.authorization()
    report_fns = ReportPage(driver, link_report_fns)
    report_fns.should_be_report_button()
    report_fns.open()
    # report_fns.check_filter_org(name_org)
    # report_fns.check_basket_close()
    DownloadReports(driver).load_file_api_and_open(file_path, opened_in_new_tab=False)  # загрузка всех файлов в папке
    file_result = FileResultWindow(driver)
    file_result.check_all_loading_successful(2)
    file_result.close()
    print(f'Выбираем РСВ за {period_1}')
    report_fns.select_report_by_period(period_1)
    report_fns.check_discrepancies(disc_number_test_1_1)
    report_fns.run_all_calc_in_subsection_1_rsv()
    sleep(10)
    report_fns.close_report()
    print(f'Выбираем РСВ за {period_2}')
    report_fns.select_report_by_period(period_2)
    report_fns.check_discrepancies(disc_number_test_1_2)
    report_fns.run_all_calc_in_subsection_1_rsv()
    sleep(10)
    report_fns.check_not_discrepancies()
    report_fns.close_report()
    report_fns.delete_all_report()
    sleep(1)
