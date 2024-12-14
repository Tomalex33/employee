import os
import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains


sbis_site = 'https://sbis.ru/'


class Start:
    def __init__(self):
        self.driver = webdriver

    def browser(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(25)
        self.driver.get(sbis_site)


# @pytest.fixture()#выполняется для каждой функции
# def clean_cart(browser): #в функцию передаём имя функции-фикстуры, в которой инициализировали браузер (здесь эта фикстура “browser”)
#     yield #по завершении теста выполняется код, который идет после этой команды
#     print('yield')
#     browser.get(sbis_site)



# # Находит путь у файлу из текущей директории
# current_dir = os.path.abspath(os.path.dirname(__file__))
# file_path = os.path.join(current_dir, 'test-files\\case_2', 'NO_RASCHSV_6665_6665_9614602229961460222_20230207_0eb8d50d-d336-4f39-b245-7bcb1d874bb2.xml')


# код js CSS: делаем div-элемент невидимым/видимым, но макет не нарушаем!
# function toggleDivVisibilityKeepLayout(id) {
#   var el = document.getElementById(id); //вместо getElementById можно вставить querySelector и найти по селектору css
#   el.style.visibility = el.style.visibility === 'hidden' ? 'visible' : 'hidden';
# }
# toggleDivVisibilityKeepLayout("указываем id или селектор css")
# driver.execute_script('function toggleDivVisibilityKeepLayout(css) { var el = document.querySelector(css); el.style.visibility = el.style.visibility === "hidden" ? "visible" : "hidden"; } toggleDivVisibilityKeepLayout("[data-qa="controls-CheckboxMarker_state-true"]")')

# Подобную конструкцию необходимо знать и применять каждый раз, когда есть код, выполнение которого вы не хотите допустить во время импорта
# if __name__ == '__main__':

# Переход на новую вкладку браузера
# driver.switch_to.window(driver.window_handles[1])

# Текст url
# driver.current_url

# Открытие окна браузера на весь экран
# driver.maximize_window()

# action_chains = ActionChains(driver)
# action_chains.move_to_element(news) # Наведение на элемент
# action_chains.context_click(news) # контекстный клик на элемент
# action_chains.perform() # выполнение действий описанных ранее

# заморозка состояние у элемента,
# переходим на вкладку sources, делаем какое то действие на элементt (у элемента, который хотим заморозить) далее нажать F8, переходим во вкладку Elements

# news[5].location_once_scrolled_inro_view # проскрол к элементу

# driver.close() # закрытие вкладки

# Выполнение js скрипта в python
# script_1 = "alert('Robots at work');"
# driver.execute_script(script_1)

################################
# class Test():
#     @classmethod
#     def setup_class(cls):  # выполнится 1 раз перед всеми тестами в классе
#         pass
#     def setup_method(self):  # Выполняется перед каждым тестом
#         pass
#
#     def test_1(self): # выполнение теста
#
#
#     def teardown_method(self): # Выполняется после каждого теста, независимо от успешности setup_method
#         pass
#
#     @classmethod
#     @teardown_class(cls):  # Выполняется 1 раз после всех тестов в классе
#         pass

######################
# @pytest.mark.login
# class TestLoginFromProductPage():
#     @pytest.fixture(scope="function", autouse=True)
#     def setup(self):
#         self.product = ProductFactory(title="Best book created by robot")
#         self.link = self.product.link
#         yield
#         # после этого ключевого слова начинается teardown
#         # выполнится после каждого теста в классе
#         # удаляем те данные, которые мы создали
#         self.product.delete()
#
#     def test_guest_can_go_to_login_page_from_product_page(self, browser):
#         page = ProductPage(browser, self.link)
#         # дальше обычная реализация теста
###############################
# class MainPage(BasePage):  # заглушка
#     def __init__(self, *args, **kwargs):
#         super(MainPage, self).__init__(*args, **kwargs)

###############################

 # task_in = Element(By.CSS_SELECTOR, '[data-qa="row"]:has([title="Входящие"])', 'Входящие задачи')

 ##############################

# Функция для поиска элемента по селектору ID
# def find_element_by_id(driver, id):
#     try:
#         return WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, id))
#         )
#     except TimeoutException:
#         return None

######################

    # Xpath
    # input[value = "150 000.00"]
# [data - qa = "cell"].controls - DecoratorMoney.controls - text - danger
######################


