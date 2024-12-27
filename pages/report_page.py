from pages.base_page import BasePage
from file.locators import ReportPageLocators, RVSLocators, PerSvedLocators
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium.webdriver import ActionChains


class ReportPage(BasePage):

    def should_be_report_button(self):
        assert self.is_element_present(*ReportPageLocators.REPORT_BUTTON), 'Не нашли кнопку перехода в раздел "Отчетность"'

    def delete_all_report(self):
        # locators_del = [*ReportPageLocators.PMO_BUTTON, *ReportPageLocators.CHECK_PMO_BUTTON, *ReportPageLocators.REMOTE_REPORT_BUTTON, *ReportPageLocators.CONFIRM_DIALOG_BUTTON_TRUE,
        #                 *ReportPageLocators.BASKET_BUTTON, *ReportPageLocators.CHECK_PMO_BUTTON, *ReportPageLocators.REMOTE_REPORT_BUTTON, *ReportPageLocators.CONFIRM_DIALOG_BUTTON_TRUE,
        #                 *ReportPageLocators.PMO_BUTTON_CLOSE, *ReportPageLocators.BASKET_BUTTON_CLOSE]
        # for i, j in locators_del:
        #     self.finds_element_and_click(i, j)
        self.finds_element_and_click(*ReportPageLocators.PMO_BUTTON)
        self.finds_element_and_click(*ReportPageLocators.CHECK_PMO_BUTTON)
        self.finds_element_and_click(*ReportPageLocators.REMOTE_REPORT_BUTTON)
        self.finds_element_and_click(*ReportPageLocators.CONFIRM_DIALOG_BUTTON_TRUE)
        self.finds_element_and_click(*ReportPageLocators.BASKET_BUTTON)
        self.finds_element_and_click(*ReportPageLocators.CHECK_PMO_BUTTON)
        self.finds_element_and_click(*ReportPageLocators.REMOTE_REPORT_BUTTON)
        self.finds_element_and_click(*ReportPageLocators.CONFIRM_DIALOG_BUTTON_TRUE)
        self.finds_element_and_click(*ReportPageLocators.PMO_BUTTON_CLOSE)
        self.finds_element_and_click(*ReportPageLocators.BASKET_BUTTON_CLOSE)

    def check_basket_close(self):
        try:
            self.finds_element_and_click(*ReportPageLocators.BASKET_BUTTON_CLOSE)
            sleep(2)
        except NoSuchElementException:
            return True
        return True

    def check_filter_org(self, name_org):
        self.finds_element_and_click(*ReportPageLocators.ICON_FILTER_ORG)
        self.finds_element_and_click(*ReportPageLocators.RESET_ORG_IN_FILTER)
        self.finds_element_and_click(*ReportPageLocators.FILTER_ORG_APPLY)
        self.finds_element_and_click(*ReportPageLocators.ORG_ALL)
        self.finds_elements_and_send_keys(*ReportPageLocators.ORG_FIND, name_org)
        self.finds_element_and_click(*ReportPageLocators.ORG_CHOICE)

    def select_report_by_period(self, period):
        self.finds_elements_contain_text(*ReportPageLocators.PERIOD_CHOICE, period)
        self.is_element_present(*ReportPageLocators.SAVE_REPORT)

    def created_report_2022(self, years_text, report):
        self.finds_element_and_click(*ReportPageLocators.CREATED_REPORT)
        sleep(1)
        self.finds_element_and_click(*ReportPageLocators.ALL_LIST_REPORT)
        sleep(1)
        self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT)
        sleep(1)
        current_years = self.driver.find_element(*ReportPageLocators.CURRENT_YEARS)
        sleep(1)
        if current_years.text == years_text:
            self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2022_12)
            sleep(1)
        elif current_years.text > years_text:
            self.finds_element_and_click(*ReportPageLocators.LEFT_YEARS)
            sleep(1)
            if current_years.text != years_text:
                self.finds_element_and_click(*ReportPageLocators.LEFT_YEARS)
                sleep(1)
                self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2022_12)
                sleep(1)
            else:
                self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2022_12)
        elif current_years.text < years_text:
            self.finds_element_and_click(*ReportPageLocators.RIGHT_YEARS)
            sleep(1)
            if current_years.text != years_text:
                self.finds_element_and_click(*ReportPageLocators.RIGHT_YEARS)
                sleep(1)
                self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2022_12)
                sleep(1)
            else:
                self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2022_12)
        self.finds_elements_and_send_keys(*ReportPageLocators.REPORT_FIND, report)
        sleep(1)
        self.finds_element_and_click(*ReportPageLocators.CHOICE_FIND_REPORT)
        sleep(1)

    def created_report_2024(self, years_text, report):
        self.finds_element_and_click(*ReportPageLocators.CREATED_REPORT)
        sleep(1)
        self.finds_element_and_click(*ReportPageLocators.ALL_LIST_REPORT)
        sleep(1)
        self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT)
        sleep(1)
        current_years = self.driver.find_element(*ReportPageLocators.CURRENT_YEARS)
        sleep(1)
        if current_years.text == years_text:
            self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2024_12)
            sleep(1)
        elif current_years.text > years_text:
            self.finds_element_and_click(*ReportPageLocators.LEFT_YEARS)
            sleep(1)
            if current_years.text != years_text:
                self.finds_element_and_click(*ReportPageLocators.LEFT_YEARS)
                sleep(1)
                self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2024_12)
                sleep(1)
            else:
                self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2024_12)
        elif current_years.text < years_text:
            self.finds_element_and_click(*ReportPageLocators.RIGHT_YEARS)
            sleep(1)
            if current_years.text != years_text:
                self.finds_element_and_click(*ReportPageLocators.RIGHT_YEARS)
                sleep(1)
                self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2024_12)
                sleep(1)
            else:
                self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2024_12)
        self.finds_elements_and_send_keys(*ReportPageLocators.REPORT_FIND, report)
        sleep(1)
        self.finds_element_and_click(*ReportPageLocators.CHOICE_FIND_REPORT)
        sleep(1)

    def save_report(self):
        sleep(2)
        self.is_element_present(*ReportPageLocators.SAVE_REPORT)
        self.finds_element_and_click(*ReportPageLocators.SAVE_REPORT)
        self.is_element_present_text(*ReportPageLocators.REPORT_CREATED)
        sleep(2)

    def close_report(self):
        sleep(1)
        self.finds_element_and_click(*ReportPageLocators.CLOSE_REPORT)
        sleep(2)

    def check_discrepancies(self, disc_number):
        disc = self.driver.find_element(*ReportPageLocators.DISC)
        assert disc.text == disc_number, f'Фактическое значение {disc.text} \n Количество расхождений отличается от эталонного значения = {disc_number}'
        print(f"Количество расхождений соответствует эталонному значению {disc_number}")
        sleep(1)

    def check_not_discrepancies(self):
        sleep(1)
        disc_not = self.driver.find_element(*ReportPageLocators.DISC_NOT)
        assert disc_not.text == 'Расхождений нет', 'Не должно быть расхождений, ошибка'
        print(f"Расхождений нет") 
        sleep(1)

    def check_not_discrepancies_ps(self):
        sleep(1)
        self.is_element_present_text_1(*PerSvedLocators.DISC_NOT_PS, "Расхождений нет")
        disc_not = self.driver.find_element(*PerSvedLocators.DISC_NOT_PS)
        assert disc_not.text == 'Расхождений нет', 'Не должно быть расхождений, ошибка'
        print(f"Расхождений нет")
        sleep(1)

    def run_all_calc_in_subsection_1_rsv(self):
        self.finds_element_and_click(*RVSLocators.SUBSECTION_1)
        self.finds_element_and_click(*RVSLocators.RUN_ALL_CALC_RSV_IN_SUBSECTION_1)
        self.finds_element_and_click(*RVSLocators.CONFIRM_CALC)
        self.is_element_present_text(*ReportPageLocators.REPORT_CREATED)
        sleep(2)

    def run_all_calc_in_employee_card(self, text_value):
        self.finds_element_and_click(*ReportPageLocators.DISC)
        self.finds_element_and_click(*RVSLocators.SYM_DISC_TEST3)
        self.finds_element_and_click(*RVSLocators.RUN_ALL_CALC_RSV_IN_EMPLOYEE_CARD)
        self.finds_element_and_click(*RVSLocators.CONFIRM_CALC)
        self.is_element_present_value(*RVSLocators.STRING_210_1_MONTH, text_value)
        self.finds_element_and_click(*RVSLocators.CONFIRM_CHANGE_EMPLOYEE_CARD)

    def type_payer_choice(self):
        self.is_element_clickable(*RVSLocators.MAIN)
        sleep(1)
        print('проверка что Раздел 1 присутствует')
        self.is_element_present(*RVSLocators.SECTION_1)
        print('поиск Раздела 1 и клик по нему')
        self.finds_element_and_click(*RVSLocators.SECTION_1)
        print('ждем появления надписи "Отчет создан"')
        self.is_element_present_text(*ReportPageLocators.REPORT_CREATED)
        sleep(2)
        print('Выбор типа плательщика"')
        self.finds_element_and_click(*RVSLocators.TYPE_PAYER)
        print('Выбираем тип плательщика - 1"')
        self.finds_element_and_click(*RVSLocators.TYPE_PAYER_1)
        print('проверка что выбран тип плательщика - 1"')
        check_text = self.driver.find_element(*RVSLocators.CHECK_TEXT_TYPE_PAYER_1)
        assert check_text.text == '1 - Выплаты физ. лицам осуществлялись', 'Текст не соответсвует эталонному "1 - Выплаты физ. лицам осуществлялись"'

    def adding_employees_section_3(self, fio):
        print('\nПроверяем что раздел 3 загружен')
        self.is_element_present(*RVSLocators.SECTION_3)
        print('Кликаем на раздел 3')
        self.finds_element_and_click(*RVSLocators.SECTION_3)
        print('Кликаем на добавления сотрудника')
        self.finds_element_and_click(*RVSLocators.ADD_EMPLOYEES_SECTION_3)
        print('Проверяем что кнопка добавления сотрудников в карточке сотрудников присутствует')
        self.is_element_present(*RVSLocators.BUTTON_ADD_EMPLOYEES_IN_CARD)
        self.finds_element_and_send_keys_text(*RVSLocators.FIND_EMPLOYEE, fio)
        self.finds_element_and_click(*RVSLocators.CHOICE_FIND_EMPLOYEE)
        self.is_element_present(*RVSLocators.CONFIRM_CHANGE_EMPLOYEE_CARD)
        sleep(1)

    def adding_summ_month(self, sym_140):
        self.finds_element_and_click(*RVSLocators.ADD_MONTH_EMPLOYEE_CARD)
        self.finds_element_click_send_keys_text(*RVSLocators.STRING_140, sym_140)
        self.finds_element_and_click(*RVSLocators.CONFIRM_CHANGE_STRING_MONTH)
        self.finds_element_and_click(*RVSLocators.ADD_MONTH_EMPLOYEE_CARD)
        self.finds_element_and_click(*RVSLocators.CHOICE_MONTH_EMPLOYEE_CARD)
        self.finds_element_and_click(*RVSLocators.CHOICE_MONTH_EMPLOYEE_CARD_NOV)
        self.finds_element_click_send_keys_text(*RVSLocators.STRING_140, sym_140)
        self.finds_element_and_click(*RVSLocators.CONFIRM_CHANGE_STRING_MONTH)
        self.finds_element_and_click(*RVSLocators.ADD_MONTH_EMPLOYEE_CARD)
        self.finds_element_and_click(*RVSLocators.CHOICE_MONTH_EMPLOYEE_CARD)
        self.finds_element_and_click(*RVSLocators.CHOICE_MONTH_EMPLOYEE_CARD_DEC)
        self.finds_element_click_send_keys_text(*RVSLocators.STRING_140, sym_140)
        self.finds_element_and_click(*RVSLocators.CONFIRM_CHANGE_STRING_MONTH)
        self.finds_element_and_click(*RVSLocators.CONFIRM_CHANGE_EMPLOYEE_CARD)
        self.finds_element_and_click(*ReportPageLocators.SAVE_REPORT)
        sleep(2)
        self.is_element_present_text(*ReportPageLocators.REPORT_CREATED)
        sleep(1)

    def adding_summ_month_2(self, sym):  # один месяц декабрь, суммы одинаковые
        self.finds_element_and_click(*RVSLocators.ADD_MONTH_EMPLOYEE_CARD)
        self.finds_element_and_click(*RVSLocators.CHOICE_MONTH_EMPLOYEE_CARD)
        self.finds_element_and_click(*RVSLocators.CHOICE_MONTH_EMPLOYEE_CARD_DEC)
        self.finds_element_click_send_keys_text(*RVSLocators.STRING_140, sym)
        self.finds_element_click_send_keys_text(*RVSLocators.STRING_150, sym)
        self.finds_element_and_click(*RVSLocators.CONFIRM_CHANGE_STRING_MONTH)
        self.finds_element_and_click(*RVSLocators.CONFIRM_CHANGE_EMPLOYEE_CARD)
        sleep(1)
        self.finds_element_and_click(*ReportPageLocators.SAVE_REPORT)
        sleep(1)
        self.is_disappeared(*RVSLocators.MESSAGE_IN_HEADER_DISC_REPORT)

    def checking_text_for_discrepancies(self, disc_text_standard):
        self.finds_element_and_click(*ReportPageLocators.DISC_SECTION)
        sleep(2)
        disc = self.driver.find_element(*ReportPageLocators.DISC_NAME_CONTENT)
        assert disc.text == disc_text_standard, f'\nФактический текст расхождения \\{disc.text}\\ \nотличается от эталонного текста \\{disc_text_standard}\\'
        print('\nЭталонный текст совпадает с текущим')

    def checking_text_for_discrepancies_ps(self, disc_text_standard, disc_text_standard1):
        sleep(1)
        disc = self.driver.find_element(*ReportPageLocators.DISC_NAME_CONTENT)
        assert disc.text == disc_text_standard, f'\nФактический текст расхождения \\{disc.text}\\ \nотличается от эталонного текста \\{disc_text_standard}\\'
        print('\nЭталонный текст совпадает с текущим')
        disc1 = self.driver.find_element(*PerSvedLocators.SYM_DISC_TEST4)
        assert disc1.text == disc_text_standard1, f'\nФактический текст расхождения \\{disc1.text}\\ \nотличается от эталонного текста \\{disc_text_standard1}\\'
        print('\nЭталонный текст совпадает с текущим')

    def click_on_hover_ps(self, sym_ps):
        element_hover = self.driver.find_element(*PerSvedLocators.MOVE_TO_DISPLAY_HOVER)
        hover = ActionChains(self.driver).move_to_element(element_hover)
        hover.perform()
        sleep(1)
        self.finds_element_and_click(*PerSvedLocators.DISC_V_PERSVED_HOVER)
        self.finds_element_click_send_keys_text(*PerSvedLocators.SYMM_CARD_PS, sym_ps)
        self.finds_element_and_click(*PerSvedLocators.CONFIRM_CHANGE_EMPLOYEE_CARD_PS)

    def close_data_menu(self):
        self.finds_element_and_click(*PerSvedLocators.CLOSE_FILL_ACC_DATA)
        sleep(1)

    def number_of_insured_persons(self, number):
        self.finds_element_and_click(*RVSLocators.SUBSECTION_1)
        self.finds_element_click_send_keys_text(*RVSLocators.STRING_10_ALL_MONTH, number)
        self.finds_element_click_send_keys_text(*RVSLocators.STRING_10_MONTH_3, number)

    def adding_employees_ps(self, fio):
        self.finds_element_and_click(*PerSvedLocators.ADD_EMPLOYEES)
        self.is_element_present(*PerSvedLocators.BUTTON_ADD_EMPLOYEES_IN_CARD_PERS)
        self.finds_element_and_send_keys_text(*RVSLocators.FIND_EMPLOYEE, fio)
        self.finds_element_and_click(*RVSLocators.CHOICE_FIND_EMPLOYEE)
        self.is_element_present(*PerSvedLocators.CONFIRM_CHANGE_EMPLOYEE_CARD_PS)
        self.finds_element_and_click(*PerSvedLocators.CONFIRM_CHANGE_EMPLOYEE_CARD_PS)
        sleep(1)
