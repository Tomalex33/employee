from time import sleep
import pytest
import os
from pages.login_page import LoginPage
from pages.Start import Start
from pages.report_page import ReportPage
from file.action import DownloadReports, FileResultWindow
from pages.base_page import BasePage
from selenium import webdriver

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
disc_number_test_1_1 = "3"
disc_number_test_2_1 = '6'
disc_number_test_2_2 = '4'
disc_number_test_3_1 = '23'
report_rsv = 'Расчет по страховым взносам'
report_persved = 'Персонифицированные сведения'
fio = "Иванов Константин Олегович"
sym_140 = '1000.00'
disc_text_standard = "01 - НР, ВЖНР, ВПНР - Расхождения между разделом 3 и приложением 1"


class TestSym(LoginPage):

    @classmethod
    def setup_class(cls):
        page = LoginPage(cls.driver, link_fix)
        page.open()
        page.should_be_login_button()
        page.authorization()
        print("\nВыполнится 1 раз перед всеми тестами в классе")

    def setup_method(self):
        print("\nВыполняется перед каждым тестом")

    def teardown_method(self):
        print("\nВыполняется после каждого теста, независимо от успешности setup_method")

    @classmethod
    def teardown_class(cls):
        print("\nВыполняется 1 раз после всех тестов в классе")

    def test1(self):
        print("\nВыполнение теста 1")

    def test2(self):
        print("\nВыполнение теста 2")
