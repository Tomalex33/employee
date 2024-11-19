from selenium.common.exceptions import NoSuchElementException


class BasePage:

    def __init__(self, driver, url, timeout=5):
        self.driver = driver
        self.url = url
        self.driver.implicitly_wait(timeout)   # Неявное ожидание timeout - задаем значение в секундах

    def open(self):
        self.driver.get(self.url)

    def is_element_present(self, how, what):  # Проверка, что элемент найден
        try:
            self.driver.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

