from selenium import webdriver
from time import sleep
import unittest
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import pytest
from pages.login_page import LoginPage


# @pytest.mark.usefixtures("print_name")
class Test:

    @classmethod
    def setup_class(cls):
        print("Выполнится 1 раз перед всеми тестами в классе")
        print("Запуск браузера")
        print("Открываем страничку ФНС")
        print("Проверяем выбранную организацию")
        print("Закрыта ли корзина")

    def setup_method(self):
        print("\nВыполняется перед каждым тестом")
        print("Проверяем удалены ли все комплекты")

    def test1(self):
        print("\nВыполнение теста 1")

    def test2(self):
        print("\nВыполнение теста 2")

    def teardown_method(self):
        print("\nВыполняется после каждого теста, независимо от успешности setup_method")
        print("Удаляем созданные отчеты")

    @classmethod
    def teardown_class(cls):
        print("\nВыполняется 1 раз после всех тестов в классе")
        print("Закрываем браузер")


# class TestFixture:
#
#     def test1(self, print_name, print_name1):
#         print("\nВыполнение теста 1")
#
#     def test2(self, print_name, print_name1):
#         print("\nВыполнение теста 2")


