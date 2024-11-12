from selenium import webdriver
from time import sleep
import unittest
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import pytest
from base_page import BasePage

link_fix = 'https://fix-sso.sbis.ru/auth-online/?ret=fix-online.sbis.ru'
link_sbis = "https://sbis.ru/"


def test_1(driver):
    page = BasePage(driver, link_fix)
    page.open()
    sleep(2)

