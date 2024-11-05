import hashlib
import json
import mimetypes
import os
from urllib.parse import quote

import requests
from atf import *


def upload_file(client, file_path, link):
    """Загрузка простого файла через RPC API метод Сбис.Диск
    :param file_path - путь к файлу
    :param client - экземпляр класса Client
    :param link - ссылка на файл в ХФ
    """

    log("Загружаем файл %s в СБИС.Диск" % file_path.encode("utf-8").decode(), "[m]")
    filename = os.path.basename(file_path)
    size = os.path.getsize(file_path)
    hash_md5 = hashlib.md5()
    hash_md5.update(file_path.encode())
    r = client.call("FileSD.CreateFile", "/disk/api/v1/",
                    Object={"d": ['mydocs', filename, size, link, hash_md5.hexdigest()],
                            "s": [{"n": "ParentId", "t": "Строка"},
                                  {"n": "Name", "t": "Строка"},
                                  {"n": "Size", "t": "Число целое"},
                                  {"n": "Link", "t": "Строка"},
                                  {"n": "MD5", "t": "Строка"}]})

    return r["d"][0], r["d"][1]


def upload_file_to_sbis_disk(file_path, site, sid):
    """Загружаем файл на СБИС.Диск
    Документация по методу -
    https://online.sbis.ru/shared/disk/76328463-8edf-409f-82e0-589183f8e709
    Раздел "Закачать файл/папку"
    :param file_path - путь к файлу
    :param site - адрес стенда
    :param sid - ИД сессии в браузере
    :return ИдентификаторДискДокумент и ИдентификаторДискВерсияДокумента
    """

    info("Загружаем файл %s на СБИС.Диск" % file_path.encode("utf-8").decode())
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    info("Путь до файла - {0}. Имя файла - {1}. Размер - {2}".format(file_path, file_name, file_size))

    if ".xlsx" in file_name:
        file_mymetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif ".djvu" in file_name:
        file_mymetype = "image/vnd.djvu"
    elif ".ods" in file_name:
        file_mymetype = "application/vnd.oasis.opendocument.spreadsheet"
    elif ".rtf"in file_name:
        file_mymetype = "application/rtf"
    elif ".csv"in file_name:
        file_mymetype = "text/csv"
    elif ".sgn" in file_name:
        file_mymetype = "text/xml"
    else:
        file_mymetype = mimetypes.guess_type(file_path)[0]

    headers = {"X-SBISDISK": "1",
               "X-SBISSessionID": sid,
               "Content-Length": str(file_size),
               "Content-Type": file_mymetype,
               "Content-Disposition": "attachment; filename*=UTF-8''{}".format(quote(file_name.encode("utf-8")))
               }
    info("Заголовки - {}".format(headers))
    with open(file_path.encode("utf-8").decode(), 'rb') as file:
        response = requests.request(method='POST',
                                    url=site + "disk/api/v1/temp/",
                                    headers=headers,
                                    data=file)
        try:
            assert json.loads(response.text)["status"] == 201, \
                "Не удалось загрузить файл!\nОшибка: %s" % response.text
        except Exception as e:
            raise AssertionError('Не удалось загрузить файл. Ошибка: {}'.format(e))
        file_id = json.loads(response.text)["fileid"]
        version_id = json.loads(response.text)["versionid"]
    return file_id, version_id
