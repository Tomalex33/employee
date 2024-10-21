from selenium import webdriver
from time import sleep
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

sbis_site = 'https://sbis.ru/'
sbis_site_about = 'https://tensor.ru/about'

driver = webdriver.Chrome()
sleep(1)

try:
    driver.maximize_window()
    driver.get(sbis_site)
    sleep(2)
    contacts = driver.find_element(By.CSS_SELECTOR, '.sbisru-Header__menu-item-1')
    contacts.click()
    sleep(2)
    banner = driver.find_element(By.CSS_SELECTOR, '.sbisru-Contacts__logo-tensor.mb-12')
    banner.click()
    sleep(3)
    driver.switch_to.window(driver.window_handles[1])
    sleep(2)
    power_of_people = driver.find_element(By.CSS_SELECTOR, '.tensor_ru-Index__block4-content.tensor_ru-Index__card')
    power_of_people.location_once_scrolled_into_view
    sleep(1)
    s = power_of_people.text[:12]
    assert s == 'Сила в людях'
    assert power_of_people.is_displayed()
    sleep(2)
    more_details = driver.find_element(By.CSS_SELECTOR, '[href="/about"].tensor_ru-Header__menu-link')
    more_details.click()
    assert driver.current_url == sbis_site_about
    print("Проверка прошла")
    sleep(2)
finally:
    driver.quit()

# login = driver.find_element(By.CSS_SELECTOR, '.controls-InputBase__nativeField_caretFilled.controls-InputBase__nativeField_caretFilled_theme_default')
#         login.send_keys('сверк', Keys.ENTER)