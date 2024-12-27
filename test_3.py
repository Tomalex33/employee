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
report_rsv = 'Расчет по страховым взносам'
report_persved = 'Персонифицированные сведения'
fio = "Иванов Константин Олегович"


def test_case_pd1(driver):
    page = LoginPage(driver, link_fix)
    page.open()
    page.should_be_login_button()
    page.authorization()
    report_fns = ReportPage(driver, link_report_fns)
    report_fns.should_be_report_button()
    report_fns.open()
    report_fns.check_filter_org(name_org)
    report_fns.check_basket_close()
    report_fns.created_report_2024('2024', report_rsv)
