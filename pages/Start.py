import pytest
from selenium import webdriver


class Start:


    def driver(self):
        print("\nstart browser for test..")
        driver = webdriver.Chrome()
        driver.maximize_window()
        yield driver
        print("\nquit browser..")
        driver.quit()
