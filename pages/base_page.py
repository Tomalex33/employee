from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.support.ui import Select


class BasePage:

    def __init__(self, driver, timeout=5):
        self.driver = driver
        # self.url = url
        self.driver.implicitly_wait(timeout)   # Неявное ожидание timeout - задаем значение в секундах

    # def open(self):
    #     self.driver.get(self.url)
    #     sleep(2)

    def is_element_present(self, how, what, timeout=30):  # Проверка, что элемент найден, если не найден обрабатываем исключение и тест падает по false
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((how, what)))
        except NoSuchElementException:
            return False
        return True

    def is_element_present_text(self, how, what, timeout=30, text='Отчет создан'):  # Проверка, что элемент найден имеет значение text
        try:
            WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element((how, what), text))
        except NoSuchElementException:
            return False
        return True

    def is_element_present_text_1(self, how, what, text, timeout=30):  # Проверка, что элемент найден имеет значение text
        try:
            WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element((how, what), text))
        except NoSuchElementException:
            return False
        return True

    def is_element_present_value(self, how, what, text_value, timeout=30):  # Проверка, что элемент найден, ждет пока значение value будет text_value
        try:
            WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element_value((how, what), text_value))
        except NoSuchElementException:
            return False
        return True

    def is_element_present_value1(self, how, what, timeout=30):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((how, what)))

    def is_not_element_present(self, how, what, timeout=1):  # упадет, как только увидит искомый элемент. Не появился: успех, тест зеленый.
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    def is_disappeared(self, how, what, timeout=10):  # будет ждать до тех пор, пока элемент не исчезнет.
        try:
            WebDriverWait(self.driver, timeout).until_not(EC.visibility_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    def finds_element_and_send_keys(self, how, what, text, keys):    # находим элемент пишем text, нажимаем кнопку
        element = self.driver.find_element(how, what)
        element.send_keys(text, keys)

    def finds_elements_and_send_keys(self, how, what, text):   # находим несколько элементов и выбираем первый + передаем текст
        element = self.driver.find_elements(how, what)
        sleep(1)
        element[0].send_keys(text)
        sleep(1)

    def finds_element_and_send_keys_text(self, how, what, text):   # находим элемент и передаем текст
        element = self.driver.find_element(how, what)
        sleep(1)
        element.send_keys(text)
        sleep(1)

    def finds_element_click_send_keys_text(self, how, what, text):   # находим элемент, кликаем по нему и передаем текст
        element = self.driver.find_element(how, what)
        sleep(1)
        element.click()
        element.send_keys(text)
        sleep(1)

    def finds_elements_contain_text(self, how, what, period):   # находим несколько элементов и выбираем по тексту
        periods = self.driver.find_elements(how, what)
        for i in periods:
            if i.text == period:
                i.click()

    def finds_element_and_click(self, how, what):
        element = self.driver.find_element(how, what)
        element.click()
        sleep(1)

    def finds_elements_and_click(self, how, what):               # находим первый элемент и кликаем по нему
        element = self.driver.find_elements(how, what)
        element[0].click()
        sleep(1)

    def finds_elements(self, how, what):               # находим первый элемент и кликаем по нему
        element = self.driver.find_elements(how, what)

        sleep(1)

    def finds_element_and_click_send_keys(self, how, what, text, keys):
        element = self.driver.find_element(how, what)
        element.click()
        element.send_keys(text, keys)

    def finds_element_and_select(self, how, what, text):
        select = Select(self.driver.find_element(how, what))
        select.select_by_value(text)

    def is_element_clickable(self, how, what, timeout=30):  # Ожидание проверки элемента видно и включено, так что вы можете нажать на него. элемент является либо локатором (текстом), либо WebElement
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((how, what)))
        except NoSuchElementException:
            return False
        return True
