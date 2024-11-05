from selenium import webdriver
from time import sleep
import unittest
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import pytest

sbis_site = 'https://sbis.ru/'




def setUp(self):
    self.driver = webdriver.Chrome()


def test_example(self):
    self.driver.get(sbis_site)
    sleep(2)


def tearDown(self):
    self.driver.close()


