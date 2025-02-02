import os
from time import sleep
from pages.login_page import LoginPage
from pages.report_page import ReportPage
from file.action import DownloadReports, FileResultWindow
import pytest


link_fix = 'https://fix-sso.sbis.ru/auth-online/?ret=fix-online.sbis.ru'
link_report_fns = 'https://fix-online.sbis.ru/page/fns'
name_org = "Новая сверка тест"
fio = "Иванов Константин Олегович"
report_rsv = 'Расчет по страховым взносам'
report_persved = 'Персонифицированные сведения'
file_path2 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test-files\\case_2')
file_path3 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test-files\\case_3')
period_1_24 = "I кв'24"
period_2_24 = "II кв'24"
period_3_24 = "III кв'24"


@pytest.mark.usefixtures("browser_setup")
class TestSym:

    def setup_class(cls):
        cls.driver.maximize_window()
        cls.driver.get(link_fix)
        sleep(2)
        cls.page_login = LoginPage(cls.driver)
        sleep(2)
        cls.page_login.authorization()
        sleep(6)
        cls.report_page = ReportPage(cls.driver)
        cls.report_page.should_be_report_button()
        cls.driver.get(link_report_fns)
        cls.report_page.check_filter_org(name_org)
        cls.report_page.check_basket_close()
        print("Выполнится 1 раз перед всеми тестами в классе")
        print("Запуск браузера")
        print("Открываем страничку ФНС")
        print("Проверяем выбранную организацию")
        print("Закрыта ли корзина")

    def setup_method(self):
        print("\nВыполняется перед каждым тестом")
        print("Проверяем удалены ли все комплекты")

    def teardown_method(self):
        print("\nВыполняется после каждого теста, независимо от успешности setup_method")
        print("Удаляем созданные отчеты")
        self.report_page.delete_all_report()

    @classmethod
    def teardown_class(cls):
        print("\nВыполняется 1 раз после всех тестов в классе")
        print("Закрываем браузер")
        cls.driver.quit()

    def test1(self):
        print("\nВыполнение теста 1")
        self.report_page.created_report('2022', '12')
        self.report_page.choice_report(report_rsv)
        self.report_page.type_payer_choice()
        self.report_page.check_not_discrepancies()
        self.report_page.adding_employees_section_3(fio)
        self.report_page.adding_summ_month('1000.00')
        self.report_page.check_discrepancies("3")
        self.report_page.checking_text_for_discrepancies("01 - НР, ВЖНР, ВПНР - Расхождения между разделом 3 и приложением 1")
        self.report_page.close_report()

    def test2(self):
        print("\nВыполнение теста 2")
        DownloadReports(self.driver).load_file_api_and_open(file_path2, opened_in_new_tab=False)  # загрузка всех файлов в папке
        file_result = FileResultWindow(self.driver)
        file_result.check_all_loading_successful(2)
        file_result.close()
        self.report_page.select_report_by_period(period_1_24)
        self.report_page.check_discrepancies("6")  # проверяем количество расхождений
        self.report_page.run_all_calc_in_subsection_1_rsv()
        self.report_page.close_report()
        self.report_page.select_report_by_period(period_2_24)
        self.report_page.check_discrepancies("4")
        self.report_page.run_all_calc_in_subsection_1_rsv()
        self.report_page.check_not_discrepancies()
        self.report_page.close_report()

    def test3(self):
        print("\nВыполнение теста 3")
        DownloadReports(self.driver).load_file_api_and_open(file_path3, opened_in_new_tab=False)  # загрузка всех файлов в папке
        file_result = FileResultWindow(self.driver)
        file_result.check_all_loading_successful(3)
        file_result.close()
        self.report_page.select_report_by_period(period_3_24)
        self.report_page.check_discrepancies("23")
        self.report_page.run_all_calc_in_employee_card()
        self.report_page.check_not_discrepancies()
        self.report_page.close_report()

    def test4(self):
        print("\nВыполнение теста 4")
        self.report_page.created_report('2024', '12')
        self.report_page.choice_report(report_rsv)
        self.report_page.type_payer_choice()
        self.report_page.check_not_discrepancies()
        self.report_page.number_of_insured_persons('1')
        self.report_page.adding_employees_section_3(fio)
        self.report_page.adding_summ_month_2('100000.00')
        self.report_page.close_report()
        self.report_page.created_report('2024', '12')
        self.report_page.choice_report(report_persved)
        self.report_page.save_report()
        self.report_page.adding_employees_ps(fio)
        self.report_page.close_data_menu()
        self.report_page.checking_text_for_discrepancies_ps('Расхождение сумм выплат по сотруднику между отчетами РСВ и ПерсСвед', '100 000')
        self.report_page.click_on_hover_ps('111 111.11')
        self.report_page.check_not_discrepancies_ps()
        self.report_page.close_report()
