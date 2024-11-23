from time import sleep
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import pytest
from pages.login_page import LoginPage

link_fix = 'https://fix-sso.sbis.ru/auth-online/?ret=fix-online.sbis.ru'


def test_1(driver):
    page = LoginPage(driver, link_fix)
    page.open()
    page.should_be_login_button()
    page.authorization()
    sleep(8)


