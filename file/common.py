# -*- coding: utf-8 -*-
import os
import time

from atf import *
from atf.api import JsonRpcClient
from atf.ui import *
from controls import *

from file.file_path import FolderPath, FilePath
from file.translate import translate


def get_staff_id(staff_name, client):
    """Поиск ID частного лица по имени"""

    params = {"ДопПоля": [],
              "Фильтр": {"d": ["-2", staff_name],
                         "s": [{"n": "Контрагент", "t": "Строка"},
                               {"n": "СтрокаПоиска", "t": "Строка"}]},
              "Сортировка": None,
              "Навигация": None}

    ids = client.call("Персонал.СписокПерсоналаДляАвтодополнения", **params)['d']
    if ids:
        return ids[0][7]
    return None


class Overlay(Region):
    """Индикаторы и оверлеи"""

    # README!!! Если у вас возникла мысль, сюда что то добавить,
    # необходимо написать Хахину А.К. и согласовать данное действие! Иное невозможно!
    overlay_report_elm = Element('jquery', '.ws-LoadingIndicator__loadingContainer:visible',
                                 "Индикатор загрузки в отчетности")
    indicator_ajax = Element(By.CSS_SELECTOR, "div.ws-browser-ajax-loader:not(.ws-hidden) .ws-loading-indicator",
                             "Индикатор загрузки")
    carry_indicator = Element(By.CSS_SELECTOR, 'div.ws-wait-indicator, .controls-loading-indicator-in',
                              'Индикатор загрузки розницы')

    # Это делаем, для того чтобы спросить если элемент один раз,
    # а не много раз искать элементы, которых может вообще не быть
    class_list = (
        'ws-loading-indicator',
        'controls-AjaxLoader',
        'ws-LoadingIndicator__window',
        'controls-loading-indicator-in',
        # Эти классы пока то отключил, т.к. к ним обращаются напрямую через элементы
        # 'ws-LoadingIndicator__loadingContainer',  # overlay_report_elm
        # 'ws-wait-indicator',  # carry_indicator
    )
    selector = ', '.join(f'.{i}:visible' for i in class_list)  # для того чтобы не проверять is_displayed
    base_overlay = Element('jquery', selector, "Индикатор загрузки")

    def check_indicators(self, wait_time=True):
        """Проверить отсутствие индикаторов загрузки на странице"""

        self.base_overlay.should_not_be(Present, wait_time=wait_time)

    def wait_visible(self, wait_time=None):
        """Ждем отображаения"""

        return wait(lambda: self.base_overlay.is_displayed, wait_time)


class ConfirmDialog(Region):
    """Диалог с кнопками Да/Нет"""

    yes_btn            =    Button(      By.CSS_SELECTOR, "[sbisname='Yes']", "Да")
    no_btn             =    Button(      By.CSS_SELECTOR, "[sbisname='No']", "Нет")
    ok_btn             =    Button(      By.CSS_SELECTOR, "[sbisname='simpleDialogOk']", "Ок")
    cancel_btn         =    Button(      By.CSS_SELECTOR, '[sbisname="Cancel"]', 'Отмена')
    question_txt       =    Text(        By.CSS_SELECTOR, 'h2.ws-smp-header', 'Текст запроса')

    def confirm_dismiss(self, confirm=True, msg=''):
        """Метод обрабатывает всплывающее сообщение о подтверждении действия

        :param confirm True/False Подтвердить/Отказаться от выполняемого действия
        :param msg текст для проверки
        """

        self.yes_btn.should_be(Displayed, msg="Нет диалога подтверждения")
        if msg:
            self.question_txt.should_be(ContainsText(msg), msg="Неверный текст")
        delay(0.5)
        last_text = self.question_txt.text
        self.yes_btn.click() if confirm else self.no_btn.click()
        self.question_txt.should_not_be(ExactText(last_text), msg='Окно диалога на подтверждение не закрылось')


class ControlsSubmitPopup(Region):
    """Диалог с кнопками Да/Нет (иногда есть Отмена). Окно '.controls-SubmitPopup_popup' """

    yes_btn           =    Button(      By.CSS_SELECTOR, '[sbisname="positiveButton"]', "Да")
    no_btn            =    Button(      By.CSS_SELECTOR, "[sbisname='negativeButton']", "Нет")
    ok_btn            =    Button(      By.CSS_SELECTOR, '[name="okButton"]', 'ОК')
    cancel_btn        =    Button(      By.CSS_SELECTOR, '[name="cancelButton"]', 'Отмена')
    question_txt      =    Text(        By.CSS_SELECTOR, '.controls-SubmitPopup__message', 'Текст запроса')
    details_txt       =    Text(        By.CSS_SELECTOR, '.controls-SubmitPopup__details', 'Детализация сообщения')
    popup_panel       =    Element(     By.CSS_SELECTOR, ".controls-SubmitPopup_popup", "Панель диалога")

    def confirm_dismiss(self, confirm=True, msg=''):
        """Метод обрабатывает всплывающее сообщение о подтверждении действия
        :param confirm True/False Подтвердить/Отказаться от выполняемого действия
        :param msg текст для проверки
        """

        self.yes_btn.should_be(Displayed, msg="Нет диалога подтверждения", wait_time=True)
        if msg:
            self.question_txt.should_be(ContainsText(msg), msg="Неверный текст")
        delay(0.5)
        last_text = self.question_txt.text
        self.yes_btn.click() if confirm else self.no_btn.click()
        self.question_txt.should_not_be(ExactText(last_text), msg='Окно диалога на подтверждение не закрылось')

    def check_presence(self, msg='', close_err=True):
        """Проверка наличия окна с ошибкой, используется в Демо при отправке отчетности
        :param msg: если передан текст, то проверит и его
        :param close_err: закрываем окно с ошибкой
        """

        self.details_txt.should_be(Displayed, wait_time=True, msg="Не найдено окно с ошибкой")
        if msg:
            self.details_txt.should_be(ContainsText(msg), msg="Неверный текст ошибки")
        if close_err:
            self.select_ok()

    def check_message(self, message: str, exact: bool = False):
        """Проврека сообщения в всплывающем сообщении
        :param message: Сообщение
        :param exact: True- проверка по точному совпадению, False- по частичному
        """

        condition = ExactText(message) if exact else ContainsText(message)
        self.question_txt.should_be(Displayed, msg="Не найдено высплывающее окно", wait_time=True)
        self.question_txt.should_be(condition, msg=f'Высплывающее окно не содержит текст {message}')

    def select_ok(self):
        """Закрытие всплывашке по кнопке ОК"""

        self.ok_btn.click()
        self.ok_btn.should_be(Hidden)

    def close_dialog_if_open(self, msg: str, wait_time=2.5):
        """
        Закрыть диалог, если открыт

        :param msg: ожидаемое сообщение
        :param wait_time: ожидание
        """

        if wait(lambda: self.popup_panel.is_displayed, wait_time):
            self.check_message(msg)
            self.select_ok()


class ErrorMessage(Region):
    """Окно с ошибкой"""

    # 1ый вид окна с ошибкой
    error_txt           =   Text(       By.CSS_SELECTOR, '.ws-smp-header', "Текст ошибки")
    ok_btn              =   Button(     By.CSS_SELECTOR, '[sbisname="simpleDialogOk"]', "Ок")
    # 2ой вид окна с ошибкой
    error_2_txt         =   Text(       By.CSS_SELECTOR, '.controls-SubmitPopup__message', 'Ошибка')
    error2_full_txt     =   Text(       By.CSS_SELECTOR, '.controls-SubmitPopup__details-centered', "Полный текст ошибки")
    ok_2_btn            =   Button(     By.CSS_SELECTOR, '[sbisname="okButton"]', 'Ok')
    checker_elm         =   Element(    By.CSS_SELECTOR,  '[id="onlineChecker"]', 'Ошибка при загрузке дочерних элементов')
    # Кнопа для ошибки дубля документов
    leave_it_as_is_btn  =  Button(By.CSS_SELECTOR, '[sbisname="negativeButton"]', 'Оставить без изменений')

    class_list = (
        '.ws-smp-header',
        '.controls-SubmitPopup__message',
        '[id="onlineChecker"]',
        '.controls-ConfirmationTemplate__status-danger'
        # '.'+Region.popup_confirmation.styles['danger'].css_class
    )
    selector = ', '.join(f'{i}:visible' for i in class_list)  # для того чтобы не проверять is_displayed
    base_error = Element('jquery', selector, "Ошибка")

    def check_error_absence(self):
        """Проверка отсутствия ошибок"""

        self.base_error.should_not_be(Present, wait_time=0, msg="Найдено окно с ошибкой")

    def check_error_presence(self, msg='', close_error=False):
        """Проверка наличия окна с ошибкой (т.е. что окно должно быть)

        :param msg: если передан текст, то проверит и его.
        :param close_error: закрываем окно с ошибкой
        """

        self.error_txt.should_be(Displayed, wait_time=True, msg="Не найдено окно с ошибкой")
        if msg:
            self.error_txt.should_be(ExactText(msg), msg="Не верный текст ошибки")
        if close_error:
            self.ok_btn.click()
            self.ok_btn.should_be(Hidden)

    def check_altern_error_presence(self, msg='', close_error=False):
        """Проверка наличия окна с ошибкой, альтернативное (т.е. что окно должно быть)

        :param msg: если передан текст, то проверит и его
        :param close_error: закрываем окно с ошибкой
        """

        self.error_2_txt.should_be(Displayed, wait_time=True, msg="Не найдено окно с ошибкой")
        if msg:
            if isinstance(msg, list):
                assert_that(self.error_2_txt.text, is_in(msg), "Неверный текст ошибки")
            else:
                self.error_2_txt.should_be(ExactText(msg), msg="Неверный текст ошибки")
        if close_error:
            self.ok_2_btn.click()
            self.ok_2_btn.should_be(Hidden)


# todo use LongOperations/notifier:View
class ControlInformationPopup(Region):
    """Зеленая панель информирования в правом нижнем углу (выгрузка в Excel, копирование ссылки в буфер и т.п.)
    Проще говоря, панель длительных операций"""

    caption_elm         = Element(          By.CSS_SELECTOR, ".LongOperations-Notifier", 'Панель')
    expand_elm          = Element(          By.CSS_SELECTOR, '.LongOperations-Notifier__header__title_theme-default', 'Развернутая панель')
    close_btn           = Button(           SabyBy.DATA_QA, 'controls-stack-Button__close', 'Закрыть панель операций')
    success_elm         = Element(          By.CSS_SELECTOR, '.controls-Notification__success_theme-default, .controls-Notification__success', 'Зеленый индикатор успеха')
    notification_message = Element(         By.CSS_SELECTOR, '.controls-Notification', "Нотификационное сообщение")
    notification_text   = Text(             By.CSS_SELECTOR, '.controls-Notification__simpleTemplate-message', "Текст нотификационного сообщения")
    download_lnk        = ControlsButton(   By.CSS_SELECTOR, '.LongOperations-Notifier__footer__resultButton', 'Скачать/печать')
    data_vclg           = ControlsTreeGridView(By.CSS_SELECTOR, '.LongOperations-Log [name="content"] .controls-Grid', "Данные в журнале операций")
    header_lnk          = Link(             By.CSS_SELECTOR, '.LongOperations-Notifier__header__title', 'Ссылка заголовок панели')
    open_btn            = Button(           'jquery',        '[templatename="LongOperations/Views/Notifier/View"] .controls-BaseButton__text:contains("Открыть")', 'Открыть')
    abort_btn           = ControlsButton(   By.CSS_SELECTOR, '.LongOperations-Notifier__header__abortButton', "Прервать")

    alert_elm           =   Element(        By.CSS_SELECTOR, '.controls-NotificationPopup__header_caption:not(.controls-LongOperationsPopup__header_caption)', "Алерт по действию")
    footer_elm          =   Element(        By.CSS_SELECTOR, '.LongOperations-Notifier__footer', 'Нижняя часть панели')
    progress_elm        =   Element(        By.CSS_SELECTOR, '.controls-Indicator-Progress__left__percent', "Процент выполнения")
    delete_btn          =   Button(         By.CSS_SELECTOR, ' i.icon-Erase.icon-error', 'Удалить по ховеру')
    cancel_btn          =   Button(         By.XPATH,        '//span[.="Отмена"]',  'Отмена выполняемого действия')

    def check_informer_panel(self, operation, wait_time=True):
        """Проверка информера
        :param operation: название операции
        :param wait_time: время ожидания"""

        self.notification_message.should_be(Displayed, wait_time=wait_time, msg="Информер не отображается")
        self.notification_text.should_be(ContainsText(operation),
                                         msg="Текст информера: {}\nТекст информера должен быть: {}"
                                         .format(self.notification_text.text, operation))

    def check_message(self, message: str):
        """Проверка нотификационного сообщения
        :param message: Текст сообщения
        """

        self.notification_message.should_be(Displayed, ContainsText(message), Hidden, wait_time=True)

    def show_excel_panel(self):
        """Показать панель выгрузки в Excel"""

        script = """require(['Core/SessionStorage'], function(CStorage)
        {a = CStorage.get('autoTestConfig');
        a.hideLongOperationsPanel = false;
        CStorage.set('autoTestConfig', a);});"""

        self.browser.execute_script(script)

    def check_success(self, operation, wait_time=True):
        """Проверяем, что выполненная операция завершена успешно

        :param operation: Название операции (например, Выгрузка в Excel)
        :param wait_time: Время ожидания
        """

        self.caption_elm.should_be(Displayed, ContainsText(operation), wait_time=wait_time,
                                   msg='Не выполнена операция {}'.format(operation))
        self.success_elm.should_be(Displayed, msg='Действие должно завершиться успешно', wait_time=wait_time)

    def open(self):
        """
            Отркыть результат
        """

        self.open_btn.click()

    def check_close(self):
        """Проверка закрытия панели"""

        self.notification_message.should_be(Hidden, wait_time=True, msg="Информер не пропадает")

    def cancel_actions(self):
        """
        Отмена выполняемого действия
        """

        self.cancel_btn.click()

class AddressSelection(Region):
    """Форма выбора адреса"""

    city_inp                =    TextField(   By.CSS_SELECTOR,           '[sbisname="Город"] input', "Город")
    street_inp              =    TextField(   By.CSS_SELECTOR,           '[sbisname="Улица"] input', "Улица")
    flat_inp                =    TextField(   By.CSS_SELECTOR,           '[name="Квартира"] input', "Квартира")
    house_inp               =    TextField(   By.CSS_SELECTOR,           '[name="Дом"] input', "Дом")
    building_inp            =    TextField(   By.CSS_SELECTOR,           '[name="Строение"] input', "Литера")
    housing_inp             =    TextField(   By.CSS_SELECTOR,           '[name="Корпус"] input', "Корпус")
    index_inp               =    TextField(   By.CSS_SELECTOR,           "[sbisname='Индекс'] input", "Индекс")
    expand_lnk              =    Link(        By.CSS_SELECTOR, '.Postal-Russia-Requisite [name="SwitchButton"]', "Дополнительно")
    select_country_btn      =    Button(      By.CSS_SELECTOR, '.Kladr-TitleCountry__country', 'Выбрать страну')
    save_btn                =    Button(      By.CSS_SELECTOR, '[sbisname="ВыбратьКладр"]', "Выбрать")
    region_lnk              =    Link(        By.CSS_SELECTOR, '[data-component="SBIS3.Kladr.RegionChoose"] .Kladr-RegionChoose__region', "Выбрать регион")
    regions_cslst           =    CustomList(  By.CSS_SELECTOR, '.Kladr-Regions__regionLinks.asLink', "Регионы")
    kladr_suggest_tbl       =    Table(       By.CSS_SELECTOR, '.controls-Suggest__picker:not(.ws-hidden) table', 'Автодополнение')
    building_type           =    Sbis3ControlsDropdownList( By.CSS_SELECTOR, '[sbisname="ТипСтр"]', 'Тип строения')

    short_city_inp          =    TextField(          'jquery', '[sbisname="Город"]:visible input', "Город")
    short_street_inp        =    TextField(          'jquery', '[sbisname="Улица"]:visible input', "Улица")
    region_cmbx             =    Sbis3ControlsComboBox(   'jquery', '[name="РегионВыпадающийСписок"]:visible', "Регион")
    apply_btn               =    Button(             'jquery', 'i.icon-done:visible', "Применить")
    suggest_tbl             =    Table(              'jquery', '.controls-Suggest__picker table:visible', "Автодополнение")
    short_house_inp         =    TextField(          'jquery', '[sbisname="Дом"]:visible input', "Дом")
    short_flat_inp          =    TextField(          'jquery', '[sbisname="Квартира"] input', 'Квартира')

    # ПАНЕЛЬ ВЫБОРА СТРАНЫ
    select_country_panel    =    Element(           By.CSS_SELECTOR, '[templatename="Postal/ListCountry/ListCountry"]', 'Панель выбора страны')
    select_country2_panel    =    Element(           By.CSS_SELECTOR, '.controls-Scroll_webkitOverflowScrollingTouch', 'Панель выбора страны')

    search_country_csf      =    Sbis3ControlsSearchForm(By.CSS_SELECTOR, '[sbisname="CountryName"]', 'Поиск страны')
    country_suggest_tbl     =    Table(             By.CSS_SELECTOR, '.ListCountry-picker table', 'Автодополнение при поиске страны')
    overlay = Overlay()

    def fill_address_short_form(self, **kwargs):
        """Заполняет коротку форму Адреса

        :param kwargs: Город, Улица
        """

        log('Заполняем адрес')
        self.short_city_inp.should_be(Displayed, wait_time=True, msg="Не открылась форма добавления адреса")
        delay(1)
        if 'Регион' in kwargs.keys():
            reg = kwargs.get('Регион')
            self.region_cmbx.select(reg)
        if 'Город' in kwargs.keys():
            city = kwargs.get('Город')
            self.short_city_inp.type_in(city)
            self.short_city_inp.should_be(ExactText(city), msg='Город не соответствует введенному', wait_time=3)
        if 'Улица' in kwargs.keys() and self.short_street_inp:
            street = kwargs.get('Улица')
            self.short_street_inp.type_in(street)
            self.short_street_inp.should_be(ExactText(street), msg='Улица не соответствует введенной', wait_time=3)
        delay(0.5)
        self.apply_btn.click()
        self.short_city_inp.should_not_be(Displayed, wait_time=10, msg="Не закрылась форма добавления адреса")

    def fill_address(self, **kwargs):
        """Заполняет форму Адреса

        :param kwargs: Город, Улица, Дом ...
        """

        log('Заполняем адрес')
        self.city_inp.should_be(Displayed, wait_time=True, msg="Не открылась форма добавления адреса")
        delay(1)
        if 'Страна' in kwargs.keys():
            self.select_country_btn.click()
            self.select_country_panel.should_be(Displayed, wait_time=True)
            self.search_country_csf.search(kwargs.get('Страна'))
            self.country_suggest_tbl.wait_for_load()
            delay(1)
            self.country_suggest_tbl.row(contains_text=kwargs.get('Страна'))\
                .click()
            self.select_country_panel.should_be(Hidden, wait_time=True)
        if 'Регион' in kwargs.keys():
            self.region_lnk.click()
            tmp_region = self.regions_cslst.item(contains_text=kwargs.get('Регион'))
            tmp_region.click().should_not_be(Displayed, msg="Не пропала панель с регионами")
        if 'Город' in kwargs.keys():
            city = kwargs.get('Город').split(',')[0]
            self.city_inp.clear()
            self.overlay.check_indicators()
            self.city_inp.type_in(city, clear_txt=False)
            self.kladr_suggest_tbl.wait_for_load()
            self.kladr_suggest_tbl.cell(contains_text2=city).click()
            self.city_inp.should_be(ContainsText(city), msg='Город не соответствует введенному', wait_time=3)
            self.overlay.check_indicators()
        if 'Улица' in kwargs.keys():
            street = kwargs.get('Улица').split(',')[0]
            self.street_inp.type_in(street)
            self.kladr_suggest_tbl.wait_for_load()
            self.kladr_suggest_tbl.cell(contains_text2=street).click()
            self.street_inp.should_be(ContainsText(street), msg='Улица не соответствует введенной', wait_time=3)
            self.overlay.check_indicators()
        if 'Дом' in kwargs.keys():
            house = kwargs.get('Дом')
            self.house_inp.clear()
            self.overlay.check_indicators()
            self.house_inp.type_in(house, clear_txt=False, human=True)
            self.overlay.check_indicators()
            self.house_inp.should_be(ContainsText(house), msg='Дом не соответствует введенному', wait_time=2)
            self.expand_lnk.click()
        if 'Литера' in kwargs.keys():

            building = kwargs.get('Литера')
            self.building_type.select('Литера')
            self.building_inp.type_in(building)
            self.building_inp.should_be(ExactText(building), msg='Литера не соответствует введенной', wait_time=2)
        if 'Корпус' in kwargs.keys():
            housing = kwargs.get('Корпус')
            self.housing_inp.clear()
            self.overlay.check_indicators()
            self.housing_inp.type_in(housing)
            self.housing_inp.should_be(ExactText(housing), msg='Корпус не соответствует введенному', wait_time=2)
        if 'Квартира' in kwargs.keys():
            flat = kwargs.get('Квартира')
            self.flat_inp.clear()
            self.overlay.check_indicators()
            self.flat_inp.type_in(flat, clear_txt=False, human=True)
            self.overlay.check_indicators()
            self.flat_inp.should_be(ExactText(flat), msg='Квартира не соответствует введенной', wait_time=2)
        if 'Индекс' in kwargs.keys():
            index = kwargs.get('Индекс')
            delay(1, 'Прогруз карты и индекса')
            self.index_inp.type_in(index)
            self.index_inp.should_be(ExactText(index), msg='Индекс не соответствует введенному', wait_time=2)
        self.save_btn.should_not_be(CssClass(BasicCss.disabled), msg="Кнопка сохранения должна быть активной!")
        delay(1)
        self.save_btn.click()
        self.city_inp.should_not_be(Displayed, wait_time=10, msg="Не закрылась форма добавления адреса")


class AddresseeChoice(Region):
    """Выбор адресата

    для поиска используем метод класса autocomplete_search, остальные методы смотрим у Sbis3ControlFieldLink
    """

    addressee_flnk     =    Sbis3ControlFieldLink(   By.XPATH,        './/*[@data-component="WS3AddresseeChoice/Contractor/FieldLink/FieldLink" or @data-component="AddresseeChoice/FieldLink/AddresseeChoice"]', "Выбор адресата")
    data_clv           =    CustomList(         By.CSS_SELECTOR, '[sbisname="SuggestPage"] .ws-SwitchableArea__item.ws-enabled:not(.ws-hidden) .controls-ListView__item', "Автодополнение")
    data_tab_clv       =    Sbis3ControlsListView(   By.CSS_SELECTOR, '.profiles-SuggestAddresseChoice .ws-SwitchableArea__item:not(.ws-hidden) [data-component="SBIS3.CONTROLS/ListView"]', "Автодополнение на вкладке")
    addressee_tabs     =    Sbis3ControlTabButtons(  By.CSS_SELECTOR, '.controls-Suggest__picker:not(.ws-hidden) .profiles-SuggestAddresseChoice [data-component="SBIS3.CONTROLS/Tab/Buttons"]', "Контрагенты")
    addressee_cslst    =    CustomList(         By.CSS_SELECTOR, '.controls-Suggest__picker:not(.ws-hidden) [sbisname="SuggestPage"] .controls-TabButton:not(.ws-hidden)', 'Контрагенты')

    def autocomplete_search(self, text, text2=None, tab='Наши клиенты', human=False, clear_txt=True):
        """Поиск в поле связи с автодополнением

        :param text: текст который ищем
        :param text2: текст по которому кликаем в таблицу
        :param tab: название вкладки, на которой ищем (Наши клиенты/Все компании/Сотрудники)
        :param human: посимвольный ввод
        :param clear_txt: очищать поле перед вводом текста или нет
        """

        if text2 is None:
            text2 = text

        human = Env().is_ie() or human

        log('Ищем текст {} на вкладке {}'.format(text2, tab))
        self.addressee_flnk.type_in(text, clear_txt=clear_txt, human=human)
        if tab:
            self.addressee_tabs.select(tab)
        search_item = self.data_clv.item(contains_text=text2)
        search_item.should_be(Displayed, wait_time=True, msg='Не найден текст {} в списке автодополнения'.format(text))
        delay(0.5)
        if Env.is_ie():
            search_item.double_click()
        else:
            search_item.click()
        self.data_clv.should_not_be(Displayed, wait_time=True, msg="Список автодополнения должен закрыться")
        self.addressee_flnk.data_lnk.should_be(Displayed, msg="Не заполнилось поле связи", wait_time=True)
        log('Ввели и выбрали текст {}'.format(text2, '[c]'))

    def autocomplete_search2(self, text, text2=None, tab='Наши клиенты'):
        """Поиск в поле связи с автодополнением (если не работает autocomplete_search)

        :param text: текст который ищем
        :param text2: текст по которому кликаем в таблицу
        :param tab: название вкладки, на которой ищем (Наши клиенты/Все компании/Сотрудники)
        """

        if text2 is None:
            text2 = text

        info('Ищем текст {} на вкладке {}'.format(text2, tab))
        self.addressee_flnk.type_in(text)
        if tab:
            self.addressee_cslst.item(contains_text=tab).click()
        search_item = self.data_tab_clv.item(contains_text=text2)
        search_item.should_be(Displayed, wait_time=True, msg='Не найден текст {} в списке автодополнения'.format(text))
        delay(0.2)
        search_item.click()
        self.data_tab_clv.should_not_be(Displayed, wait_time=True, msg="Список автодополнения должен закрыться")
        self.addressee_flnk.data_lnk.should_be(Displayed, msg="Не заполнилось поле связи", wait_time=True)
        info('Ввели и выбрали текст {}'.format(text2, '[c]'))


class SortingFilesInDialog(Region):
    """Сортировка файлов в окне выбора файлов"""

    name_column_elm    =   Element(     By.CSS_SELECTOR, '[sbisname="Name"]', "Имя")
    size_column_elm    =   Element(     By.CSS_SELECTOR, '[sbisname="Size"]', "Размер")
    date_column_elm    =   Element(    By.CSS_SELECTOR, '[sbisname="Date"]', "Дата")

    sort_down = ".icon-TrendDown"
    sort_up = ".icon-TrendUp"

    def check_start_state(self, links_name):
        """Проверка состояния ссылок сортировки ДО сортировки

        :param: links_name Название ссылки - Имя или Размер
        """

        links = {"Имя": self.name_column_elm,
                 "Размер": self.size_column_elm,
                 "Дата": self.date_column_elm}
        curr_link = links.get(links_name)

        curr_link.should_be(Displayed)
        curr_link.element(self.sort_up).should_not_be(
            Displayed, msg="У ссылки {} не должно быть стрелки вверх!".format(links_name))
        curr_link.element(self.sort_down).should_not_be(
            Displayed, msg="У ссылки {} не должно быть стрелки вниз!".format(links_name))

    def sort_name_up(self):
        """Сортировка имени в алфавитном порядке"""

        with report.step('Установим сортировку в алфавитном порядке в таблице'):
            row = self.name_column_elm
            for _ in range(2):
                if row.element(self.sort_up).is_displayed:
                    break
                if row.element(self.sort_down).is_displayed:
                    row.element(self.sort_down).click()
                else:
                    row.element('.icon-16').click()
            row.element(self.sort_up).should_be(Displayed, msg='Сортировка отработала неверно')


class SelectFilesDialog(Region):
    """Диалог выбора файлов"""

    sort_area          =    SortingFilesInDialog()
    input_file_elm     =    Element(     By.CSS_SELECTOR, 'input[type="file"]', 'Путь к файлу для загрузки')
    folder_cslst       =    CustomList(  By.CSS_SELECTOR, '[sbisname="folderBrowser"] .js-controls-ListView__item', "Папки слева")
    items_container_elm=    Element(     By.CSS_SELECTOR, '.controls-ListView__itemsContainer', "Папки слева")
    grain_crumbs_elm   =    Element(     By.CSS_SELECTOR, '[sbisname="grainCrumbs"]', "Путь к папке/файлу")
    right_arrow_lnk    =    Link(        By.CSS_SELECTOR, '[name="setAddress"] .icon-TFFollow', "Стрелка вправо в адресном пути")
    open_history_lnk   =    Link(        By.CSS_SELECTOR, '[name="openHistory"] .icon-primary', "История в адресной строке")
    history_tbl        =    Table(       By.CSS_SELECTOR, '[sbisname="pathList"] table', "Список выбранных ранее путей")
    overlay_elm        =    Element(     By.CSS_SELECTOR, '.FL-FileChooser__explorer-browser .ws-loading-indicator', "Загрузка")
    overlay_2_elm      =    Element(     By.CSS_SELECTOR,  '.FL-FileChooser__explorer-browser div:not(.ws-hidden).ws-browser-ajax-loader', "Ромашка загрузки")
    arrows_cslst       =    CustomList(  By.CSS_SELECTOR, '.fl-grainCrumbs__icon', "Раскрыть список директорий")
    crumbs_name_cslst  =    CustomList(  By.CSS_SELECTOR, '.fl-grainCrumbs__name', "Названия папок в адресной строке")
    path_on_top_inp    =    TextField(   By.CSS_SELECTOR, '[sbisname="edit"] input', "Путь к директории с файлом")
    files_tbl          =    Table(       By.CSS_SELECTOR, '[data-component="FileLoader/Panel/FileChooser/Browser/File"] [sbisname="fileBrowser"] .controls-DataGridView__table:not(.ws-hidden)', "Список файлов справа")
    files_preview_cslst=    CustomList(  'jquery',        '[sbisname="fileBrowser"] .controls-CompositeView__itemsContainer:visible div.js-controls-ListView__item', "Превью файлов справа")
    empty_elm          =    Element(     By.CSS_SELECTOR, '[data-component="FileLoader/Panel/FileChooser/Browser/File"] .controls-ListView__EmptyData', "Нет файлов")
    search_form        =    Sbis3ControlsSearchForm(   By.CSS_SELECTOR, '[sbisname="fileSearchString"]', "Поиск файла")
    fast_filter_cdl    =    Sbis3ControlsDropdownList( By.CSS_SELECTOR, '[sbisname="fileFilterPanel"] [data-component="SBIS3.CONTROLS/DropdownList"]', "Быстрый фильтр")
    fast_filter_elm    =    Element(     By.CSS_SELECTOR, '[sbisname="fileFilterPanel"] .controls-DropdownList__selectedItem', "Быстрый фильтр")
    fast_filter_cslst  =    CustomList(  By.CSS_SELECTOR, '.controls-DropdownList__item.controls-DropdownList__multiselect', "Список опций")
    select_btn         =    Button(      By.CSS_SELECTOR, '[sbisname="DropdownList_buttonChoose"]', "Отобрать")
    load_btn           =    Button(      By.CSS_SELECTOR, '[sbisname="startLoadButton"] .js-controls-Button__text', "Загрузить")
    overlay_3_elm      =    Element(     By.CSS_SELECTOR, '[sbisname="fileBrowserComponent"] .ws-loadingimg', 'Загрузка')
    panel_elm          =    Element(     By.CSS_SELECTOR, '[templatename="FileLoader/fileChooser:FileChooser"].ws-float-area-show-complete', 'Панель')
    panel_elm_vdom     =    Element(     By.CSS_SELECTOR, '.FileChooserWindow', 'Панель')
    close_panel_btn    =    Button(      By.CSS_SELECTOR, '[sbisname="floatAreaCloseButton"]', 'Закрыть панель загрузки')
    choose_btn         =    Button(      By.CSS_SELECTOR, '.controls-ItemActions [title="Выбрать"]', 'Выбрать папку для загрузки')
    overlay_4_elm      =    Element(     By.CSS_SELECTOR, '[sbisname = "folderBrowserComponent"] .ws-loadingimg', 'Ромашка загрузки в навигации')

    mark_lnk           =    Button(      By.CSS_SELECTOR, '[name="markButton"]', "Отметить")
    popup_menu          =   Sbis3PopupMenu()

    view_mode_btn      =    Button(      By.CSS_SELECTOR, '[sbisname = "switchViewMode"] .js-controls-Button__icon', "Режим отображения файлов")
    separator_elm      =    Element(     By.CSS_SELECTOR, ".FileChooserWindow__separator", "Разделитель")

    next_btn           =    Button(     By.CSS_SELECTOR,  "[name='fileChooserWindow'] [name='PagingNext']", "Вперед")
    prev_btn           =    Button(     By.CSS_SELECTOR,  "[name='fileChooserWindow'] [name='PagingPrev']", "Назад")
    begin_btn          =    Button(     By.CSS_SELECTOR,  "[name='fileChooserWindow'] [name='PagingBegin']", "В начало")

    index_cftb         =    Sbis3ControlsFormattedTextBox(By.CSS_SELECTOR, '[name="index"]', 'Порядковый номер')
    recognition        =    Sbis3ControlCheckBox(By.CSS_SELECTOR, '[name="recognition"]', "Распознавание документов")

    triangle_elm        = ".controls-TreeView__expand"
    opened_triangle_elm = ".controls-TreeView__expand.controls-TreeView__expand__open"

    mark_txt = "Отметить"
    all_item = "Все"
    take_off = "Снять"
    invert = "Инвертировать"
    marked_all = "Отмечено всё"

    def set_initial_state(self):
        """Привести окно выбора файлов к исходному состоянию"""

        log("Приводим окно выбора файлов в исходное состояние")
        # Для сброса выбранного пути и положения папок
        self.browser.execute_script("window.localStorage.removeItem('fileChooserSavedHistory')")
        # Для сброса сортировки и режима отображения
        self.browser.execute_script("window.localStorage.removeItem('fileChooserSavedConfig')")

    def select_path(self, file_path, empty_folder=False, panel_elm=None, wait_time=True, human=False):
        """Выбираем путь в диалоге выбора файла

        :param file_path: путь до папки
        :param empty_folder: если в пути к папке нет файлов
        :param panel_elm: если страница на vdom, передавать туда panel_elm_vdom
        :param wait_time
        :param human
        """

        if self.config.get('DOCKER'):
            file_path_on_node = self.config.get('FILES_PATH')
        else:
            file_path_on_node = FolderPath(file_path).on_node
        log("Путь до папки в select_path 3 %s" % file_path)
        panel_elm = panel_elm if panel_elm else self.panel_elm

        log("Выбираем путь в диалоге выбора файла: %s" % file_path)
        panel_elm.should_be(Displayed, wait_time=wait_time, msg='Не загрузился плагин загрузки файлов')
        self.overlay_elm.should_not_be(Displayed, msg="Не запустился плагин загрузки файлов", wait_time=True)
        self.overlay_2_elm.should_not_be(Present, msg="Не прекратилась крутиться ромашка загрузки", wait_time=True)
        self.arrows_cslst.should_be(Displayed, wait_time=60)
        delay(2)
        self.arrows_cslst.item(1).click()
        self.path_on_top_inp.type_in(Keys.DELETE, False)
        delay(1.5)
        if empty_folder:
            self.path_on_top_inp.type_in(file_path_on_node)
            delay(0.5)
            self.path_on_top_inp.type_in(Keys.ENTER, False)
            self.empty_elm.should_be(Displayed, ExactText("Нет файлов"))
        else:
            self.path_on_top_inp.type_in(file_path, False, human=human)
            delay(0.5)
            self.files_tbl.wait_for_change(action=self.path_on_top_inp.type_in(Keys.ENTER, False))

    def change_path(self, file_path, panel_elm=None, wait_time=True, human=False):
        """Метод для выбора пути в диалоге загрузки файла из общей папки

        :param file_path: путь до папки
        :param panel_elm: пробрасываем в метод select_path панель
        :param wait_time
        :param human
        """

        panel_elm = panel_elm if panel_elm else self.panel_elm
        log("Путь до папки в change_path %s" % file_path)
        if self.config.get('DOCKER'):
            file_path = self.config.get('FILES_PATH')
        else:
            file_path = FolderPath(file_path).on_node
        log("Путь до папки в change_path 2 %s" % file_path)
        self.select_path(file_path, panel_elm=panel_elm, wait_time=wait_time, human=human)

    def load_file(self, file_name):
        """Выбора файла для загрузки по его имени"""

        self.files_tbl.wait_for_load()
        file_elm = self.files_tbl.cell(contains_text=file_name)
        file_elm.scroll_into_view()
        delay(0.5)
        file_elm.click()
        self.overlay_3_elm.should_not_be(Displayed, wait_time=60, msg='Загрузка не закончилась')

    @staticmethod
    def form_file_to_download(folder_path_on_builder, files):
        """Сформировать список файлов для загрузки

        :param folder_path_on_builder: папка для загрузки на билдере
        :param files: файлы
        """

        if len(files) == 0 or not files[0]:
            files_to_download = os.listdir(folder_path_on_builder)
            assert_that(len(files_to_download), not_equal(0),
                        "Папка %s, из которой мы загружаем файлы не должна быть пустой" % folder_path_on_builder)
        else:
            files_to_download = files

        # удаляем из списка файлов папку .svn
        if '.svn' in files_to_download:
            files_to_download.remove('.svn')

        return files_to_download

    def execute_download_js(self, files_record, files_to_download):
        """Загрузить набор файлов

        :param files_to_download - список файлов для загрузки
        :param files_record - recordSet
        """

        files_record = '\n'.join(files_record)
        array = ', '.join(['loadRec%s' % i for i in range(len(files_to_download))])

        request_template = """
                require(['Types/entity'],function(entity){
                    %s
                    var array=[%s];
                    FileChooser = $('.FileChooserWindow').wsControl();
                    FileChooser.startLoadFiles(array)
                });"""
        self.browser.execute_script(request_template % (files_record, array))

    def load_file_js_with_plugin(self, folder, *files, panel_elm=None, check_error=True, wait_time=True):
        """Загрузка файла через js

        Если не передан параметр files - загружаем все файлы из папки folder
        :param folder: папка для загрузки
        :param files: файлы
        :param panel_elm: панель загрузки, нужно передавать другое значение для VDOM
        :param check_error Проверять отсутствие ошибки
        :param wait_time Время ожидания загрузки
        """
        folder_path = FolderPath(folder)
        files_to_download = self.form_file_to_download(folder_path.on_builder, files)

        panel_elm = panel_elm if panel_elm else self.panel_elm
        panel_elm.should_be(Present, wait_time=True)
        files_recordset = []
        for index, file in enumerate(files_to_download):
            file_path = FilePath(folder_path.on_builder, file)
            if self.config.get('DOCKER'):
                result_path = self.config.get('FILES_PATH') + file
            else:
                result_path = file_path.on_node
            log('Путь загрузки на builder: {}, на node: {}'.format(file_path.on_builder, result_path))
            assert os.path.isfile(file_path.on_builder), 'Не найден файл для загрузки - %s' % result_path
            file_size = os.path.getsize(file_path.on_builder)
            files_recordset.append("""
                var loadRec%s = new entity.Record({
                    rawData: {
                        path: '%s',
                        name: '%s',
                        size: '%s',
                        data: false,
                        type: 'file'
                    }
                });""" % (index, result_path.replace('\\', '\\\\'), file, file_size))

        self.execute_download_js(files_recordset, files_to_download)
        log('Загрузили файлы {0} из папки {1}'.format(', '.join(files_to_download), folder))
        if check_error:
            ErrorMessage(self.driver).check_error_absence()
        overlay = Overlay(self.driver)
        overlay.overlay_report_elm.should_be(Hidden, wait_time=60, msg='Файл не загрузился')
        overlay.check_indicators(wait_time=wait_time)

    def load_file_js(self, folder, *files, check_error=True, wait_time=True, check_indicators=True):
        """Загрузка файла без нотификатора

        Если не передан параметр files - загружаем все файлы из папки folder

        :param folder: папка для загрузки
        :param files: файлы
        :param check_error Проверять отсутствие ошибки
        :param wait_time ожидание в сек.
        :param check_indicators: Проверить отсутствие индикатора после загрузки файла
        """

        if self.config.get('DOCKER'):
            self.load_file_js_docker(folder, *files, check_error=check_error, wait_time=wait_time,
                                     check_indicators=check_indicators)
        else:
            folder_path = FolderPath(folder)
            if not self.config.get('SERVER_ADDRESS'):  # для локального запуска, чтобы постоянно не править конфиги
                folder_path.on_builder = os.path.abspath(folder)
            files_to_download = self.form_file_to_download(folder_path.on_builder, files)
            files_paths = ''
            for file in files_to_download:
                file_path = FilePath(folder_path.on_builder, file)
                log('Путь загрузки на builder: {}\nна node: {}'.format(file_path.on_builder, file_path.on_node))
                assert os.path.isfile(file_path.on_builder), 'Не найден файл для загрузки - %s' % file_path.on_node
                if self.config.get('SERVER_ADDRESS'):
                    files_paths = files_paths + file_path.on_node + '\n'
                else:
                    files_paths = files_paths + file_path.on_builder + '\n'
            files_paths = files_paths[:-1]

            self.input_file_elm.should_be(Present, wait_time=True)
            if Env.is_ff():
                # Делаем инпут видимым, так как в FF нельзя взаимодействовать с невидимым элементом
                self.browser.execute_script("arguments[0].classList.remove('ws-hidden');",
                                            self.input_file_elm.webelement())
            self.input_file_elm.type_in(files_paths)
            delay(1)
            log('Загрузили файлы {0} из папки {1}'.format(', '.join(files_to_download), folder))
            if check_error:
                ErrorMessage(self.driver).check_error_absence()
            if check_indicators:
                Overlay(self.driver).check_indicators(wait_time)

    def load_file_js_docker(self, folder, *files, check_error=True, wait_time=True, check_indicators=True):
        """Загрузка файла без нотификатора

        Если не передан параметр files - загружаем все файлы из папки folder

        :param folder: папка для загрузки
        :param files: файлы
        :param check_error Проверять отсутствие ошибки
        :param wait_time ожидание в сек.
        :param check_indicators: Проверить отсутствие индикатора после загрузки файла
        """

        folder_path = os.path.abspath(folder)
        files_to_download = self.form_file_to_download(folder_path, files)
        files_paths = ""
        self.input_file_elm.should_be(Present, wait_time=True)
        if Env.is_ff():
            # Делаем инпут видимым, так как в FF нельзя взаимодействовать с невидимым элементом
            self.browser.execute_script("arguments[0].classList.remove('ws-hidden');",
                                        self.input_file_elm.webelement())

        for file in files_to_download:
            file_path = os.path.abspath(os.path.join(folder, file))
            assert os.path.isfile(file_path), 'Не найден файл для загрузки - %s' % file_path
            files_paths = files_paths + file_path + '\n'

        files_paths = files_paths[:-1]
        self.input_file_elm.upload_file(files_paths)

        log('Загрузили файлы {0} из папки {1}'.format(', '.join(files_to_download), folder))
        if check_error:
            ErrorMessage(self.driver).check_error_absence()
        if check_indicators:
            Overlay(self.driver).check_indicators(wait_time)

    def load_file_selenium(self, *files, check_error=True, wait_time=True, check_indicators=True):
        """Загрузка файла без нотификатора

        Если не передан параметр files - загружаем все файлы из папки folder

        :param files: файлы
        :param check_error Проверять отсутствие ошибки
        :param wait_time ожидание в сек.
        :param check_indicators: Проверить отсутствие индикатора после загрузки файла
        """

        files_paths = ''
        for index, file in enumerate(files):
            files_paths += os.path.abspath(file) + '\n'

        self.input_file_elm.should_be(Present, wait_time=True)
        if Env.is_ff():
            # Делаем инпут видимым, так как в FF нельзя взаимодействовать с невидимым элементом
            self.browser.execute_script("arguments[0].classList.remove('ws-hidden');",
                                        self.input_file_elm.webelement())
        self.input_file_elm.type_in(files_paths.rstrip())
        delay(1)
        log('Загрузили файлы {0}'.format(', '.join(files)))
        if check_error:
            ErrorMessage(self.driver).check_error_absence()
        if check_indicators:
            Overlay(self.driver).check_indicators(wait_time)

    def check_open_panel(self, empty=False):
        """Проверка открытия окна выбора файлов

        :param empty: если не должно быть файлов справа
        """

        self.panel_elm.should_be(Displayed, msg='Не загрузился плагин загрузки файлов', wait_time=True)
        self.overlay_elm.should_not_be(Displayed, wait_time=True)
        self.overlay_2_elm.should_not_be(Displayed, wait_time=True)
        if empty:
            self.empty_elm.should_be(Displayed, ExactText("Нет файлов"))
        else:
            self.files_tbl.wait_for_load()

    def close_panel(self):
        """Закрыть окно выбора файлов"""

        self.close_panel_btn.click()
        self.panel_elm.should_not_be(Displayed)
        delay(1)

    def check_selected_path(self, files_count, crumbs_path=None, input_path=None, wait_time=5):
        """Проверка выбора файла/папки

        :param files_count: количество файлов
        :param crumbs_path: путь из хлебных крошек
        :param input_path: путь из строки поиска
        :param wait_time время ожидания
        """

        self.files_tbl.should_be(RowsNumber(files_count), msg="Неверное количество файлов справа!")
        if crumbs_path:
            self.grain_crumbs_elm.should_be(Displayed, ContainsText(crumbs_path),
                                            msg="Неверный путь через хлебные крошки!", wait_time=wait_time)
        if input_path:
            self.path_on_top_inp.should_be(ExactText(input_path),
                                           msg="Неверный путь в адресной строке!", wait_time=wait_time)

    def select_view_mode(self, mode_list=True):
        """Установка режима отображения файлов

        :param mode_list: режим отображения, список/плитка - True/False
        """
        css_list = "icon-TFList"
        css_tile = "icon-TFPreview"

        if mode_list:
            log("Устанавливаем режим отображения список")
            if self.view_mode_btn.has_css_class(css_list):
                self.view_mode_btn.click()
            self.view_mode_btn.should_be(CssClass(css_tile), msg="Не удалось установить режим 'Список'!")
            self.files_tbl.should_be(Displayed, msg="Не переключились в режим список!")
            self.files_preview_cslst.should_not_be(Displayed)
        else:
            log("Устанавливаем режим отображения плитка")
            if self.view_mode_btn.has_css_class(css_tile):
                self.view_mode_btn.click()
            self.view_mode_btn.should_be(CssClass(css_list), msg="Не удалось установить режим 'Плитка'!")
            self.files_preview_cslst.should_be(Displayed, msg="Не переключились в режим плитка!")
            self.files_tbl.should_not_be(Displayed)

    def get_folder_on_path(self, path):
        """Получить папку слева по пути

        :param path: путь до папки
        :return: folder: элемент 'папка'
        """
        data_id = "MYCOMPUTER|{}".format(path)
        data_id_up = data_id.upper().replace("\\", "/")

        folder = self.items_container_elm.element('xpath', '//div[contains(@data-id, "{}")]'.format(data_id_up))
        return folder

    def check_selected_file(self, start_row, end_row, check=True):
        """Проверка отмеченного файла в режиме Список

        :param check: должен быть отмечен или нет
        :param start_row: первая строка с чек-боксом
        :param end_row: последняя строка с чек-боксом
        """

        css_check = "controls-ListView__item__multiSelected"

        if check:
            for i in range(start_row, end_row + 1):
                self.files_tbl.row(i).should_be(CssClass(css_check),
                                                msg="Файл в строке {} должен быть отмечен!".format(i))
        else:
            for i in range(start_row, end_row + 1):
                self.files_tbl.row(i).should_not_be(CssClass(css_check),
                                                    msg="Файл в строке {} не должен быть отмечен!".format(i))

    def check_selected_file_for_tile_mode(self, start_row, end_row, check=True):
        """Проверка отмеченного файла в режиме Плитка

        :param check: должен быть отмечен или нет
        :param start_row: первая строка с чек-боксом
        :param end_row: последняя строка с чек-боксом
        """

        css_check = "controls-ListView__item__multiSelected"

        if check:
            for i in range(start_row, end_row + 1):
                self.files_preview_cslst.item(i).should_be(CssClass(css_check),
                                                           msg="Файл {} должен быть отмечен!".format(i))
        else:
            for i in range(start_row, end_row + 1):
                self.files_preview_cslst.item(i).should_not_be(CssClass(css_check),
                                                               msg="Файл {} не должен быть отмечен!".format(i))

    def check_sorting_by_file_size(self, files_count, sort_down=True):
        """Проверка сортировки файлов по размеру

        :param files_count: количество файлов
        :param sort_down: сортировка по убыванию/возрастанию
        """

        log("Все размеры файлов переводим в КБ")
        self.files_tbl.wait_for_change(5)
        new_list = []
        for i in range(1, self.files_tbl.rows_number + 1):
            file_size = self.files_tbl.cell(i, 3).text.split()
            only_number = file_size[0]
            float_number = float(only_number.replace(",", "."))
            if file_size[1] == 'МБ':
                log("Для файла в строке {} переводим МБ в КБ".format(i))
                float_number_kb = float_number * 1024
                new_list.append(float_number_kb)
            elif file_size[1] == 'КБ':
                log("Файл в строке {} - в КБ".format(i))
                new_list.append(float_number)
            else:
                raise AssertionError('У файла {} не указан размер!'.format(i))
        assert_that(len(new_list), equal_to(files_count),
                    "Неверное количество файлов после преобразования размера!")
        if sort_down:
            log("Проверяем сортировку по убыванию")
            for i in range(files_count - 1):
                assert_that(new_list[i] >= new_list[i + 1], is_(True),
                            "Файл в строке {0} должен быть больше, чем файл в следующей строке!".format(i + 1))
        else:
            log("Проверяем сортировку по возрастанию")
            for i in range(files_count - 1):
                assert_that(new_list[i] <= new_list[i + 1], is_(True),
                            "Файл в строке {0} должен быть меньше, чем файл в следующей строке!".format(i + 1))

    def check_sorting_by_file_name(self, standard_list):
        """Проверка сортировки файлов по имени

        :param standard_list: список из имен файлов, отсортированный в проводнике
        """

        file_name_locator = ".fileNameText"

        assert_that(self.files_tbl.rows_number, equal_to(len(standard_list)),
                    "Количество файлов в окне выбора файлов и в эталонном списке должно совпадать!")
        for i in range(1, self.files_tbl.rows_number + 1):
            assert_that(self.files_tbl.cell(i, 2).element(file_name_locator).text,
                        equal_to(standard_list[i - 1]),
                        "Неверная сортировка файлов по имени: в строке {} - расхождение с проводником!".format(i))

    @staticmethod
    def get_crumbs_path(folder_path):
        """Получить хлебные крошки для пути

        :param folder_path путь в адресной строке в Окне выбора файлов
        :return: путь из хлебных крошек
        """

        folder_path_list = folder_path.split("\\")
        folder_crumbs = '\n'.join(folder_path_list)

        return folder_crumbs

    def check_start_file_download(self, elm_for_click):
        """Проверяем, что загрузка файла началась
        :param elm_for_click элемент, по которому надо кликнуть,
        чтобы загрузка файла началась
        """

        self.panel_elm.should_be(Displayed)
        elm_for_click.click()
        self.panel_elm.should_not_be(Displayed, msg="Не началась загрузка файла!")
        ErrorMessage(self.driver).check_error_absence()

    def check_file_preview(self, file_number, wait_time=5):
        """Проверка отображения превью у файла в режиме плитка
        :param file_number номер файла
        :param wait_time Время ожидания превью файла
        """

        file_name_locator = ".FileBrowserComponent__Browser__name"

        file_item = self.files_preview_cslst.item(file_number)

        file_name_item = file_item.element(file_name_locator)
        file_item.element('img').should_be(
            Displayed, msg='Не отображается preview у файла "{}"!'.format(file_name_item.text), wait_time=wait_time)

        link = file_item.element('img').get_attribute('src')
        assert_that(link, is_not(None), 'Нет ссылки на картинку внутри preview у файла "{}"!'.
                    format(file_item.element(file_name_item.text)))

    def select_folder_to_download(self, download_path):
        """Выбрать папку для загрузки в нее файлов

        :param folder_path: (str) путь до папки
        """

        folder_name = download_path.split("\\")[-1]
        folder_path = download_path.split('\\{}'.format(folder_name))[0]
        self.select_path(folder_path)
        search_folder = self.files_tbl.row(contains_text2=folder_name)
        search_folder.scroll_into_view()
        delay(0.5, 'Резервный')
        search_folder.mouse_over()
        delay(0.5)
        self.choose_btn.should_be(Displayed, msg='Нет кнопки "Выбрать"').click()


class PrintForm(Region):
    """Проверка печатной формы [templatename="js!SBIS3.CONTROLS/PrintDialogTemplate"]"""

    close_btn       =   Button(     By.CSS_SELECTOR, '.controls-PrintDialog__titlebar .ws-float-close-right, .controls-PrintDialog__titlebar [data-qa="controls-stack-Button__close"],.controls-DialogTemplate [data-qa="controls-stack-Button__close"]', "Закрыть")
    print_btn       =   Button(     By.CSS_SELECTOR, '.controls-PrintDialog__button', "Печать")
    html_elm        =   Element(    By.CSS_SELECTOR, 'html', 'Форма печати')
    error           =   ErrorMessage()

    def verify_print_form(self, wait_time=True):
        """Проверка открытия/закрытия печатной формы

        :param wait_time: Ожидание построения печатной формы, если True, то ждет WAIT_ELEMENT_LOAD
        """

        self.print_btn.should_be(Displayed, msg="Не открылась печатная форма", wait_time=wait_time)
        self.error.check_error_absence()
        frames = self.browser.count_frames
        assert_that(lambda: frames, not_equal(0), "Нет фрейма для отображения печатной формы", and_wait(wait_time))
        self.browser.switch_to_frame(frames-1)
        self.html_elm.should_not_be(Not(Displayed), ExactText(''),
                                    msg='Форма предварительного просмотра пустая', wait_time=True)
        self.browser.switch_to_parent_frame()
        self.error.check_error_absence()
        self.close_btn.click()
        self.print_btn.should_not_be(Displayed, msg="Не закрылась печатная форма", wait_time=True)


class InfoPopup(Region):
    """Всплывающее окно с детализацией валидации .ws-info-box """

    infobox_popup_elm   =   Element(        By.CSS_SELECTOR, '.ws-infobox-content', "Всплывающее окно информации")
    close_btn           =   Button(         By.CSS_SELECTOR, '.ws-infobox-close-button', 'Закрыть')
    infobox_vdom_elm    =   Element(        By.CSS_SELECTOR, '.controls-InfoBox__message', "Всплывающее окно информации")
    close_vdom_btn      =   Button(         By.CSS_SELECTOR, '.controls-InfoBox [data-qa="controls-stack-Button__close"]', 'Закрыть')

    def check_error_absence(self):
        """Проверка отсутсвия ошибки"""

        info('Проверяем отсутствие ошибок')
        self.infobox_vdom_elm.should_not_be(Displayed, msg='Окно ошибки не должно отображаться')

    def check_error_presence(self, msg, close_error=False):
        """Проверка наличия окна с ошибкой (т.е. что окно должно быть)

        :param msg: если передан текст, то проверит и его.
        :param close_error: закрываем окно с ошибкой
        """

        info('Проверяем наличие ошибки')
        self.infobox_vdom_elm.should_be(Displayed, wait_time=True, msg="Не найдено окно с ошибкой")
        if msg:
            self.infobox_vdom_elm.should_be(ExactText(msg), msg="Не верный текст ошибки")
        if close_error:
            self.close_vdom_btn.click()
            self.infobox_vdom_elm.should_be(Hidden)


class InfoPopupVDOM(Region):
    """ В разделах старый класс не подошел """

    infobox_popup_elm = Element(By.CSS_SELECTOR, '.controls-InfoBox', "Всплывающее окно информации")


class SelectOrg(Region):
    """Форма выбора организации в реестрах"""

    panel_section_elm   =   Element(                    By.XPATH, '//div[contains(@templatename, "WS3OurOrganization/ListOurOrganizationsFilialControls/ListOurOrganizationsFilialControls") or contains(@templatename, "OurOrganizationChoice/ListOurOrg/ListOurOrg") or contains(@templatename, "WS3OurOrganization/ListOurOrg/ListOurOrg")][contains(@class, "ws-float-area-show-complete")]', 'Панель выбор организации')
    our_org_ctcv        =   Sbis3ControlsTreeCompositeView(  By.XPATH, '//div[contains(@templatename, "WS3OurOrganization/ListOurOrganizationsFilialControls/ListOurOrganizationsFilialControls") or contains(@templatename, "OurOrganizationChoice/ListOurOrg/ListOurOrg") or contains(@templatename, "WS3OurOrganization/ListOurOrg/ListOurOrg")]//div[@data-component="SBIS3.CONTROLS/Tree/DataGridView"]', 'Наши организации')
    search_cs           =   Sbis3ControlsSearchForm(         By.XPATH, '//div[contains(@templatename, "WS3OurOrganization/ListOurOrganizationsFilialControls/ListOurOrganizationsFilialControls") or contains(@templatename, "OurOrganizationChoice/ListOurOrg/ListOurOrg") or contains(@templatename, "WS3OurOrganization/ListOurOrg/ListOurOrg")]//div[@data-component="SBIS3.CONTROLS/SearchForm"]', 'Поиск организации')
    close_btn           =   Button(                     By.XPATH, '//div[contains(@templatename, "WS3OurOrganization/ListOurOrganizationsFilialControls/ListOurOrganizationsFilialControls") or contains(@templatename, "OurOrganizationChoice/ListOurOrg/ListOurOrg") or contains(@templatename, "WS3OurOrganization/ListOurOrg/ListOurOrg")]//*[@data-qa="controls-stack-Button__close"]', 'Закрыть')

    edit_org_btn        =   Button(                     By.CSS_SELECTOR, '[sbisname="СписокНашихОрганизаций"] i.icon-Edit', 'Редактировать')
    active_filter       =   Sbis3ControlsDropdownList(       By.CSS_SELECTOR, '[name="activeFilter"]', 'Фильтр Действующие/Все')
    filter_our_org_dl   =   Sbis3ControlsDropdownList(       'jquery', '[sbisname="FilterOurOrganisation"]:visible', 'Фильтр по организации')

    overlay = Overlay()

    def change_org_in_fast_filter(self, org_name, drop_down_elm=None, without_space=True, kpp=None):
        """
        Из реестра открываем панель "Выбор организации" и выбираем в ней org_name
        :param org_name: Организация, которую ищем
        :param kpp: КПП организации, указываем, если есть несколько организаций с одним названием,
        отличающиеся только КПП. Поиск будет происходить сначала по org_name, затем в полученной выборке по КПП
        :param drop_down_elm: Элемент Sbis3ControlsDropdownList, из которого выбирается организация. По умолчанию указан
        наиболее используемый
        :return:
        """

        log('Меняем организацию в быстром фильтре', level="[i]")
        if not drop_down_elm:
            drop_down_elm = self.filter_our_org_dl
        drop_down_elm.should_be(Displayed, wait_time=True)
        if drop_down_elm.text != org_name:
            drop_down_elm.open()
            if org_name in drop_down_elm.menu_cslst and not kpp:
                # если организация есть в Sbis3ControlsDropdownList, панель выбора организации открвать не надо
                drop_down_elm.menu_cslst.item(with_text=org_name).click()
            else:
                drop_down_elm.more_btn.click()
                self.select_org_from_our_org_panel(org_name, without_space, kpp=kpp)
            drop_down_elm.should_be(ContainsText(org_name), msg='Огранизация не установилась')

    def change_org_js(self, org_name="", inn="", kpp="", refresh=False, is_active=True, scope_areas='Наши компании'):
        """Установка организации через js

        Можно искать по трем параметрам одновременно (org_name, inn, kpp)

        ВАЖНО! Для работы метода нужно находиться АВТОРИЗОВАННЫМИ НА САЙТЕ, но не на ver.html
        Без параметра refresh ничего не произойдет, значение применится, но только при обновлении страницы

        :param org_name: имя организации
        :param inn: ИНН организации
        :param kpp: КПП организации
        :param refresh: если надо обновить страницу
        :param is_active - bool если действующая организация True, иначе False
        :param scope_areas - Область видимости. Задается для каждого реестра своя(узнать значение можно из интерфейса)
        """

        org_id = self.get_id_org(org_name, inn, kpp, is_active, scope_areas)

        script = 'require(["Core/SessionStorage", "SBIS3.ENGINE/Config/Scope"],' \
                 ' function(CStorage, ConfigScope){{CStorage.set("ИдентификаторНашейОрганизации", "{0}");' \
                 'CStorage.set("IdCOOAcc","{0}");' \
                 'ConfigScope.USER.getConfig().set("ИдентификаторНашейОрганизации","{0}");' \
                 'ConfigScope.USER.getConfig().set("IdCOOAcc", "{0}");}});'.format(org_id)

        self.browser.execute_script(script)
        time.sleep(1)  # по другому почему то не успевает сохраняться
        if refresh:
            self.browser.refresh()

        return org_id

    def get_id_org(self, org_name="", inn="", kpp="", is_active=True, scope_areas='Наши компании'):

        from api.clients.our_organization import OurOrganization
        client = None
        org_ids = {'Все юрлица': -1, 'Наша компания': -2,
                   translate('Наша компания'): -2, translate('Все юрлица'): -1}
        assert org_name or inn or kpp, 'Должен быть задан хоть один один параметр для поиска'

        if org_name in org_ids.keys():
            org_id = org_ids[org_name]
        else:
            client = JsonRpcClient(url=self.browser.current_url, sid=self.browser.get_sid())
            org_id = OurOrganization(client).find_org_id(org_name=org_name, inn=inn, kpp=kpp,
                is_active=is_active, scope_areas=scope_areas)

        return org_id

    def change_org_new_js(self, org_name="", inn="", kpp="", is_active=True, scope_areas='Наши компании',
                          org_id=None):
        """Установка организации через js с обновлением реестра без перезагрузки страницы
        :param org_name: имя организации
        :param inn: ИНН организации
        :param kpp: КПП организации
        :param org_id: Напрямую передаём org_id
        """

        if org_id is None:
            org_id = self.get_id_org(org_name, inn, kpp, is_active, scope_areas)
        script = "require(['WS3OurOrganization/OurCompanyComponents/CurrentOurOrganization/CurrentOurOrganization']," \
                 " function(ORG) {{ORG.setMainParam('{0}');" \
                 " ORG.setAccountParam('{0}');" \
                 " ORG.setDistributionParam('{0}');}});".format(str(org_id))
        self.browser.execute_script(script)

        return org_id

    def select_org_from_our_org_panel(self, org_name, without_space=True, open_org_card=False, kpp=None):
        """Выбираем организацию в открытой панели Выберите организацию
        :param org_name - название орг-ции, которую хотим выбрать
        :param kpp: КПП организации
        """

        log('Выбираем организацию {} в открытой панели "Выбор организации"'.format(org_name), level="[i]")
        if not without_space:
            org_name += ' '

        self.panel_section_elm.should_be(Displayed, wait_time=True)
        self.our_org_ctcv.check_load()
        action = lambda: self.search_cs.search(org_name, True)
        self.our_org_ctcv.check_change(action=action)
        self.our_org_ctcv.should_be(ContainsText(org_name), wait_time=True, msg='Не найден организация %s' % org_name)

        search_string = org_name if not kpp else kpp

        if not open_org_card:
            self.our_org_ctcv.cell(contains_text=search_string).click()
            self.popup_confirmation.check_error_absence()
            self.panel_section_elm.should_not_be(Displayed, wait_time=True)
        else:
            self.our_org_ctcv.row(contains_text=search_string).mouse_over()
            self.edit_org_btn.should_be(Displayed, msg="Не отображается кнопка редактирования")
            self.edit_org_btn.click()


@parent_element('[templatename="OurOrganizationChoice/ListOurOrg/ListOurOrg"].ws-float-area-show-complete, [templatename="WS3OurOrganization/ListOurOrg/ListOurOrg"].ws-float-area-show-complete')
class ContragentsListOurOrg(StackTemplate):
    """Форма для выбора организации [templatename="(WS3)OurOrganizationChoice/ListOurOrg/ListOurOrg"] """

    panel_elm                   =   Element(                    By.CSS_SELECTOR, '[templatename="OurOrganizationChoice/ListOurOrg/ListOurOrg"], [templatename="WS3OurOrganization/ListOurOrg/ListOurOrg"]', "Панель выбора организации")
    org_tcv                     =   Sbis3ControlsTreeCompositeView(  By.CSS_SELECTOR, '[data-component="SBIS3.CONTROLS/Tree/DataGridView"]', 'Список организаций')
    search_cs                   =   Sbis3ControlsSearchForm(         By.CSS_SELECTOR, '[data-component="SBIS3.CONTROLS/SearchForm"]', 'Поиск организации')
    panel_elm.set_absolute_position()

    def select_org(self, org):
        """ Выбор организации на панели

        :param org: название организации
        """

        log('Выбираем организацию %s из списка' % org)
        self.panel_elm.should_be(Displayed, wait_time=True)
        self.org_tcv.check_load()
        if org not in ['Наша компания', 'Все юрлица']:
            self.search_cs.search(org)
            self.org_tcv.check_load()
        self.org_tcv.should_be(ContainsText(org), wait_time=True, msg='Не найден организация %s' % org)
        self.org_tcv.cell(contains_text=org).click()
        self.org_tcv.should_be(Hidden, wait_time=True)
        self.popup_confirmation.check_error_absence()

    def close(self):
        """Закрыть"""

        self.close_btn.click()
        self.panel_elm.should_not_be(Displayed, wait_time=True)
