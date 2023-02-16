import json
from razdel import sentenize
import re
from tqdm import tqdm
import core_file as cf
from yargy_setting import parser_characteristics, parser_measure_and_value, parser_value


stop_words = ['может', 'быть', 'уже']
SET_CORE_ALL_JSON = []


class Measures:
    """Класс для работы с единицами измерения"""
    def __init__(self, curs):
        self.curs = curs
        self.dict_measure = {}

    @staticmethod
    def __cleans_the_text1(text: str):
        """Удаляет элементы, мешающие распознать предложение
        """
        text = re.sub(r'\n|\s+|\\xa0|Ø|\'|\"', ' ', str(text))
        text1 = re.sub(r'(\d+)[.,] *(\d+)', r'\1.\2', str(text))
        return text1

    @staticmethod
    def __is_measure(text):
        """
        Проверяет текст на длину более 6 символов
        и текст содержит буквы
        """
        is_alpha = re.search('[a-zА-ЯA-Zа-я]', text)
        return (len(text) < 6) and is_alpha

    @classmethod
    def __search_measures_and_text(cls, measure: str, text: str, dict_measure: dict) -> dict:
        """Формирует словарь из единиц измерений
        measure: единицы измерений, например мм2;
        text: текст где встретилась единица измерения
        dict_measure: словарь {мм2:[1, 'Длина 10 мм2']}
        """
        if cls.__is_measure(measure):
            maybe_measure = measure.strip('., \\/?\"\'')
            if maybe_measure in dict_measure and maybe_measure:
                dict_measure[measure] = [dict_measure.get(measure, [0])[0] + 1, text]
            return dict_measure

    @staticmethod
    def __sorted_dict_measure(func):
        """Сортирует словарь в значении которого список.Сортировка по первому элементу списка
        """

        def wrapper(*args, **kwargs):
            dict_measure = func(*args, **kwargs)
            dict_measure = {k: v for k, v in sorted(dict_measure.items(), key=lambda item: item[1], reverse=True)}
            return dict_measure

        return wrapper

    def extract_values_from_data(self):
        """Полученный итератор из базы данных с текстом, в котором ищутся единицы измерения
        """
        data = (eval(row) for cur in self.curs for row in cur)
        values = (j for i in filter(None, data) for j in i.items())
        return values

    @__sorted_dict_measure
    def search_measure_maybe(self):
        """Находит предположительные строки с единицами измерений
        """
        for name, value in tqdm(self.extract_values_from_data(), desc=f'Поиск единиц измерений'):
            if is_number_and_measures(value):
                values_clear = self.__cleans_the_text1(value)
                extract_measure_maybe = re.findall(r'\A[\d.,]+ ([\w\s/.]+)', values_clear)
                measure_maybe = ''.join(extract_measure_maybe)
                name_value = f'{name} {value}'
                self.dict_measure = self.__search_measures_and_text(measure_maybe, name_value, self.dict_measure)
        return self.dict_measure

    @staticmethod
    def get_measures_base_from_txt() -> list:
        """Получает список с единицами измерений
        """
        paht_measures_base = 'sources/measures_base.txt'
        with open(paht_measures_base, "r", encoding='utf-8') as file:
            texts = file.readlines()
            measures_base = [i.strip() for i in texts]
        return measures_base


def delete_stop_words(text: str) -> str:
    """Удаляет стоп-слова
    """
    text_no_stop_words = []
    for word in text.split():
        if word not in stop_words:
            text_no_stop_words.append(word)
    return ' '.join(text_no_stop_words)


def delete_repeat_measures(text: str):
    """ Удаляет единицы измерения одной величины.
    Например: 10мм х 20 мм преобразует в 10 х 20 мм
    """
    pattern = r"\s?[+-]?\d+.?\d*\s?([a-zA-Zа-яА-Я\d\/]+)\s?(?:[xXхХ]|до)\s?[+-]?\d+.?\d*\s?(\1)(?:\s?[xXхХ]|до)*\s?(?:[+-]?\d+.?\d*\s?(\1))*"
    matches = re.findall(pattern, text)
    if not matches:
        return text
    matches_is_not_num = list(filter(lambda x: x and not x.isdigit(), matches[0]))
    N = len(matches_is_not_num) - 1
    if 0 < N <= 2 and len(set(matches_is_not_num)) == 1:
        return text.replace(matches_is_not_num[0], '', N)
    return text


def primary_text_cleaning(text: str):
    """
    Удаляет элементы, мешающие распознать предложение
    """
    text = re.sub(r'\n|\s+|\\xa0|Ø|\'|\"', ' ', str(text))
    text = re.sub(r'(\d+)[.,] *(\d+)', r'\1.\2', text)
    text = re.sub(r'[Мм]акс[\b\.]', 'максимальный', text)
    text = re.sub(r'[Дд]иам[\b\.]|ø', 'диаметр', text)
    text = re.sub(r'\.\.\.', r' - ', text)
    return text


def secondary_text_cleaning(text: str) -> str:
    """
    Очистка текста от мусора
    """
    text = re.sub(r'(\b[А-ЯA-Z][А-ЯA-Za-z\d]{2,})|(\b\d[А-ЯA-Z][А-ЯA-Za-z\d]{2,})', '', str(text))
    text = re.sub(r"[ДдШшГгВв]\s?[хХ*xX/]\s?[ГгШшДдВв]\s?[хХ*Xx/]*\s?[ВвШшГгДд]*", "", text)
    text = re.sub(r"(\d+\s?)(~)(\s?\d+)",r"\1-\3", text)
    text = re.sub(r'[•\n()=:Ø（）~_\\]', " ", text).replace('   ', ' ').strip().replace('×', 'х').replace('*',
                                                                                                           'х').replace(
        '  ', ' ')
    text = re.sub(r'[°⁰0][CС]', 'C', text)
    text = re.sub(r'(max|не более|\+/-)|(min|не менее)', '', text)
    text = re.sub(r'([а-я]{4,}) ?[-/–] ?([а-я]{2,})', r'\1 \2', text)
    text = re.sub(r'([а-я]{4,}),', r'\1', text)
    text = re.sub(r'([А-Я])([А-Я][а-я]{4,})', r'\1 \2', text)
    text = re.sub(r'([а-я]{4,})(\d{2,})', r'\1 \2', text)
    text = re.sub(r'([А-Я])([А-Я][а-я]{2,})', r'\1 \2', text)
    text = re.sub(r'([А-Я][а-я]*)(\d{2,})', r'\1 \2', text)
    text = re.sub(r'([А-Я][а-я]+)\.\B', r'\1', text)
    text = re.sub("([а-я]\d*[А-Я]*[а-я]*)([А-Я][а-я]{2,})", r'\1 \2', text)
    text = re.sub(r'([А-Я][а-я]{3,})([А-Я][а-я]*)', r'\1 \2', text)
    text = re.sub(r'(\d{2,}|,\d)([А-Я][а-я]*)', r'\1 \2', text)
    text = re.sub(r'(\bмм)([А-Яа-я]{4,})', r'\1 \2', text)
    text = re.sub(r'([кК]ол-во)', r'количество', text)
    text = re.sub(r'(³)', r'3', text)
    text = re.sub(r'(²)', r'2', text)
    return text


def replace_latin_letters(text):
    """Заменяет латинские буквы на русские
    """
    latin_to_russian = {'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'k': 'к', 'c': 'с', 'l': 'л',
                        'm': 'м', 'n': 'н', 'o': 'о', 'W': 'В', 'A': 'A'}
    pattern = '|'.join(latin_to_russian.keys())
    return re.sub(pattern, lambda x: latin_to_russian[x.group()], text)


def replace_volt(text):
    """Если есть в тексте "в" и "напряжение", то заменить "в" на "В"
    """
    volt_re = r'[Нн]апряж.*\bв\b'
    text2 = re.findall(volt_re, text)
    if text2:
        text3 = ' '.join(text2).replace(' в', ' В ')
        return text3
    return text


def replace_gabarit(text):
    """Если есть в тексте "Габарит" или "Размер" , то приводит числа к форме 10х10"
    """
    text = delete_repeat_measures(text)
    text2 = re.findall(r'[Гг]абарит.*(?:\d+)[^\d]+(?:\d+)|[Рр]азмер.*(?:\d+)[^\d]+(?:\d+)', str(text))
    if text2:
        text3 = re.sub(r'(?<=\d)[^\d]{1,4}(?=\d)', r'x', text)
        return text3
    return text


def separate_sentences(text: str):
    """Разделяет текст на предложения
    """
    match = re.split(
        r"(?="
        r"\b[А-Я][а-я][а-я][а-я]+)"
        r"|\B-\b"
        r"|;",
        text, re.X)
    return match


def search_number_in_text(text):
    """Проверяет есть ли число в тексте
    """
    match = re.search(r'\d', text)
    return match


def write_json(data, name):
    """Записывает результат работы программы в json.
    """
    json_file = f'output/output_{name}.json'
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def is_measure(text):
    """
    Проверяет текст на длину более 6 символов
    и текст содержит буквы
    """
    is_alpha = re.search('[a-zА-ЯA-Zа-я]', text)
    return (len(text) < 6) and is_alpha


def split_text_sentence_and_is_number(text: str) -> list:
    """Создает список из предложений в которых есть числа.
    """
    lines = primary_text_cleaning(text)
    sentences_list = list(sentenize(lines))
    lines_numbers = []
    for sentences_text in sentences_list:
        if search_number_in_text(sentences_text.text):
            line_no_dot_the_end = sentences_text.text.strip('.')
            line_clean = secondary_text_cleaning(line_no_dot_the_end)
            line = separate_sentences(line_clean)
            for j in filter(search_number_in_text, line):
                lines_numbers.append(j)
    return lines_numbers


def extract_satom_text_or_table(bd: str, key: str):
    """Получает табличные и текстовые данные сатом.
    bd: общие данные из сатом
    key: 'text' или 'table'
    """
    data_dict = eval(bd.replace('\n', ' '))
    description = data_dict.get(key, 'NA')
    if description != 'NA':
        if key == "table":
            merge = ('{} {}'.format(k, v) for k, v in description.items())
            return merge
        return description
    return []


def create_cores(row: str, weight=1.5) -> list:
    """Создает core из текста
    """
    SET_CORE_ALL_JSON.append({f'raw_text': row})
    lines_numbers = split_text_sentence_and_is_number(row)
    set_core_all_db = []
    for line in lines_numbers:
        line = replace_volt(line)
        line = replace_gabarit(line)
        line = delete_stop_words(line).replace(',', '')
        line = replace_latin_letters(line)
        SET_CORE_ALL_JSON.append({'raw': line})
        for match in parser_characteristics.findall(line):
            update_core_match = match.fact.as_json
            name = update_core_match.get('name')
            if name:
                set_core = cf.search_core(name)
                set_core |= update_core_match
                set_core |= {'weight': weight}
                set_core_all_db.append(set_core)
                SET_CORE_ALL_JSON.append(set_core)
    if not set_core_all_db:
        return []
    return set_core_all_db


def is_number_and_measures(text):
    """Проверка на число и текст
    """
    value_and_measure = r'(\d+|\d+,\d+|\d+.\d+) ([\d\/А-Яа-яA-Za-z\ ]+).*(?![^,])'
    return re.search(value_and_measure, text) is not None


def is_number(text):
    """Проверка на число
    """
    text = re.sub(r"\W", "", str(text), flags=re.UNICODE)
    return text.isdigit()


def separate_number_and_measures(text):
    """Разделяет число и текст единиц измерения
    """
    value_and_measure = r'(\d+|\d+,\d+|\d+.\d+) ([\d\/А-Яа-яA-Za-z\ ]+).*(?![^,])'
    value, measure = re.search(value_and_measure, text).groups()
    return value, measure


def create_cores_from_structural_data(data: str, weight=2.5) -> list:
    """Создает core из структурированных данных
    """
    global SET_CORE_ALL_JSON
    result = []
    for row in eval(data).items():
        set_core = {}
        SET_CORE_ALL_JSON.append({'raw': row})
        json_name = {}
        name = row[0]
        text_value_or_value_measure = delete_repeat_measures(primary_text_cleaning(row[1]))
        if is_number_and_measures(text_value_or_value_measure):
            json_name['name'] = name
            delete_repeat_measures(text_value_or_value_measure)
            parser = [match.fact.as_json for match in parser_measure_and_value.findall(text_value_or_value_measure)]
            if parser:
                match_core = parser[0]
                json_name |= match_core
                set_core = cf.search_core(name)
            else:
                value, measure = separate_number_and_measures(text_value_or_value_measure)
                json_name['value'] = [match.fact for match in parser_value.findall(value)][0]
                json_name['measure'] = measure
                set_core = cf.search_core(name)
        elif is_number(text_value_or_value_measure):
            text_unit = f'{name} {text_value_or_value_measure}'.replace(',', '')
            core_text_unit = create_cores(text_unit, weight)
            if core_text_unit:
                json_name |= core_text_unit[0]
            else:
                json_name['name'] = name
                json_name['value'] = text_value_or_value_measure
                set_core = cf.search_core(name)
        else:
            json_name['name'] = name
            json_name['value'] = text_value_or_value_measure
            set_core = cf.search_core(name)
        set_core |= json_name
        set_core |= {'weight': weight}
        result.append(set_core)
        SET_CORE_ALL_JSON.append(set_core)
    return result


def result_text_data(row):
    """Распределяет текст по сатом текст, сатом таблица и другое
    """
    new_characteristics = []
    if row[0] == "{":
        description_text = extract_satom_text_or_table(row, 'text')
        description_table = extract_satom_text_or_table(row, 'table')
        new_characteristics_text = create_cores(description_text, weight=1)
        for i in filter(None, map(create_cores, description_table)):
            new_characteristics.extend(i)
        new_characteristics.extend(new_characteristics_text)
    else:
        new_characteristics = create_cores(row, weight=1)
    return new_characteristics


def create_core_in_db(cur) -> list:
    """Первичное разделение данных на текст, структурированные данные
    Объединяет результаты
    cur: данные из таблиц
    result: список с характеристиками
    """
    global SET_CORE_ALL_JSON
    description_product = cur[1]
    characteristics = cur[2]
    data = [f"{key} {' '.join(values)}" for key, values in eval(cur[3]).items()]
    data = '. '.join(data)
    result = []
    result_text = result_text_data(description_product)
    if result_text:
        result += result_text
    if data:
        result_data = result_text_data(data)
        if result_data:
            result += result_data
    if characteristics != 'NA' and characteristics is not None:
        SET_CORE_ALL_JSON.append({'raw_structur': characteristics})
        result_structural = create_cores_from_structural_data(characteristics)
        result += result_structural
    return result
