import pytest
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



login_add = 'пчелкин'
pas_add = 'пчелкин123'
report_page_link = "https://fix-online.sbis.ru/page/fns"
sbis_site = 'https://fix-online.sbis.ru/'


@pytest.fixture(scope="function")
def driver():
    print("\nstart browser for test..")
    driver = webdriver.Chrome()
    driver.maximize_window()
    # driver.implicitly_wait(10)
    # driver.get(sbis_site)
    # sleep(2)
    # login = driver.find_element(By.CSS_SELECTOR,
    #                             '.controls-InputBase__nativeField_caretFilled.controls-InputBase__nativeField_caretFilled_theme_default')
    # login.send_keys(login_add, Keys.ENTER)
    # pas = driver.find_element(By.CSS_SELECTOR, '.controls-Password__nativeField_caretFilled_theme_default')
    # sleep(1)
    # pas.send_keys(pas_add, Keys.ENTER)
    # sleep(1)
    # start_page = WebDriverWait(driver, 5).until(
    #     EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-qa='NavigationPanels-Accordion__title']")))
    # # проверка элемента на видимость,Ожидание проверки наличия элемента в DOM странице и видна. Видимость означает, что элемент не только отображается
    # # но также имеет высоту и ширину больше 0. локатор — используется для поиска элемента возвращает WebElement, как только он будет обнаружен и виден
    # driver.get(report_page_link)
    # report_page = WebDriverWait(driver, 5).until(
    #     EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-qa='sabyPage-addButton']")))
    yield driver
    print("\nquit browser..")
    driver.quit()
