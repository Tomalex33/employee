import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    print("\nstart browser for test..")
    driver = webdriver.Chrome()
    driver.maximize_window()
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
