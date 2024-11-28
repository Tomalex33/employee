from pages.base_page import BasePage
from file.locators import ReportPageLocators
from selenium.webdriver import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from time import sleep

name_org = "Новая сверка тест"


class ReportPage(BasePage):

    def should_be_report_button(self):
        assert self.is_element_present(*ReportPageLocators.REPORT_BUTTON), 'Не нашли кнопку перехода в раздел "Отчетность"'

    def delete_all_report(self):
        self.finds_element_and_click(*ReportPageLocators.PMO_BUTTON)
        self.finds_element_and_click(*ReportPageLocators.CHECK_PMO_BUTTON)
        self.finds_element_and_click(*ReportPageLocators.REMOTE_REPORT_BUTTON)
        self.finds_element_and_click(*ReportPageLocators.CONFIRM_DIALOG_BUTTON_TRUE)
        self.finds_element_and_click(*ReportPageLocators.BASKET_BUTTON_DELETE_REPORT)
        self.finds_element_and_click(*ReportPageLocators.CHECK_PMO_BUTTON)
        self.finds_element_and_click(*ReportPageLocators.REMOTE_REPORT_BUTTON)
        self.finds_element_and_click(*ReportPageLocators.CONFIRM_DIALOG_BUTTON_TRUE)
        self.finds_element_and_click(*ReportPageLocators.PMO_BUTTON_CLOSE)
        self.finds_element_and_click(*ReportPageLocators.CLOSE_BASKET_BUTTON)

    def check_basket_close(self):
        try:
            self.finds_element_and_click(*ReportPageLocators.CLOSE_BASKET_BUTTON)
        except NoSuchElementException:
            return True
        return True

    def check_filter_org(self):
        self.finds_element_and_select(*ReportPageLocators.ORG_NAME_FILTER, 'text')

