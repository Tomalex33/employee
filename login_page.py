from base_page import BasePage
from file.locators import LoginPageLocators
from selenium.webdriver.common.by import By


class LoginPage(BasePage):

    def should_be_login_page(self):
        assert self.is_element_present(*LoginPageLocators.LOGIN_BUTTON_ENTER), 'Не нашли кнопку ввода логина'
