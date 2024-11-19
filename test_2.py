from selenium import webdriver
from time import sleep
import unittest
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import pytest
from login_page import LoginPage

link_fix = 'https://fix-sso.sbis.ru/auth-online/?ret=fix-online.sbis.ru'


def test_1(driver):
    page = LoginPage(driver, link_fix)
    page.open()
    page.url_text('fix')
    page.should_be_login_button()
    page.should_be_login_field()
    sleep(1)

