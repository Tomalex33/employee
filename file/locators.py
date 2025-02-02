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
    ORG_ALL_FILTER = (By.CSS_SELECTOR, '[title="Все юрлица"]')  # выбрать все юр. лица в фильтре

    PERIOD_CHOICE = (By.CSS_SELECTOR, '.eoregistry-MainRegister__period')  # выбираем период у отчетов, в реестре

    CREATED_REPORT = (By.CSS_SELECTOR, '[data-qa="sabyPage-addButton"]')  # создать отчет
    ALL_LIST_REPORT = (By.CSS_SELECTOR, '.eoregistry-appCreateButton__moreButton')  # весь список отчетов
    PERIOD_REPORT = (By.CSS_SELECTOR, '[data-qa="DateLinkView__template"]')  # выбираем период отчета при создание и всего списка отчетов
    PERIOD_REPORT_ALL = (By.CSS_SELECTOR, '[data-qa="controls-PeriodLiteDialog-item__month-caption"]')  # находит все года и месяца отчетов, при создание отчета из всего списка
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

    MAIN = (By.CSS_SELECTOR, '[title="Главная"]')  # Главная
    MESSAGE_IN_HEADER_DISC_REPORT = (By.CSS_SELECTOR, '[data-qa="eo-notification_message"]')  # Сообщение в шапке отчета о количестве расхождений
    SECTION_1 = (By.CSS_SELECTOR, '.tw-overflow-ellipsis[title="Раздел 1"]')  # Раздел 1
    TYPE_PAYER = (By.CSS_SELECTOR, '[data-qa="ЕССС.РасчетСВ.ОбязПлатСВ.ТипПлат"]')  # Выбор типа плательщика Раздела 1
    TYPE_PAYER_1 = (By.CSS_SELECTOR, '[title="1 - Выплаты физ. лицам осуществлялись"]')  # Выплаты физ. лицам осуществлялись
    TYPE_PAYER_2 = (By.CSS_SELECTOR, '[title="2 - Выплаты физ. лицам не осуществлялись"]')  # Выплаты физ. лицам не осуществлялись
    CHECK_TEXT_TYPE_PAYER_1 = (By.CSS_SELECTOR, '[data-name="ЕССС.РасчетСВ.ОбязПлатСВ.ТипПлат"] div div .controls-ComboBox__contentTemplate')  # Проверка выбора текста типа плательщики
    SUBSECTION_1 = (By.CSS_SELECTOR, '[data-qa="structure-item"][title="Подраздел 1"][data-state="created"]')  # Раздел 1 подраздел 1"
    RUN_ALL_CALC_RSV_IN_SUBSECTION_1 = (By.CSS_SELECTOR, '[data-qa="runFedAllCalc"]')  # Запуск всех расчетов
    CONFIRM_CALC = (By.CSS_SELECTOR, '[data-qa="controls-ConfirmationDialog__button-true"]')  # Подтверждения запуска всех расчетов
    STRING_10_ALL_MONTH = (By.CSS_SELECTOR, '[data-qa="ЕССС.РасчетСВ.ОбязПлатСВ.РасчСВ_ОПС_ОМС.РасчСВ_ОПС.КолСтрахЛицВс.КолВсегоПер"] [data-qa="controls-Render__field"] input')  # Количество застрахованных лиц, всего
    STRING_10_MONTH_1 = (By.CSS_SELECTOR, '[data-qa="ЕССС.РасчетСВ.ОбязПлатСВ.РасчСВ_ОПС_ОМС.РасчСВ_ОПС.КолСтрахЛицВс.Кол1Посл3М"] [data-qa="controls-Render__field"] input')  # Количество застрахованных лиц, 1 месяц
    STRING_10_MONTH_2 = (By.CSS_SELECTOR, '[data-qa="ЕССС.РасчетСВ.ОбязПлатСВ.РасчСВ_ОПС_ОМС.РасчСВ_ОПС.КолСтрахЛицВс.Кол2Посл3М"] [data-qa="controls-Render__field"] input')  # Количество застрахованных лиц, 2 месяц
    STRING_10_MONTH_3 = (By.CSS_SELECTOR, '[data-qa="ЕССС.РасчетСВ.ОбязПлатСВ.РасчСВ_ОПС_ОМС.РасчСВ_ОПС.КолСтрахЛицВс.Кол3Посл3М"] [data-qa="controls-Render__field"] input')  # Количество застрахованных лиц, 3 месяц
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
    STRING_150 = (By.CSS_SELECTOR, '[data-name="Сотрудники.Сотрудник.СвВыплСВОПС.СвВыпл.СвВыплМК.ВыплОПС"] div div input')  # строка 150
    STRING_210_1_MONTH = (By.CSS_SELECTOR, '[data-qa="editing_component-view_render"] [title="10530.05"] [title="10530.05"] .controls-fontsize-m')  # Сумма в строке 210, находит три записи по всем месяцам


class PerSvedLocators:

    ADD_EMPLOYEES = (By.CSS_SELECTOR, '.tw-grow .controls-BaseButton__text')  # Добавления сотрудников в когда список сотрудников пуст.
    BUTTON_ADD_EMPLOYEES_IN_CARD_PERS = (By.CSS_SELECTOR, '[data-qa="staff-Buttons__add"]')  # Кнопка добавления сотрудников в карточке сотрудника
    CONFIRM_CHANGE_EMPLOYEE_CARD_PS = (By.CSS_SELECTOR, '[data-qa="FED2UI__ButtonSuccess"]')  # Подтверждения изменений после добавления сотрудника в ПерсСвед
    SYM_DISC_TEST4 = (By.CSS_SELECTOR, '.controls-DecoratorMoney .controls-text-danger')  # сумма расходления в тестах сумм 4
    MOVE_TO_DISPLAY_HOVER = (By.CSS_SELECTOR, '.controls_Person_theme-default.ws-flex-shrink-0')  # наводим на элемент для появления ховера
    DISC_V_PERSVED_HOVER = (By.XPATH, '//*[contains(text(), "В ПерсСвед")]')  # нажимаем по ховеру в расхождениях на ПерсСвед
    SYMM_CARD_PS = (By.CSS_SELECTOR, '[data-qa="Сотрудники.Сотрудник.СуммаВыпл"] .controls-Field')  # Поле для ввода суммы в карточке сотрудника ПерсСвед
    DISC_NOT_PS = (By.CSS_SELECTOR, '[data-name="np-employee__collationTitle"]')  # Нет расхождений в ПерсСвед
    CLOSE_FILL_ACC_DATA = (By.CSS_SELECTOR, '.controls-CloseButton__close__icon_linkButton')  # закрываем всплывающее окно "Заполнить по данным"