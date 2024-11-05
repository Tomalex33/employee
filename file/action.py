# -*- coding: utf-8 -*-

import json
import os
import time
from urllib import parse

from atf import *
from atf.api import JsonRpcClient
from atf.ui import *
from controls import *

from file.file_path import FolderPath, FilePath
from file.common import ErrorMessage, SelectFilesDialog


class FileResultWindowNoStack(Region):
    """Панель с результатами загрузки файлов (не стек панель)"""

    loaded_elm          = Element(By.CSS_SELECTOR, '[sbisname*="Loaded"]', "Загруженные отчеты")
    unloaded_title_elm  = Element(By.CSS_SELECTOR, '[sbisname="UnloadedFiles"] .UnloadedFiles__Title', "Заголовок для ошибок")
    unloaded_tcv        = Sbis3ControlsTreeCompositeView(By.CSS_SELECTOR, '[sbisname="UnloadedFiles"] [sbisname="UnloadedFilesBrowser"]', "Ошибки")
    unallocated_elm     = Element(By.CSS_SELECTOR, '[sbisname="UnallocatedFiles"]', "Что делать с файлом?")

    def check_all_loading_unsuccessful(self, error_count_summ, *error_folder_name):
        """
        Проверка, что все файлы не загрузились
        :param error_count_summ общее количество файлов, которые не загрузились
        :param error_folder_name список из название папок с ошибками (вместе с количеством ошибок)
        """
        self.unloaded_title_elm.should_be(Displayed, ExactText("Ошибки {}".format(error_count_summ)), wait_time=True)
        self.unloaded_tcv.should_be(RowsNumber(len(error_folder_name)))
        for item in error_folder_name:
            self.unloaded_tcv.row(contains_text=item).should_be(Displayed)
            error_folder = self.unloaded_tcv.row(contains_text=item)
            assert_that(error_folder.count_elements, equal_to(1),
                        "Папка с ошибкой {} должна быть только одна!".format(item))
        self.loaded_elm.should_not_be(Displayed)
        self.unallocated_elm.should_not_be(Displayed)

    def check_unloaded_reports(self, error_count_summ, error_name, *file_name):
        """
        Проверка отчетов, загруженных с ошибками
        :param error_count_summ общее количество ошибок
        :param error_name название папки с ошибкой (вместе с количеством ошибок)
        :param file_name список из названий файлов
        :return:
        """

        self.unloaded_title_elm.should_be(Displayed, ExactText("Ошибки {}".format(error_count_summ)))
        self.unloaded_tcv.row(contains_text=error_name).should_be(Displayed)
        error_folder = self.unloaded_tcv.row(contains_text=error_name)
        assert_that(error_folder.count_elements, equal_to(1),
                    "Папка с ошибкой {} должна быть только одна!".format(error_name))

        log("Разворачиваем папку с ошибкой")
        self.unloaded_tcv.row(contains_text=file_name[0]).should_not_be(Displayed)
        action = error_folder.click
        self.unloaded_tcv.check_change(action, 1)
        for item in file_name:
            self.unloaded_tcv.row(contains_text=item).should_be(Displayed)


@panel_name("Результаты загрузки файлов")
@templatename('FileResult/Panel/FileResult')
class FileResultWindow(StackTemplate):
    """Панель с результатами загрузки файлов"""

    loaded_elm             =       Element(    By.CSS_SELECTOR, '[sbisname*="Loaded"]', "Загруженные отчеты")
    loaded_text_block      =       CustomList( 'jquery',        '[sbisname*="Loaded"] .LoadedFiles__Title__TextBlock', "Заголовок загруженных файлов по блокам")
    loaded_doc_names_cslst =       CustomList( By.CSS_SELECTOR, '[sbisname*="Loaded"] .documentName', "Названия загруженных документов")
    loaded_org_names_cslst = CustomList(By.CSS_SELECTOR, '.contragentName', 'Названия компаний, для которых загружены документы')

    loaded_title_elm    =       Element(    'jquery',        '[sbisname*="Loaded"] .LoadedFiles__Title:contains("Отчеты") .LoadedFiles__Title__Text', "Заголовок для загруженных отчетов")
    loaded_count_elm    =       Element(    'jquery',        '[sbisname*="Loaded"] .LoadedFiles__Title__Counter', "Счетчик загруженных отчетов")
    loaded_tcv          =       Table(      'jquery',        '[sbisname*="Loaded"] .LoadedFiles__Title:contains("Отчеты")+.controls-Browser table', "Загруженные отчеты")
    loaded_cslst        =       CustomList( By.CSS_SELECTOR, '[sbisname*="Loaded"] .js-controls-ListView__item', "Загруженные отчеты")
    updated_sick_tbl    =       Table(      'jquery',        '[sbisname*="Loaded"] .LoadedFiles__Title:contains("Обновлённые больничные")+.controls-Browser table', "Обновленные больничные")

    unloaded_elm             =       Element(       By.CSS_SELECTOR, '[sbisname="UnloadedFiles"]', "Ошибки")
    unloaded_title_elm       =       Element(       By.CSS_SELECTOR, '[sbisname="UnloadedFiles"] .UnloadedFiles__Title', "Заголовок для ошибок")
    unloaded_doc_names_cslst =       CustomList(    By.CSS_SELECTOR, '[sbisname="UnloadedFiles"] .UnloadedFileRow', "Полные тексты ошибок")
    unloaded_tcv             =       Sbis3ControlsTreeCompositeView(      By.CSS_SELECTOR, '[sbisname="UnloadedFiles"] [sbisname="UnloadedFilesBrowser"]', "Ошибки")
    unloaded_count_elm       =       Element(       By.CSS_SELECTOR, '.UnloadedFiles__Title span', 'Счетчик незагруженных отчетов')

    unallocated_elm     =       Element(     By.CSS_SELECTOR, '[sbisname="UnallocatedFiles"]', "Что делать с файлом?")
    report_list_tbl     =       Table(       'jquery',        '[sbisname="browserView"] table:visible', 'Загруженный отчет')
    more_btn            =       Button(      By.CSS_SELECTOR, '[name="loadMoreButton"]', 'Еще')

    #Для массовой отправки отчетов
    select_all_cb       =       Checkbox(                       By.CSS_SELECTOR, '[sbisname="CheckBox-0"]', 'Чекбокс для выделения всего')
    to_send_btn         =       Button(                         By.CSS_SELECTOR, '[sbisname="SendReportsButton"]', 'К отправке')
    check_btn = Button(By.CSS_SELECTOR, '[sbisname="CheckoutReportsButton"]', 'Проверить')

    file_name           =       Element(                        By.CSS_SELECTOR,  '.docview-CommandPanel__Name', 'Файл')
    preview_elm         =       Element(                        By.CSS_SELECTOR,  '.docview-iFrame:not(.docview-notLoadedYet)', 'Отображение вложения')
    tables = CustomList(By.CSS_SELECTOR, '[name="browserView"]', 'Загруженные документы')
    files_titles = CustomList(By.CLASS_NAME, 'LoadedFiles__Title__Text', 'Тип загруженных документов')
    files_counters = CustomList(By.CLASS_NAME, 'LoadedFiles__Title__Counter', 'Счетчик загруженных документов')
    # тут все списками, т.к. может быть несколько разных типов

    create_doc_button = ControlsDropdownButton(By.CSS_SELECTOR, '.UnallocatedFiles__CreateDocButton', 'Создать')

    def check_file_result(self, *args, counter=None, files_type=None, types_number=1):
        """Проверяем таблицу загруженных документов
        :param args: Какой текст должен быть в таблице
        :param counter: если проверяем счетчик
        :param files_type: если проверяем название типа загруженных документов
        :param types_number: с каким типом по порядку работаем, т.к. их может быть несколько"""

        docs_table = self.tables.item(types_number, element_type=Sbis3ControlsTreeCompositeView)
        title_elm, counter_elm = self.files_titles.item(types_number), self.files_counters.item(types_number)

        self.check_open()
        for value in args:
            docs_table.should_be(ContainsText(value), msg=f'В таблице загруженных документов должен быть текст {value}')
        if counter:
            counter_elm.should_be(ExactText(str(counter)), msg='Неверно указан счетчик документов')
            docs_table.should_be(RowsNumber(int(counter)), msg=f'В таблице должно быть {counter} документов')
        if files_type:
            title_elm.should_be(ExactText(files_type), msg='Неверно указан тип документов')
        docs_table.check_load()

    def click_in_row(self, row):
        """Кликаем на нужную строку в списке
        :param row: строка - номер или по содержаниюя текста
        """
        if isinstance(row, int):
            self.loaded_cslst.item(item_number=row).click()
        else:
            self.loaded_cslst.item(contains_text=row).click()

    def check_file_name(self, file_name):
        """Проверить название загруженного файла
        :param file_name название файла
        """
        self.check_open()
        self.file_name.should_be(ContainsText(file_name))

    def check_unloaded_files_count(self, unloaded_count: str):
        """
        Проверить количество незагруженных файлов
        :param unloaded_count: ожидаемое количество
        """

        self.unloaded_tcv.row(contains_text='не более 99 файлов'). \
            element('.UnloadedFileErrorCount').should_be(ContainsText(unloaded_count))

    def check_preview(self):
        """Проверка отображения превью"""
        self.preview_elm.should_be(Displayed, wait_time=True)

    def open_downloaded_file(self, file_name=None, opened_is_new_tab=True):
        """Открыть загруженный файл
        :param file_name название файла
        Если передано название файла, то кликаем по нему.
        Если нет, то кликаем по первому файлу
        :param opened_is_new_tab: отчет открывается на соседней вкладке
        """

        self.loaded_tcv.should_be(Displayed)
        if file_name:
            self.loaded_tcv.row(contains_text=file_name).click()
        else:
            self.loaded_tcv.row(1).click()
        if opened_is_new_tab:
            self.browser.should_be(CountWindows(2), msg="Загруженный файл должен открыться в соседней вкладке!")
            self.browser.switch_to_opened_window()

    def check_unloaded_folder(self, error_count_summ, error_name):
        """Проверка ошибки в незагруженных файлах
        :param error_count_summ общее количество ошибок
        :param error_name название папки с ошибкой (вместе с количеством ошибок)
        """

        self.unloaded_title_elm.should_be(Displayed, ExactText("Ошибки {}".format(error_count_summ)),
                                          wait_time=True)
        self.unloaded_tcv.row(contains_text=error_name).should_be(Displayed)
        error_folder = self.unloaded_tcv.row(contains_text=error_name)
        assert_that(error_folder.count_elements, equal_to(1),
                    "Папка с ошибкой {} должна быть только одна!".format(error_name))

    def check_unloaded_reports(self, error_count_summ, error_name, *file_name):
        """
        Проверка отчетов, загруженных с ошибками
        :param error_count_summ общее количество ошибок
        :param error_name название папки с ошибкой (вместе с количеством ошибок)
        :param file_name список из названий файлов
        :return:
        """
        self.check_unloaded_folder(error_count_summ, error_name)

        log("Разворачиваем папку с ошибкой")
        self.unloaded_tcv.row(contains_text=file_name[0]).should_not_be(Displayed)
        action = self.unloaded_tcv.row(contains_text=error_name).click
        self.unloaded_tcv.check_change(action, 1)
        for item in file_name:
            self.unloaded_tcv.row(contains_text=item).should_be(Displayed)

    def check_loaded_reports_count(self, report_count):
        """
        Проверка количества успешно загруженных отчетов
        :param report_count: количество отчетов
        """

        self.loaded_count_elm.should_be(Displayed, ExactText(str(report_count)))
        self.loaded_tcv.should_be(RowsNumber(report_count))

    def check_loaded_reports(self, report_count, *report_info):
        """
        Проверка успешно загруженных отчетов
        :param report_count: количество отчетов
        :param report_info: информация по отчету
        :return:
        """

        self.loaded_title_elm.should_be(Displayed)
        self.check_loaded_reports_count(report_count)

        if len(report_info) != 0:
            for info in report_info:
                self.loaded_tcv.row(contains_text2=info).should_be(Displayed, wait_time=True)

    def check_loaded_orgs(self, report_count, *org_names):
        """
        Проверка организаций, для которых загружены отчеты
        :param report_count: количество отчетов
        :param org_names: названия организаций
        """

        self.check_loaded_reports_count(report_count)
        for name in org_names:
            self.loaded_org_names_cslst.item(contains_text=name).should_be(Displayed)

    def check_all_loading_successful(self, report_count):
        """
        Проверка, что все файлы успешно загрузились
        :param report_count: количество отчетов
        """
        self.check_loaded_reports(report_count)
        self.unloaded_elm.should_not_be(Displayed)
        self.unallocated_elm.should_not_be(Displayed)

    def check_all_loading_unsuccessful(self, error_count_summ, *error_folder_name, wait_time=20):
        """
        Проверка, что все файлы не загрузились
        :param error_count_summ общее количество файлов, которые не загрузились
        :param error_folder_name список из название папок с ошибками (вместе с количеством ошибок)
        :param wait_time ожидание
        """
        self.unloaded_title_elm.should_be(Displayed, ExactText("Ошибки {}".format(error_count_summ)),
                                          wait_time=wait_time)
        self.unloaded_tcv.should_be(RowsNumber(len(error_folder_name)))
        for item in error_folder_name:
            self.unloaded_tcv.row(contains_text=item).should_be(Displayed)
            error_folder = self.unloaded_tcv.row(contains_text=item)
            assert_that(error_folder.count_elements, equal_to(1),
                        "Папка с ошибкой {} должна быть только одна!".format(item))
        self.loaded_elm.should_not_be(Displayed)
        self.unallocated_elm.should_not_be(Displayed)

    def open_from_long_operation_panel(self, wait_time=30, one_file=True):
        """
        Открыть загруженный файл
        :param wait_time: время загрузки файлов
        :param one_file: один или несколько отчетов загружаются
        Если один, то панель с результатами не появится, сразу откроется загруженный отчет
        Если несколько, откроется панель с результатами загрузки
        """
        if one_file:
            self.browser.should_be(CountWindows(2), msg="Отчет должен открыться в соседней вкладке!", wait_time=True)
            self.browser.switch_to_opened_window()
        else:
            self.loaded_elm.should_be(Displayed, msg="Не открылась панель с результатами загрузки!", wait_time=True)

    def check_error_load(self, err_msg, wait_time=20):
        """Проверка текста ошибки"""

        self.unloaded_tcv.should_be(ContainsText(err_msg), wait_time=wait_time)

    def check_error_load_report(self, err_msg):
        """Проверка текста ошибки"""

        assert_that(lambda: self.unloaded_tcv.text, equal_to(err_msg), 'Нет ошибки', and_wait())

    def to_send_downloaded_reports(self, count_reports=False, time=True):
        """
        Нажимаем к Отправке загруженные отчеты
        """
        self.report_list_tbl.should_be(Displayed, wait_time=time)
        if count_reports:
            assert_that(self.report_list_tbl.rows_number, equal_to(count_reports),
                        'Неверное количество загруженных отчетов')
        self.to_send_btn.click()
        ErrorMessage(self.driver).check_error_absence()

    def check_full_error_texts(self, sample_errors: list):
        """
        Сравнение полного текста (с цифрами в конце) ошибок у незагруженных документов
        :param sample_errors: эталонный список из ошибок
        """

        info('Сравним список ошибок в окне загрузки с эталоном')
        for error_name in sample_errors:
            self.unloaded_doc_names_cslst.item(contains_text=error_name).should_be(Displayed,
                                    msg=f"В списке незагруженных документов отсутствует текст ошибки '{error_name}'")

    def check_successful_form_names(self, sample_loaded: set):
        """
        Сравнение с эталонным списком имён формализованных документов (например, названий отчетов) со списком эталонов
        :param sample_loaded: список из названий документов
        """

        info('Сравним список загруженных документов с эталонным')
        for loaded_name in sample_loaded:
            self.loaded_doc_names_cslst.item(contains_text=loaded_name).should_be(Displayed,
                                msg=f"В списке загруженных документов отсутствует название документа '{loaded_name}'")

    def more_btn_click(self, how_many: int):
        """
        Клик по кнопке Еще в окне загрузки
        :param how_many: сколько раз кликнуть. Если передаётся 0 - то считаем, что кнопки быть не должно
        """

        info('Нажать на кнопку Еще для раскрытия полного списка')
        condition = Displayed if how_many else Not(Displayed)
        self.more_btn.should_be(condition, msg=f"Кнопка 'Еще' {'должна' if how_many else 'не должна'} присутствовать")
        for i in range(how_many):
            self.loaded_tcv.wait_for_change(action=self.more_btn.click())

    def open_downloaded_doc_panel(self, doc_name: str):
        """Открыть документ из окна загрузки по имени (только для документов на панели)
        :param doc_name: Название документа
        """

        info(f"Открываем документ с названием '{doc_name}'")
        self.loaded_doc_names_cslst.item(contains_text=doc_name).click()

    def check_counters(self, positive_count: int, negative_count: int):
        """Проверка счетчиков в окне загрузки файлов. Если какой-то проверять не нужно - передать 0
        :param positive_count: загруженные
        :param negative_count: незагруженные
        """

        if positive_count:
            self.loaded_count_elm.should_be(ExactText(str(positive_count)), wait_time=True)
        if negative_count:
            self.unloaded_count_elm.should_be(ExactText(str(negative_count)), wait_time=True)

    def check_load_docs(self, *docs, count=False):
        """
        Проверка загруженых документов
        :param docs: список документов
        :param count: количество
        """
        for doc in docs:
            self.loaded_text_block.item(contains_text=doc).should_be(Displayed)
        if count:
            self.loaded_text_block.should_be(CountElements(count), msg='Разное колличество загружных документов')

    def open_update_sick(self, name):
        """
        Открытие обноаленного больничного
        :param name: имя
        :return:
        """
        self.updated_sick_tbl.item(contains_text=name).click()

    def select_all_reports(self):
        """
        Выделения всех отчетов через чек-бокс
        :return:
        """
        self.select_all_cb.click()

    def select_report(self, *reports_names):
        """Выделить отчеты
        :param reports_names: названия отчетов для выделения
        """
        self.loaded_tcv.item()

        for report in self.loaded_tcv:
            if report.element(".documentName").text in reports_names:
                report.mouse_over()
                report.element(".controls-ListView__itemCheckBox").click()

    def check_loaded_report(self, report_name, report_info, status, signature=True):
        """Проверить загруженный отчет.
        Получение строки с отчетом с помощью регулярного выражения
        :param report_name название отчета
        :param report_info информация по отчету
        :param status статус отчета
        :param signature должен быть значок электронной подписи
        """

        from pages_inside.libraries.ReportingEvents.base import Register
        from pages_inside.business.warehouse.colors_and_icons import Icons

        all_status = Register(self.driver).all_status
        assert_that(all_status.get(status), is_not(None), "Передан неверный статус отчета!")

        row_number = self.loaded_tcv.row(contains_text2=report_name).should_be(Displayed).position
        info(f"Номер строки - {row_number}")
        row_elm = self.loaded_tcv.row(row_number)  # По номеру, потому что contains_text2 дольше отрабатывает

        row_elm.scroll_into_view()
        row_elm.should_be(Displayed, ContainsText(report_info), msg=f"Неверные данные по отчету '{report_name}'")
        if signature:
            row_elm.element(Icons.SIGNATURE).should_be(
                Displayed, msg=f"У отчета '{report_name}' должен быть значок электронной подписи")

        icon, state = all_status.get(status)
        row_elm.element(icon).should_be(Displayed, Attribute(title=state),
                                        msg=f"У отчета {report_name} должен быть статус '{state}'!")

    def check_unloaded_reports_count(self, count, folder_count):
        """Проверить общее количество незагруженных отчетов
        :param count общее количество ошибок
        :param folder_count количество папок с ошибками
        """

        self.unloaded_title_elm.should_be(Displayed, ExactText("Ошибки {}".format(count)))
        self.unloaded_tcv.should_be(Displayed, RowsNumber(folder_count))

    def check_unloaded_report(self, error_name):
        """
        Проверка отчетов, загруженных с ошибками
        :param error_name название папки с ошибкой (вместе с количеством ошибок)
        :return:
        """

        self.unloaded_tcv.row(contains_text=error_name).should_be(Displayed)

    def create_document(self, *regulation):
        """Создать документ из нераспределенного файла
        :param regulation: регламент документа"""

        self.create_doc_button.select(*regulation)


class DownloadReports(Region):
    """Раздел загрузка отчетности"""

    result_panel        =   FileResultWindow()
    files_tbl           =   Table(          By.CSS_SELECTOR, '[sbisname="fileBrowser"] table.controls-DataGridView__table', "Файлы")

    def load_one_report_and_get_id(self, folder_path):
        """Загрузить один отчет и получить его ИД"""

        session, id_report_dict = self.load_file_api(folder_path)
        id_report_list = list(id_report_dict.values())
        assert_that(len(id_report_list), equal_to(1), "Должен быть один загруженный отчет!")
        id_report = id_report_list[0]
        return id_report

    def move_in_fns_and_open_load_menu(self):
        """Перейти в реестр Налоговая и открыть меню загрузки"""

        from pages_inside.eo_controls.report_application import Desktop3 as NewDesktop

        new_register = NewDesktop(self.driver)
        new_register.move_to_section_href("Налоговая")
        new_register.check_load_registry()
        select_files = SelectFilesDialog(self.driver)
        select_files.set_initial_state()
        new_register.load_from()

    def get_file_name(self, folder_path):
        """
        Получить имя файла в папке
        :param folder_path: путь до папки, в которой лежит файл
        :return: список из имен файлов
        """

        folder_path_on = FolderPath(folder_path).on_builder
        select_file = SelectFilesDialog(self.driver)
        files_names = select_file.form_file_to_download(folder_path_on, [])

        return files_names

    @staticmethod
    def formation_files_info_for_upload(site, sid, folder, *files):
        """
        Формирование информации по загружаемым файлам
        для их загрузки
        :param site сайт
        :param sid сессия
        :param folder Папка с файлами для загрузки
        :param files - список файлов для загрузки
        :return: Список из словарей с информацией по каждому загружаемому файлу
        """

        from file.functions import upload_file_to_sbis_disk

        # Формируем список из путей до загружаемых файлов

        folder_path = FolderPath(folder).on_builder  # Путь до папки
        files_to_download = SelectFilesDialog.form_file_to_download(folder_path, files)  # Список файлов в папке

        info("Список файлов для загрузки - {}".format(files_to_download))

        files_paths = list() # Список из путей до файлов в папке
        for item in files_to_download:
            file_path = FilePath(folder, item)
            files_paths.append(file_path.on_builder)

        info("Пути до загружаемых файлов - {}".format(files_paths))

        # Загружаем файлы на СБИС.Диск, чтобы получить uuidf и ver
        files_on_sbisdisk = list() # Список из словарей с информацией по каждому загружаемому файлу
        for file in files_paths:
            file_id, version_id = upload_file_to_sbis_disk(file, site, sid)
            size = os.path.getsize(file)
            file_name = os.path.basename(file)
            files_on_sbisdisk.append({'uuidf': file_id, 'ver': version_id, 'file_name': file_name, 'size': size})

        return files_on_sbisdisk

    def load_file_api(self, folder, wait_time=20, *files):
        """
        Загрузка файлов
        :param wait_time время ожидания загрузки
        :param folder папка с файлами
        :param files файлы для загрузки

        :return: сессия загрузки, список из ИД загруженных файлов
        """

        site = parse.urljoin(self.browser.current_url, '/')
        sid = self.browser.get_sid()

        files_on_sbisdisk = DownloadReports.formation_files_info_for_upload(site, sid, folder, *files)

        log('Загружаются файлы из папки: {}'.format(folder))
        session, id_report_list = DownloadReports(self.driver).uploading_create_files(site, sid, files_on_sbisdisk, wait_time)

        return session, id_report_list

    def load_file_api_in_report(self, id_doc, folder, wait_time=20, refresh=False, *files):
        """
        Загрузка файлов в отчет
        :param id_doc ИД документа (отчета), в который загружаем файлы
        :param folder папка с загружаемыми файлами
        :param wait_time время ожидания загрузки
        :param refresh Обновить страницу
        """

        site = parse.urljoin(self.browser.current_url, '/')
        sid = self.browser.get_sid()

        files_on_sbisdisk = self.formation_files_info_for_upload(site, sid, folder, *files)

        log("Загрузить файлы")
        dw_session, id_reports = self.uploading_create_files(site, sid, files_on_sbisdisk, wait_time, id_doc)

        if refresh:
            self.browser.refresh()

        return dw_session

    def load_file_api_in_report_long(self, id_report, id_doc, folder, wait_time=20, refresh=False,  loader_type='ListOfDocuments', *files):
        """
        Загрузка файлов в отчет с помощью метода Uploading.CreateLong
        :param id_doc ИД документа (отчета), в который загружаем файлы
        :param folder папка с загружаемыми файлами
        :param wait_time время ожидания загрузки
        :param refresh Обновить страницу
        """

        site = parse.urljoin(self.browser.current_url, '/')
        sid = self.browser.get_sid()

        files_on_sbisdisk = self.formation_files_info_for_upload(site, sid, folder, *files)

        log("Загрузить файлы")
        dw_session, id_reports = self.uploading_create_files_long(site, sid, files_on_sbisdisk, wait_time, id_report, id_doc, loader_type=loader_type)

        if refresh:
            self.browser.refresh()

        return dw_session

    @staticmethod
    def uploade_file(site, sid, file_info, wait_time, id_doc=None):
        """Загрузить файл с помощью метода Uploading.Create
        :param site
        :param sid
        :param file_info - информация о файле - список из словарей
        :param wait_time время загрузки файлов
        :param id_doc ИД документа, в который загружаются файлы

        :return сессия загрузки, словарь из ИД загруженных отчетов
        """

        from file.uploading import UploadingAPI

        client_rpc = JsonRpcClient(site, sid)
        api = UploadingAPI(client_rpc)

        dw_session = api.uploading_create(file_info, id_doc=id_doc)
        info("Сессия загрузки - {}".format(dw_session))

        # Ждем окончания загрузки
        resp = None
        status = 4
        end_time = time.time() + wait_time
        while time.time() < end_time:
            delay(2, "Ждем завершения загрузки")
            resp = api.get_result(dw_session)
            if resp['Status'] == status:
                break
        assert_that(resp['Status'], equal_to(status),
                    f"Файл не успел загрузиться за {wait_time} секунд!\nid сессии {dw_session}")

        return dw_session, resp['LoadedFiles']

    @staticmethod
    def uploade_file_long(site, sid, file_info, wait_time, id_report=None, id_doc=None, loader_type='ListOfDocuments'):
        """Загрузить файл с помощью метода Uploading.CreateLong
        :param site
        :param sid
        :param file_info - информация о файле - список из словарей
        :param wait_time время загрузки файлов
        :param id_doc ИД документа, в который загружаются файлы

        :return сессия загрузки, словарь из ИД загруженных отчетов
        """

        from uploading import UploadingAPI

        client_rpc = JsonRpcClient(site, sid)
        api = UploadingAPI(client_rpc)

        dw_session = api.uploading_create_long(file_info, id_report=id_report, id_doc=id_doc, loader_type=loader_type)
        info("Сессия загрузки - {}".format(dw_session))

        # Ждем окончания загрузки
        resp = None
        status = 4
        end_time = time.time() + wait_time
        while time.time() < end_time:
            delay(2, "Ждем завершения загрузки")
            resp = api.get_result(dw_session)
            if resp['Status'] == status:
                break
        assert_that(resp['Status'], equal_to(status),
                    f"Файл не успел загрузиться за {wait_time} секунд!\nid сессии {dw_session}")

        return dw_session, resp['LoadedFiles']

    def uploading_create_files(self, site, sid, file_info, wait_time, id_doc=None):
        """Загрузить файлы с помощью метода Uploading.Create
        :param site
        :param sid
        :param file_info - информация о файле - список из словарей
        :param wait_time время загрузки файлов
        :param id_doc ИД документа, в который загружаются файлы

        :return сессия загрузки, словарь из ИД загруженных отчетов
        """

        dw_session, loaded_files = self.uploade_file(site, sid, file_info, wait_time, id_doc=id_doc)

        info("Получаем словарь из ИД загруженных отчетов")
        id_reports = DownloadReports.get_id_loaded_reports(loaded_files)

        info("Загруженные отчеты: {}".format(id_reports))
        return dw_session, id_reports

    def uploading_create_files_long(self, site, sid, file_info, wait_time, id_report=None, id_doc=None, loader_type='ListOfDocuments'):
        """Загрузить файлы с помощью метода Uploading.Create
        :param site
        :param sid
        :param file_info - информация о файле - список из словарей
        :param wait_time время загрузки файлов
        :param id_doc ИД документа, в который загружаются файлы

        :return сессия загрузки, словарь из ИД загруженных отчетов
        """

        dw_session, loaded_files = self.uploade_file_long(site, sid, file_info, wait_time, id_report=id_report, id_doc=id_doc, loader_type=loader_type)

        info("Получаем словарь из ИД загруженных отчетов")
        id_reports = DownloadReports.get_id_loaded_reports(loaded_files)

        info("Загруженные отчеты: {}".format(id_reports))
        return dw_session, id_reports

    @staticmethod
    def get_id_loaded_reports(loaded_files):
        """
        Получить ИД загруженных отчетов
        :param loaded_files сюда передать значение ключа ['LoadedFiles'],
        который получается из ответа запроса Uploading.GetResult

        :return: словарь из ИД отчетов, например, {'Название файла': ИД отчета}
        ИД отчетов могут повторяться, так как несколько файлов могут загружаться
        в один комплект, например, у НД по НДС загружаются отдельными файлами
        Разделы 8-12
        """

        id_reports = dict()
        for item in loaded_files:
            id_reports[item['Name']] = item['Document']

        return id_reports

    def open_result_panel_js(self, session):
        """
        Открыть панель с результатами загрузки файла
        В случае загрузки одного отчета после выполнения скрипта
        сразу откроется загруженный отчет в соседней вкладке
        :param session сессия загрузки
        :return:
        """
        js_script = "require(['FileResult/Result'],function(m){m.show({sessionId:'%s'});})" % session
        self.browser.execute_script(js_script)

    def check_open_result_panel(self):
        """
        Проверить открытие панели с результатом загрузки файлов
        :return:
        """

        file_panel = FileResultWindow(self.driver)
        file_panel.check_open()
        error = ErrorMessage(self.driver)
        error.check_error_absence()

    def load_file_api_and_open(self, folder, wait_time=30, *files, opened_in_new_tab=True):
        """
        Загрузить и открыть загруженный файл.
        Использовать метод для загрузки одного отчета.

        :param wait_time время ожидания загрузки
        :param folder папка с файлами
        :param files файлы для загрузки
        :param opened_in_new_tab загруженный отчет открывается в новой вкладке

        :return список из ИД загруженный отчетов
        """

        start_count_windows = self.browser.count_windows
        session, id_report_list = self.load_file_api(folder, wait_time, *files)

        log("Открыть загруженный отчет")
        delay(1, "Перед открытием загруженного отчета")
        self.open_result_panel_js(session)
        if opened_in_new_tab:
            self.browser.should_be(CountWindows(start_count_windows + 1),
                                   msg="Не открылся загруженный отчет в соседней вкладке!", wait_time=True)
            self.browser.switch_to_opened_window()
        else:
            self.browser.should_be(CountWindows(start_count_windows),
                                   msg="Загруженный отчет должен открыться в той же вкладке!", wait_time=True)

        return id_report_list

    def load_file_api_and_open_result_panel(self, folder, wait_time=30, *files):
        """
        Загрузить файл и открыть панель с результатами загрузки
        :param wait_time время ожидания загрузки
        :param folder папка с файлами
        :param files файлы для загрузки

        :return список из ИД загруженный отчетов
        """
        session, id_report_list = self.load_file_api(folder, wait_time, *files)

        log("Открываем панель с результатом загрузки")
        self.open_result_panel_js(session)
        self.check_open_result_panel()

        return id_report_list, session

    @staticmethod
    def get_id_reports_list_from_dict(report_dict):
        """
        Получить список из ИД отчетов из словаря
        :param report_dict: словарь вида "Название отчета": 123
        В методе также удаляются повторяющиеся ИД, так как одинаковые ИД относятся
        к одному и то же отчету - комплекту
        :return: список из ИД отчетов
        """

        id_report_list_all = list(report_dict.values())
        # Убираем повторяющиеся ИД, так как некоторые файлы относятся к одному и тому же отчету
        id_report_list = list(set(id_report_list_all))
        return id_report_list

    def file_download_js(self, button, folder_name, *files_name):
        """Загрузка файлов через js с открытием окна выбора файлов
        Например, загрузка с главной страницы, дозагрузка файлов в отчет.

        :param button: кнопка, клик по которой открывает окно выбора файлов
        :param folder_name: путь до папки с файлами
        :param files_name: имена загружаемых файлов
        """

        log("Загружаем отчет")
        delay(1, "Перед кликом")
        button.click()
        load = SelectFilesDialog(self.driver)
        load.load_file_js(folder_name, *files_name)

    def format_file_in_download_window(self, row_number, **kwargs):
        """
        Метод проверяет, что в окне выбора файлов файлы определяются как форматные
        Проверяемые атрибуты передавать в виде словаря.
        :param row_number: номер строки с отчетом в окне выбора файлов
        :param kwargs: словарь с атрибутами отчета
        """

        if "Название отчета" in kwargs.keys():
            self.files_tbl.cell(row_number, 2).element('.documentName').\
                should_be(ExactText(kwargs.get('Название отчета')), msg="Неверное название отчета!")
        if "Название организации" in kwargs.keys():
            self.files_tbl.cell(row_number, 2).element('.contragentName').\
                should_be(ExactText(kwargs.get('Название организации')), msg="Неверное название организации!")
        if "Отчетный период" in kwargs.keys():
            self.files_tbl.cell(row_number, 4).element('.periodDate').\
                should_be(ExactText(kwargs.get("Отчетный период")), msg="Неверный период!")
        if "Дополнительная информация" in kwargs.keys():
            self.files_tbl.cell(row_number, 2).element('.additionalInfo').\
                should_be(ExactText(kwargs.get("Дополнительная информация")))
        if "Файл" in kwargs.keys():
            self.files_tbl.cell(row_number, 4).element('.fileName').should_be(ExactText(kwargs.get("Файл")),
                                                                              msg="Неверный файл!")

    def check_org_on_configuration(self, name_org, inn, kpp):
        """
        Проверка наличия организации.

        :param name_org: краткое название организации
        :param inn: ИНН организации
        :param kpp: КПП организации
        """

        from pages_inside.saby_pages.entity_list import EntitiesList

        entity_list = EntitiesList(self.driver)
        entity_list.go_to_our_company()
        entity_list.search_org(inn)
        entity_list.list_org.row(contains_text=inn).should_be(Displayed, TextIgnoringCase(name_org), ContainsText(kpp),
                                                              msg=f"Не найдена организация с ИНН {inn} КПП {kpp}!")

    # todo Разбить метод, вынести в библиотеки сотрудников (Сане не нравится 15.02.21)
    def check_staff_cards(self, org, **kwargs):
        """Проверка данных по сотрудникам в разделе Сотрудники
        :param org Организация
        :param kwargs словарь с данными вида
        {"Иванов Иван": {"Основные данные": {"СНИЛС": "11111"}, "Дополнительно": {"Дата выдачи": "11.11.11"}},
        "Петров Петр": {"Основные данные": {"ИНН": "22222"}}}

        """

        from pages_inside.libraries.Employee.personalInfo import Content
        from pages_inside.libraries.Employee.Card import Base
        from pages_inside.libraries.PersonData.base import Snils, Inn, DateOfBirth
        from pages_inside.saby_pages.staff_list import StaffRegistry
        from helpers import datageneration

        staff_reg = StaffRegistry(self.driver)
        staff_reg.open()
        staff_reg.hide_hints()  # Убрать всплывающие подсказки
        staff_reg.change_org(org)
        page_card = Base(self.driver)
        personal_data = Content(self.driver)

        for fio, fio_data in kwargs.items():
            fio = datageneration.Name(fio)

            log(f"Проверяем данные по сотруднику {fio.name}")
            staff_reg.search_and_open(fio.brief_name)
            page_card.accordeon_move("Работа", "Личные данные")
            if fio_data.get('ДатаРождения'):
                DateOfBirth(self.driver).check_date_of_birth(fio_data.get('ДатаРождения'))
            if fio_data.get('Подразделение'):
                page_card.depart_txt.should_be(ExactText(fio_data.get('Подразделение')))
            if fio_data.get('СНИЛС'):
                Snils(self.driver).check_snils(fio_data.get('СНИЛС'))
            if fio_data.get('ИНН'):
                Inn(self.driver).check_inn(fio_data.get('ИНН'))
            if fio_data.get('ВидДокумента'):
                personal_data.passport_data.check_identity_card(**fio_data)
            if fio_data.get('Адрес'):
                personal_data.address.address_read.should_be(ExactText(fio_data.get("Адрес")))
            page_card.close()

    def check_org_card(self, org, **kwargs):
        """Проверить данные в карточке организации
        :param org
        :param kwargs Данные для проверки в карточке организации
        """

        from pages_inside.saby_pages.entity_list import EntitiesList as OurCompany
        from pages_inside.libraries.Entity.ourCompany import CardPage

        our_comp = OurCompany(self.driver)
        our_comp.go_to_our_company()
        our_comp.search_and_open_org(org)
        card_org = CardPage(self.driver)

        if 'Телефон' in kwargs.keys():
            card_org.contacts_block.controller.contacts.should_be(Displayed, ContainsText(kwargs.get('Телефон')))
        if 'Адрес' in kwargs.keys():
            card_org.address_form.law_address.check_address(kwargs.get('Адрес'))
        if 'Полное название' in kwargs.keys():
            card_org.check_data_org(**{'Название полное': kwargs.get('Полное название')})
        if 'email' in kwargs.keys():
            card_org.contacts_block.controller.contacts.should_be(Displayed, ContainsText(kwargs.get('email')))

    def log_long_load_methods(self, client_cloud, ses_id, start_time_log, end_time_log, max_time, test_name, file_path):
        """
        Метод находит и выводит в лог долгие методы при загрузке файлов
        :param client_cloud: клиент в облаке
        :param ses_id: id сессии
        :param start_time_log: начало загрузки
        :param end_time_log: окончание загрузки
        :param max_time: максимальное время выполнения
        :param test_name: название теста
        :param file_path: путь до файла, куда записываем долгие методы
        """

        from api.clients.report.analytics import Analytics

        keys = ['DateTime', 'Method', 'Duration', 'UUID', 'Message']
        delay(60, 'Ждем, чтобы логи точно пришли')
        res = Analytics(client_cloud).analysis_loadmethods(start_time_log, end_time_log, ses_id, max_time)
        if res:
            log(f'{test_name}. Выводим методы, которые выполнялись дольше {max_time} мс')
            with open(file_path, 'a', encoding='utf8') as file:
                for item in res:
                    item1 = item.copy()
                    list(filter(lambda el: item1.pop(el[0]) if el[0] not in keys else True, item.items()))
                    log(item1)
                    json.dump(item1, file)
                    file.write('\n')
        else:
            log(f'{test_name}. Методов, которые выполнялись дольше {max_time} мс, не обнаружено')

