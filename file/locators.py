from selenium.webdriver.common.by import By


class LoginPageLocators:

    LOGIN_BUTTON_ENTER = (By.CSS_SELECTOR, "[data-qa='auth-AdaptiveLoginForm__checkSignInTypeButton']")  # кнопка ввода логина
    LOGIN_FIELD = (By.CSS_SELECTOR, '.controls-InputBase__nativeField_caretFilled.controls-InputBase__nativeField_caretFilled_theme_default')  # поле ввода логина
    PASSWORD_FIELD = (By.CSS_SELECTOR, '.controls-Password__nativeField_caretFilled_theme_default')  # поле ввода пароля
