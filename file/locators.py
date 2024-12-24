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
    LEFT_YEARS = (By.CSS_SELECTOR, '[data-qa="controls-PeriodLiteDialog__arrowUp"]')  # листаем год влево, на уменьшение
    RIGHT_YEARS = (By.CSS_SELECTOR, '[data-qa="controls-PeriodLiteDialog__arrowDown"]')  # листаем год вправо, на увеличение
    CURRENT_YEARS = (By.CSS_SELECTOR, '[data-qa="controls-PeriodLiteDialog__year"]')  # текущий год в выпадающем списке дат
    REPORT_FIND = (By.CSS_SELECTOR, '[data-qa="controls-Render__field"] input')  # поле для ввода названия отчета в списке всех отчетов
    CHOICE_FIND_REPORT = (By.CSS_SELECTOR, '.controls-Highlight_highlight')  # выбор найденного отчета

    CLOSE_REPORT = (By.CSS_SELECTOR, '[data-qa="controls-stack-Button__close"]')  # закрытие отчетов (РСВ, ПерсСвед, ЕФС-1)
    SAVE_REPORT = (By.CSS_SELECTOR, '[title="Сохранить"]')  # сохранить отчет
    REPORT_CREATED = (By.CSS_SELECTOR, '[data-qa="report_state_sticker_button"]')  # отчет создан

    DISC = (By.CSS_SELECTOR, '[data-qa="structure-counter"] div span')  # количество расхождений в отчетах
    DISC_NOT = (By.CSS_SELECTOR, '[title="Расхождений нет"]')  # нет расхождений в отчете
    DISC_SECTION = (By.CSS_SELECTOR, '[title="Расхождения"]')  # переход в раздел Расхождений
    DISC_NAME_CONTENT = (By.CSS_SELECTOR, '.controls-text-secondary')  # все расхождения по названию
    VALUE_DISC_SUMM = (By.CSS_SELECTOR, '.controls_text-style_default.controls-text-danger')  # значения сумм по расхождению "01 - НР, ВЖНР, ВПНР - Расхождения между разделом 3 и подразделом 1"


class RVSLocators:

    MAIN = (By.CSS_SELECTOR, '[title="Главная"]')  # Главная"
    SECTION_1 = (By.CSS_SELECTOR, '.tw-overflow-ellipsis[title="Раздел 1"]')  # Раздел 1
    TYPE_PAYER = (By.CSS_SELECTOR, '[data-qa="ЕССС.РасчетСВ.ОбязПлатСВ.ТипПлат"]')  # Выбор типа плательщика Раздела 1
    TYPE_PAYER_1 = (By.CSS_SELECTOR, '[title="1 - Выплаты физ. лицам осуществлялись"]')  # Выплаты физ. лицам осуществлялись
    TYPE_PAYER_2 = (By.CSS_SELECTOR, '[title="2 - Выплаты физ. лицам не осуществлялись"]')  # Выплаты физ. лицам не осуществлялись
    CHECK_TEXT_TYPE_PAYER_1 = (By.CSS_SELECTOR, '[data-name="ЕССС.РасчетСВ.ОбязПлатСВ.ТипПлат"] div div .controls-ComboBox__contentTemplate')  # Проверка выбора текста типа плательщики
    SUBSECTION_1 = (By.CSS_SELECTOR, '[data-qa="structure-item"][title="Подраздел 1"][data-state="created"]')  # Раздел 1 подраздел 1"
    RUN_ALL_CALC_RSV_IN_SUBSECTION_1 = (By.CSS_SELECTOR, '[data-qa="runFedAllCalc"]')  # Запуск всех расчетов
    CONFIRM_CALC = (By.CSS_SELECTOR, '[data-qa="controls-ConfirmationDialog__button-true"]')  # Подтверждения запуска всех расчетов
    STRING_51 = (By.CSS_SELECTOR, '[data-name="ЕССС.РасчетСВ.ОбязПлатСВ.РасчСВ_ОПС_ОМС.РасчСВ_ОПС.БазНеПревышОПС.СумВсегоПер"] div div div[data-qa="controls-Render__field"] input')  # строка 51 , всего
    SYM_DISC_TEST3 = (By.XPATH, '//*[contains(text(), "10 530")]')  # поиск элемента по тексту, находим сумму расхождений для test_case_sym3
    RUN_ALL_CALC_RSV_IN_EMPLOYEE_CARD = (By.CSS_SELECTOR, '[data-qa="runAllCalculations"]')  # Запуск всех расчетов из карточки сотрудника
    SECTION_3 = (By.CSS_SELECTOR, '[item-key="Сотрудники"] div')  # Раздел 3
    ADD_EMPLOYEES_SECTION_3 = (By.XPATH, '//*[contains(text(), "Добавьте")]')  # Кнопка добавления сотрудников в Разделе 3, когда список сотрудников пуст.
    BUTTON_ADD_EMPLOYEES_IN_CARD = (By.CSS_SELECTOR, '[data-qa="staff-Buttons__add"]')  # Кнопка добавления сотрудников в карточке сотрудника
    FIND_EMPLOYEE = (By.CSS_SELECTOR, '.controls-Field-focused-item.controls-Search__nativeField_caretEmpty') # Поле поиска сотрудника
    CHOICE_FIND_EMPLOYEE = (By.CSS_SELECTOR, '.person-BaseInfo__highlightContainer_Stub')  # Выбор найденного сотрудника
    CONFIRM_CHANGE_EMPLOYEE_CARD = (By.CSS_SELECTOR, '[data-name="form_button_actionYes"]')  # Подтверждения изменений в карточке сотрудника
    CONFIRM_CHANGE_STRING_MONTH = (By.CSS_SELECTOR, '[data-qa="controls-itemActions__action controls-default-editing-apply-action"]')  # Подтверждения изменений в строке месяца после изменения
    ADD_MONTH_EMPLOYEE_CARD = (By.CSS_SELECTOR, '[data-name="form_Employee_AddButtonSum"]')  # Добавление месяцев по основному тарифу
    ADD_MONTH_EMPLOYEE_CARD_DOP = (By.CSS_SELECTOR, '[data-name="form_Employee_AddButtonOtherSum"]')  # Добавление месяцев по доп тарифу
    CHOICE_MONTH_EMPLOYEE_CARD = (By.CSS_SELECTOR, '[data-qa="Сотрудники.Сотрудник.СвВыплСВОПС.СвВыпл.СвВыплМК.Месяц"]')  # Выбор месяца в карточке сотрудника
    CHOICE_MONTH_EMPLOYEE_CARD_NOV = (By.CSS_SELECTOR, '[title="Ноябрь"]')  # Выбор февраля в карточке сотрудника
    CHOICE_MONTH_EMPLOYEE_CARD_DEC = (By.CSS_SELECTOR, '[title="Декабрь"]')  # Выбор марта в карточке сотрудника
    STRING_140 = (By.CSS_SELECTOR, '[data-name="Сотрудники.Сотрудник.СвВыплСВОПС.СвВыпл.СвВыплМК.СумВыпл"] div div input')  # строка 140
    STRING_140_EXP = (By.CSS_SELECTOR, '[title="0"] .controls-fontsize-m.controls_text-style_default.controls-text-default.controls-fontweight-default')  # все нули в месяцах карточки сотрудника
    STRING_140_EXP1 = (By.CSS_SELECTOR, '[data-qa="Сотрудники.Сотрудник.СвВыплСВОПС.СвВыпл.СвВыплМК.СумВыпл"] [type="text"].controls-Field.js-controls-Field.controls-Field-focused-item.controls-InputBase__nativeField.controls-InputBase__nativeField_caretFilled.controls-InputBase__nativeField_caretFilled_theme_default.controls-InputBase__nativeField_hideCustomPlaceholder')  # строка 140
    STRING_210_1_MONTH = (By.CSS_SELECTOR, '[data-qa="Сотрудники.Сотрудник.СвВыплСВОПС.ВыплСВДоп.ВыплСВДопМТ.НачислСВ"] div div[data-qa="controls-Render__field"] .controls-Field')  # Сумма в строке первого месяца