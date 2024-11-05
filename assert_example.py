from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()


# проверка url
# sbis_site = 'https://test.sbis.ru/'
# assert driver.current.url == sbis_site, 'Не верно открыт сайт'

# проверка title сайта
# sbis_title = 'СБИС'
# assert driver.title == sbis_title, 'Не верный заголовок'

# проверка сколько найдено элементов
# tabs = driver.find_elements(By.CLASS_NAME, 'NavigationPanels-Accordion__title')
# assert len(tabs) == 13, 'Должно быть 13 вкладкок'

# проверка соответствия текста у элемента
# tabs = driver.find_element(By.CLASS_NAME, 'NavigationPanels-Accordion__title')
# assert tabs.text == 'Какой то текст с которым сравниваем значение tabs.text', 'Не верный текст у элемента'

# проверка соответствия текста у атрибута
# tabs = driver.find_element(By.CLASS_NAME, 'NavigationPanels-Accordion__title')
# assert tabs.get_attribute('title') == 'Какой то текст с которым сравниваем значение get_attribute('title')', 'Не верный текст у атрбута'

# проверка на отображение элемента
# tabs = driver.find_element(By.CLASS_NAME, 'NavigationPanels-Accordion__title')
# assert tabs.is_displayed()

