import pytest
from selenium import webdriver
from time import sleep


class RunBrowser:

    driver = webdriver.Chrome()
    # def __init__(self, driver):
    #     self.driver = driver

    def open(self, link):
        self.driver.get(link)

    def close(self):
        self.driver.quit()
