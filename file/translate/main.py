"""Модуль для перевода"""
import os
import json
from atf.config import Config


config = Config()
translate_dict = dict()


def translate(string: str, main=False):
    """Функция для перевода
    :param main: приоритет выбора опции, если main=False, то опция приоритетно берется из кастомного файла
    Если True, то вне зависимости от опции в кастомном файле, возьмется из основного
    :type string: строка которую нужно перевести
    """

    assert string, "Передана пустая строка"
    global translate_dict
    lang = config.get('LANG')

    if lang:
        lang = lang.lower()
        module_path = os.path.split(os.path.abspath(__file__))[0]
        translate_json = os.path.join(module_path, lang + '.json')
        if lang in translate_dict:
            pass
        elif os.path.exists(translate_json):
            with open(translate_json, 'r', encoding='utf-8') as file:
                translate_dict[lang] = json.load(file)
            if os.path.exists(lang + '.json'):
                with open(lang + '.json', 'r', encoding='utf-8') as file:
                    translate_dict[lang+'_custom'] = json.load(file)
        elif not os.path.exists(translate_json):
            raise FileNotFoundError('Не найден файл для перевода ' + translate_json)

        main_value = translate_dict[lang].get(string)
        custom_dict = translate_dict.get(lang + '_custom')
        if not main and custom_dict:
            custom_value = custom_dict.get(string)
            translate_value = custom_value or main_value or string
        else:
            translate_value = main_value or string
    else:
        translate_value = string
    return translate_value


if __name__ == '__main__':
    from atf.assert_that import equal_to, assert_that
    config.set('LANG', 'eng', 'CUSTOM')
    assert_that("companies", equal_to(translate("компании")), 'Ошибка')
    assert_that("Companies", equal_to(translate("Компании")), 'Ошибка')
    assert_that("Компани", equal_to(translate("Компани")), 'Ошибка')
