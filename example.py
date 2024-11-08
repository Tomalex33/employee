from selenium import webdriver
from time import sleep
import unittest
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import pytest
from conftest import browser
# from exam import Start



# @pytest.fixture(scope='class')
# def browser():
#     driver = webdriver.Chrome()
#     driver.implicitly_wait(25)
#     driver.get(sbis_site)


class Test():
    @classmethod
    def setup_class(cls):  # выполнится 1 раз перед всеми тестами в классе
        browser()

    def setup_method(self):  # Выполняется перед каждым тестом
        pass
#
    def test_1(self): # выполнение теста
        pass


#    def setUp(self):
#       self.driver = webdriver.Chrome()
#
#
#    def test_example(self):
#       self.driver.get(sbis_site)
#       sleep(2)
#
#
#    def tearDown(self):
#     self.driver.close()
