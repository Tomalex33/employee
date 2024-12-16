from pages.base_page import BasePage
from file.locators import ReportPageLocators, RVSLocators
from selenium.common.exceptions import NoSuchElementException
from time import sleep


class ReportPage(BasePage):

    def should_be_report_button(self):
        assert self.is_element_present(*ReportPageLocators.REPORT_BUTTON), 'Не нашли кнопку перехода в раздел "Отчетность"'

    def delete_all_report(self):
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

    def close_report(self):
        self.finds_element_and_click(*ReportPageLocators.CLOSE_REPORT)
        sleep(2)

    def created_report(self, years_text, report):
        self.finds_element_and_click(*ReportPageLocators.CREATED_REPORT)
        sleep(1)
        self.finds_element_and_click(*ReportPageLocators.ALL_LIST_REPORT)
        sleep(1)
        self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT)
        sleep(1)
        current_years = self.driver.find_element(*ReportPageLocators.CURRENT_YEARS)
        sleep(1)
        if current_years.text == years_text:
            self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2022)
            sleep(1)
        elif current_years.text > years_text:
            self.finds_element_and_click(*ReportPageLocators.LEFT_YEARS)
            sleep(1)
            if current_years.text != years_text:
                self.finds_element_and_click(*ReportPageLocators.LEFT_YEARS)
                sleep(1)
                self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2022)
                sleep(1)
            else:
                self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2022)
        elif current_years.text < years_text:
            self.finds_element_and_click(*ReportPageLocators.RIGHT_YEARS)
            sleep(1)
            self.finds_element_and_click(*ReportPageLocators.PERIOD_REPORT_4_2022)
            sleep(1)
        self.finds_elements_and_send_keys(*ReportPageLocators.REPORT_FIND, report)
        sleep(1)
        self.finds_element_and_click(*ReportPageLocators.CHOICE_FIND_REPORT)
        sleep(1)
        self.is_element_present(*RVSLocators.MAIN)

    def check_discrepancies(self, disc_number):
        disc = self.driver.find_element(*ReportPageLocators.DISC)
        assert disc.text == disc_number, f'Фактическое значение {disc.text} \n Количество расхождений отличается от эталонного значения = {disc_number}'
        sleep(1)

    def check_not_discrepancies(self):
        disc_not = self.driver.find_element(*ReportPageLocators.DISC_NOT)
        assert disc_not.text == 'Расхождений нет', 'Не должно быть расхождений, ошибка'
        sleep(1)

    def run_all_calc_in_subsection_1_rsv(self, text_value):
        self.finds_element_and_click(*RVSLocators.SUBSECTION_1)
        self.finds_element_and_click(*RVSLocators.RUN_ALL_CALC_RSV_IN_SUBSECTION_1)
        self.finds_element_and_click(*RVSLocators.CONFIRM_CALC)
        self.is_element_present_value(*RVSLocators.STRING_51, text_value)
        sleep(2)

    def run_all_calc_in_employee_card(self, text_value):
        self.finds_element_and_click(*ReportPageLocators.DISC)
        self.finds_element_and_click(*RVSLocators.SYM_DISC_TEST3)
        self.finds_element_and_click(*RVSLocators.RUN_ALL_CALC_RSV_IN_EMPLOYEE_CARD)
        self.finds_element_and_click(*RVSLocators.CONFIRM_CALC)
        self.is_element_present_value(*RVSLocators.STRING_210_1_MONTH, text_value)
        self.finds_element_and_click(*RVSLocators.CONFIRM_CHANGE_EMPLOYEE_CARD)

