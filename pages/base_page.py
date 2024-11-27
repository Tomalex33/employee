from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class BasePage:

    def __init__(self, driver, url, timeout=5):
        self.driver = driver
        self.url = url
        self.driver.implicitly_wait(timeout)   # Неявное ожидание timeout - задаем значение в секундах

    def open(self):
        self.driver.get(self.url)

    def is_element_present(self, how, what, timeout=10):  # Проверка, что элемент найден, если не найден обрабатываем исключение и тест падает по false
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((how, what)))
        except NoSuchElementException:
            return False
        return True

    def is_element_present_simple(self, how, what, timeout=1):  # Простая проверка без условий
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return True

    def is_not_element_present(self, how, what, timeout=5):  # упадет, как только увидит искомый элемент. Не появился: успех, тест зеленый.
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    def is_disappeared(self, how, what, timeout=4):  # будет ждать до тех пор, пока элемент не исчезнет.
        try:
            WebDriverWait(self.driver, timeout, 1, TimeoutException). \
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    def finds_element_and_send_keys(self, how, what, text, keys):
        element = self.driver.find_element(how, what)
        element.send_keys(text, keys)

    def finds_element_and_click(self, how, what):
        element = self.driver.find_element(how, what)
        element.click()
        sleep(1)

    def finds_element(self, how, what):
        self.driver.find_element(how, what)
        sleep(1)

    def finds_element_and_click_send_keys(self, how, what, text, keys):
        element = self.driver.find_element(how, what)
        element.click()
        element.send_keys(text, keys)
