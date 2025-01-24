import pytest
from selenium import webdriver
from time import sleep

# class Start:
#     driver = None
#
#     @classmethod
#     def setup_class(cls):
#         cls.driver = webdriver.Chrome()


    # def driver(self):
    #     print("\nstart browser for test..")
    #     driver = webdriver.Chrome()
    #     driver.maximize_window()
    #     yield driver
    #     print("\nquit browser..")
    #     driver.quit()
class RunBrowser:

    def __init__(self):
        self.driver = None

    def run_chrome(self):
        self.driver = webdriver.Chrome()

    def open(self):
        self.driver.get('https://test-sso.sbis.ru/auth-online/?ret=test-online.sbis.ru')

    def close(self):
        self.driver.quit()


driver = RunBrowser()
driver.run_chrome()
driver.open()
sleep(1)
driver.close()
