"""
В файле описаны API методы объекта Uploading
"""
from atf.api import generate_record
from atf.api.base_api_ui import BaseApiUI


class UploadingAPI(BaseApiUI):
    """В классе описаны API методы объекта Uploading"""

    path = "/fileloader-facade"

    def __init__(self, client):

        super().__init__(client)

    def uploading_create(self, file_info, id_doc=None):
        """Загрузить отчет
        :param file_info - информация о файле - список из словарей
        :param id_doc ИД документа, в который загружаются файлы
        :return Сессия загрузки
        """

        params_load = {
            "Settings":
                {"d": [0],
                 "s": [
                     {"n": "Source",
                      "t": "Число целое"}]},
            "Files":
                {"d": [],
                    "s": [
                        {"n": "Name",
                         "t": "Строка"},
                        {"n": "Size",
                         "t": "Число целое"},
                        {"n": "Parameters",
                         "t": "Запись"}]}}


        # Здесь формируется значение для ключа d в словаре Files
        d_list = list()  # значение ключа d в словаре Files
        for item in file_info:
            new_list = list()  # Каждый список new_list - это информация по одному загружаемому файлу
            new_list.append(item['file_name'])
            new_list.append(item['size'])
            if id_doc:
                parameters = {"s": [{"n": "Документ", "t": "Число целое"},
                                    {"n": "ИдентификаторДискДокумент", "t": "UUID"},
                                    {"n": "ИдентификаторДискВерсияДокумента", "t": "Строка"},
                                    {"n": "LoadMode", "t": "Число целое"}
                                    ],
                              "d": [id_doc,
                                    item['uuidf'],
                                    item['ver'],
                                    None
                                    ],
                              "_type": "record"}
            else:
                parameters = {"s": [{"n": "ИдентификаторДискДокумент", "t": "UUID"},
                                    {"n": "ИдентификаторДискВерсияДокумента", "t": "Строка"}
                                    ],
                              "d": [item['uuidf'],
                                    item['ver']
                                    ],
                              "_type": "record"}

            new_list.append(parameters)
            d_list.append(new_list)
        params_load['Files']['d'] = d_list

        response = self.client.call_rrecord("Uploading.Create", self.path, **params_load).result
        dw_session = response['ID']
        return dw_session

    def get_result(self, dw_session):
        """Получить статус загрузки
        :param dw_session Сессия загрузки
        :return Статус загрузки
        """

        return self.client.call_rrecord("Uploading.GetResult", self.path, ID=dw_session).result

    def read_result(self, session_id: str):
        """
        Получить результат загрузки
        :param session_id: ИД сессии
        """

        params = {'ID': session_id,
                  'Filter': generate_record(IsResult=True,
                                            IsSortByDate=True,
                                            NumAllGroup=5,
                                            NumSingleGroup=25)}

        return self.client.call_rrecord('Uploading.ReadResult', **params, path='fileloader-facade').result

    def uploading_create_long(self, file_info, id_report=None, id_doc=None, loader_type='ListOfDocuments'):
        """Загрузить отчет
        :param file_info - информация о файле - список из словарей
        :param id_doc ИД документа, в который загружаются файлы
        :param loader_type: тип загрузчика
        :return Сессия загрузки
        """

        from datetime import datetime

        date_load = datetime.now().strftime('%Y-%m-%d %H:%M:%S+03')

        settings = generate_record(Source=0,
                        ClientOperationID='dc6b05cb-28b5-400d-bd2d-815a4a4c8d7d',
                        LRS=False,
                        ТипЗагрузчика=loader_type,
                        Type='СлужебныеЭО',
                        SubType='ПриложениеЭО',
                        ReportId=id_report,
                        Документ=id_doc,
                        __SendDate__=(date_load, 'Дата и время'))

        params_load = {
            "Settings": settings,
            "Files":
                {"d": [],
                 "s": [
                     {"n": "Name",
                      "t": "Строка"},
                     {"n": "Size",
                      "t": "Число целое"},
                     {"n": "Parameters",
                      "t": "Запись"}]}}

        # Здесь формируется значение для ключа d в словаре Files
        d_list = list()  # значение ключа d в словаре Files
        for item in file_info:
            new_list = list()  # Каждый список new_list - это информация по одному загружаемому файлу
            new_list.append(item['file_name'])
            new_list.append(item['size'])
            parameters = generate_record(ТипЗагрузчика=loader_type,
                            Type='СлужебныеЭО',
                            SubType='ПриложениеЭО',
                            ReportId=id_report,
                            Документ=id_doc,
                            ИдентификаторДискДокумент=(item['uuidf'], 'UUID'),
                            ИдентификаторДискВерсияДокумента=item['ver'])

            new_list.append(parameters)
            d_list.append(new_list)
        params_load['Files']['d'] = d_list

        response = self.client.call_rrecord("Uploading.CreateLong", self.path, **params_load).result
        dw_session = response['ID']
        return dw_session
