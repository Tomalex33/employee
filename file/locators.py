from selenium.webdriver.common.by import By


class LoginPageLocators:

    LOGIN_BUTTON_ENTER = (By.CSS_SELECTOR, "[data-qa='auth-AdaptiveLoginForm__checkSignInTypeButton']")  # кнопка ввода логина
    LOGIN_FIELD = (By.CSS_SELECTOR, '.controls-InputBase__nativeField_caretFilled.controls-InputBase__nativeField_caretFilled_theme_default')  # поле ввода логина
    PASSWORD_FIELD = (By.CSS_SELECTOR, '.controls-Password__nativeField_caretFilled_theme_default')  # поле ввода пароля


class ReportPageLocators:

    REPORT_BUTTON = (By.CSS_SELECTOR, "[data-qa='Отчетность']")  # кнопка перехода в отчетность
    PMO_BUTTON = (By.CSS_SELECTOR, "[data-qa='toggleOperationsPanel']")  # кнопка открытия ПМО (Панель массовых операций)
    CHECK_PMO_BUTTON = (By.CSS_SELECTOR, "[data-qa='controls-CheckboxMarker_state-false']")  # Чек бокс кнопки открытия ПМО
    REMOTE_REPORT_BUTTON = (By.CSS_SELECTOR, "[data-qa='remove'].controls-Toolbar__item_horizontal-spacing_medium")  # Кнопка удаления отчетов в ПМО при веделенных отчетах
    CONFIRM_DIALOG_BUTTON_TRUE = (By.CSS_SELECTOR, "[data-qa='controls-ConfirmationDialog__button-true']")  # Кнопка соглашения диалогового окна, для удаления отчетов
    BASKET_BUTTON_DELETE_REPORT = (By.CSS_SELECTOR, "[data-name='FilterViewPanel__additional-editor_deleted']")  # Кнопка перехода в корзину
    PMO_BUTTON_CLOSE = (By.CSS_SELECTOR, "[data-qa='controls-OperationsPanel__close']")  # Закрытие ПМО
    CLOSE_BASKET_BUTTON = (By.CSS_SELECTOR, "[data-qa='FilterViewPanel__baseEditor-cross']")  # Выйти из корзины
    ORG_NAME_FILTER = (By.CSS_SELECTOR, "[name='orgId']")  # Фильтр организаций


