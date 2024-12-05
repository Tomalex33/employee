from selenium.webdriver.common.by import By


class LoginPageLocators:

    LOGIN_BUTTON_ENTER = (By.CSS_SELECTOR, "[data-qa='auth-AdaptiveLoginForm__checkSignInTypeButton']")  # кнопка ввода логина
    LOGIN_FIELD = (By.CSS_SELECTOR, '.controls-InputBase__nativeField_caretFilled.controls-InputBase__nativeField_caretFilled_theme_default')  # поле ввода логина
    PASSWORD_FIELD = (By.CSS_SELECTOR, '.controls-Password__nativeField_caretFilled_theme_default')  # поле ввода пароля


class ReportPageLocators:

    REPORT_BUTTON = (By.CSS_SELECTOR, "[data-qa='Отчетность']")  # кнопка перехода в отчетность

    PMO_BUTTON = (By.CSS_SELECTOR, "[data-qa='toggleOperationsPanel']")  # кнопка открытия ПМО (Панель массовых операций)
    PMO_BUTTON_CLOSE = (By.CSS_SELECTOR, "[data-qa='controls-OperationsPanel__close']")  # Закрытие ПМО
    CHECK_PMO_BUTTON = (By.CSS_SELECTOR, "[data-qa='controls-CheckboxMarker_state-false']")  # Чек бокс кнопки открытия ПМО
    REMOTE_REPORT_BUTTON = (By.CSS_SELECTOR, "[data-qa='remove'].controls-Toolbar__item_horizontal-spacing_medium")  # Кнопка удаления отчетов в ПМО при веделенных отчетах
    CONFIRM_DIALOG_BUTTON_TRUE = (By.CSS_SELECTOR, "[data-qa='controls-ConfirmationDialog__button-true']")  # Кнопка соглашения диалогового окна, для удаления отчетов

    BASKET_BUTTON = (By.CSS_SELECTOR, "[data-name='FilterViewPanel__additional-editor_deleted']")  # Кнопка перехода в корзину
    BASKET_BUTTON_CLOSE = (By.CSS_SELECTOR, "[data-qa='FilterViewPanel__baseEditor-cross']")  # Выйти из корзины

    ICON_FILTER_ORG = (By.CSS_SELECTOR, '[data-qa="FilterView__icon"]')  # иконка фильтра организаций"
    RESET_ORG_IN_FILTER = (By.CSS_SELECTOR, '[data-qa="FilterViewPanel__baseEditor-cross"]')  # крестик для сброса организации в фильтре
    FILTER_ORG_APPLY = (By.CSS_SELECTOR, '[data-qa="controls-FilterPanelPopup__applyButton"]')  # иконка применения сброшенной организации
    ORG_ALL = (By.CSS_SELECTOR, '.controls-FilterView__text')  # поле "все юр. лица"
    ORG_FIND = (By.CSS_SELECTOR, '[data-qa="controls-Render__field"] input[type="text"].controls-Field')  # поле для ввода названия организации
    ORG_CHOICE = (By.CSS_SELECTOR, '[data-qa="cell"].controls-padding_right-list_')  # выбираем найденную организацию"

    PERIOD_CHOICE = (By.CSS_SELECTOR, '.eoregistry-MainRegister__period')  # выбираем период у отчетов


class RVSLocators:
    CLOSE_REPORT = (By.CSS_SELECTOR, '[data-qa="controls-stack-Button__close"]')  # закрытие отчета
