from time import sleep
import pytest
import os
from pages.login_page import LoginPage
from pages.report_page import ReportPage
from file.action import DownloadReports, FileResultWindow

name_org = "Новая сверка тест"
period_1_24 = "I кв'24"
period_2_24 = "II кв'24"
period_3_24 = "III кв'24"
link_fix = 'https://fix-sso.sbis.ru/auth-online/?ret=fix-online.sbis.ru'
link_report_fns = 'https://fix-online.sbis.ru/page/fns'
link_test = 'https://test-sso.sbis.ru/auth-online/?ret=test-online.sbis.ru'
link_report_test_fns = 'https://test-online.sbis.ru/page/fns'
file_path2 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test-files\\case_2')
file_path3 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test-files\\case_3')
disc_number_test_2_1 = '6'
disc_number_test_2_2 = '4'
disc_number_test_3_1 = '23'
text_value_2_1 = '75 000.00'
text_value_2_2 = '150 000.00'
text_value_3_1 = '10 530.05'
years_text = '2022'
report_rsv = 'Расчет по страховым взносам'
fio = "Иванов Константин Олегович"
sym_140 = '1000'


def test_case_sym1(driver):
    page = LoginPage(driver, link_fix)
    page.open()
    page.should_be_login_button()
    page.authorization()
    report_fns = ReportPage(driver, link_report_fns)
    report_fns.should_be_report_button()
    report_fns.open()
    # report_fns.check_filter_org(name_org)
    # report_fns.check_basket_close()
    report_fns.created_report(years_text, report_rsv)
    report_fns.type_payer_choice()
    report_fns.check_not_discrepancies()
    report_fns.adding_employees_section_3(fio, sym_140)
    sleep(1)


def test_case_sym2(driver):
    page = LoginPage(driver, link_fix)
    page.open()
    page.should_be_login_button()
    page.authorization()
    report_fns = ReportPage(driver, link_report_fns)
    report_fns.should_be_report_button()
    report_fns.open()
    report_fns.check_filter_org(name_org)
    report_fns.check_basket_close()
    DownloadReports(driver).load_file_api_and_open(file_path2, opened_in_new_tab=False)  # загрузка всех файлов в папке
    file_result = FileResultWindow(driver)
    file_result.check_all_loading_successful(2)
    file_result.close()
    report_fns.select_report_by_period(period_1_24)
    report_fns.check_discrepancies(disc_number_test_2_1)  # проверяем количество расхождений
    report_fns.run_all_calc_in_subsection_1_rsv(text_value_2_1)
    report_fns.close_report()
    report_fns.select_report_by_period(period_2_24)
    report_fns.check_discrepancies(disc_number_test_2_2)
    report_fns.run_all_calc_in_subsection_1_rsv(text_value_2_2)
    report_fns.check_not_discrepancies()
    report_fns.close_report()
    report_fns.delete_all_report()
    sleep(1)


def test_case_sym3(driver):
    page = LoginPage(driver, link_fix)
    page.open()
    page.should_be_login_button()
    page.authorization()
    report_fns = ReportPage(driver, link_report_fns)
    report_fns.should_be_report_button()
    report_fns.open()
    report_fns.check_filter_org(name_org)
    report_fns.check_basket_close()
    DownloadReports(driver).load_file_api_and_open(file_path3, opened_in_new_tab=False)  # загрузка всех файлов в папке
    file_result = FileResultWindow(driver)
    file_result.check_all_loading_successful(3)
    file_result.close()
    report_fns.select_report_by_period(period_3_24)
    report_fns.check_discrepancies(disc_number_test_3_1)
    report_fns.run_all_calc_in_employee_card(text_value_3_1)
    report_fns.check_not_discrepancies()
    report_fns.close_report()
    report_fns.delete_all_report()
    sleep(1)
