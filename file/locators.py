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

    PERIOD_CHOICE = (By.CSS_SELECTOR, '.eoregistry-MainRegister__period')  # выбираем период у отчетов, в реестре

    CREATED_REPORT = (By.CSS_SELECTOR, '[data-qa="sabyPage-addButton"]')  # создать отчет
    ALL_LIST_REPORT = (By.CSS_SELECTOR, '.eoregistry-appCreateButton__moreButton')  # весь список отчетов
    PERIOD_REPORT = (By.CSS_SELECTOR, '[data-qa="DateLinkView__template"]')  # выбираем период отчета при создание и всего списка отчетов
    PERIOD_REPORT_4_2022 = (By.CSS_SELECTOR, '.controls-PeriodLiteDialog-item__month [data-date="2022-12-01"]')  # выбираем период отчета при создание и всего списка отчетов 4 кв 2022
    POP_UP = (By.CSS_SELECTOR, '.controls-Popup.controls-DateRangeSelectorLite__picker-normal')  # выбираем период отчета при создание и всего списка отчетов 4 кв 2022

    CLOSE_REPORT = (By.CSS_SELECTOR, '[data-qa="controls-stack-Button__close"]')  # закрытие отчетов (РСВ, ПерсСвед, ЕФС-1)
    SAVE_REPORT = (By.CSS_SELECTOR, '[title="Сохранить"]')  # сохранить отчет

    DISC = (By.CSS_SELECTOR, '[data-qa="structure-counter"] div span')  # количество расхождений в отчетах
    DISC_NOT = (By.CSS_SELECTOR, '[title="Расхождений нет"]')  # нет расхождений в отчете


class RVSLocators:

    SUBSECTION_1 = (By.CSS_SELECTOR, '[data-qa="structure-item"][title="Подраздел 1"][data-state="created"]')  # Раздел 1 подраздел 1"
    RUN_ALL_CALC_RSV_IN_SUBSECTION_1 = (By.CSS_SELECTOR, '[data-qa="runFedAllCalc"]')  # Запуск всех расчетов
    CONFIRM_CALC = (By.CSS_SELECTOR, '[data-qa="controls-ConfirmationDialog__button-true"]')  # Подтверждения запуска всех расчетов
    STRING_51 = (By.CSS_SELECTOR, '[data-name="ЕССС.РасчетСВ.ОбязПлатСВ.РасчСВ_ОПС_ОМС.РасчСВ_ОПС.БазНеПревышОПС.СумВсегоПер"] div div div[data-qa="controls-Render__field"] input')  # строка 51 , всего
    SYM_DISC_TEST3 = (By.XPATH, '//*[contains(text(), "10 530")]')  # поиск элемента по тексту, находим сумму расхождений для test_case_sym3
    RUN_ALL_CALC_RSV_IN_EMPLOYEE_CARD = (By.CSS_SELECTOR, '[data-qa="runAllCalculations"]')  # Запуск всех расчетов из карточки сотрудника
    CONFIRM_CHANGE_EMPLOYEE_CARD = (By.CSS_SELECTOR, '[data-name="form_button_actionYes"]')  # Подтверждения изменений в карточке сотрудника
    STRING_210_1_MONTH = (By.CSS_SELECTOR, '[data-qa="Сотрудники.Сотрудник.СвВыплСВОПС.ВыплСВДоп.ВыплСВДопМТ.НачислСВ"] div div[data-qa="controls-Render__field"] .controls-Field')  # Сумма в строке первого месяца