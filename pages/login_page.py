from pages.base_page import BasePage
from file.locators import LoginPageLocators
from selenium.webdriver import Keys
from time import sleep

login_add = 'пчелкин'
pass_add = 'пчелкин123'

login_add_future = 'Январев'
pass_add_future = 'Январев123'


class LoginPage(BasePage):

    def authorization(self):
        self.finds_element_and_send_keys(*LoginPageLocators.LOGIN_FIELD, login_add, Keys.ENTER)
        self.finds_element_and_send_keys(*LoginPageLocators.PASSWORD_FIELD, pass_add, Keys.ENTER)

    def should_be_login_button(self):
        assert self.is_element_present(*LoginPageLocators.LOGIN_BUTTON_ENTER), 'Не нашли кнопку ввода логина'
        sleep(1)

    def should_be_login_field(self):
        assert self.is_element_present(*LoginPageLocators.LOGIN_FIELD), 'Не нашли поле ввода логина'

    def should_be_password_field(self):
        assert self.is_element_present(*LoginPageLocators.PASSWORD_FIELD), 'Не нашли поле ввода пароля'

    def url_text(self, url_text):  # проверка чтобы в url было слово url_text
        current_url = self.driver.current_url
        print(current_url)
        assert url_text in current_url, f'В ссылке нет слова {url_text}'



