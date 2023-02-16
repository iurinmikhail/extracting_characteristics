"""
Создает карточи моделей
"""

import random


def compares(A, text):
    """
    На вход поступает список словарей, если core в них равны, то выдает True, а если не равны, то False
    """
    temp_core = set(key.get(text) for key in A)
    if len(temp_core) != 1 or temp_core == {None}:
        return False
    return True


def get_name_value_measure(lst):
    """
    Из словаря выдает один словарь с name, values, measure
    """
    if isinstance(lst, dict):
        return [{key: value for key, value in lst.items() if key in ['name', 'value', 'measure']}]

    return [{key: value for key, value in dct.items() if key in ['name', 'value', 'measure']} for dct in lst]


def max_count_values(values):
    """
    Находит максимальное значение value из словарей
    """
    max_count = 0
    max_value = 0
    for value in values:
        if max_count < values.count(value):
            max_count = values.count(value)
            max_value = value
    return max_value


def clean_of_duplicates(A) -> list:
    """Удаляет дубликаты сдоварей. На выходе список с уникальными по значению словарями
    """
    return [dict(t) for t in {tuple(d.items()) for d in A}]


def clean_of_core_none(A):
    """Очистка от словарей в которых core None
    """
    core_no_none = filter(lambda x: x.get('core') is not None, A)
    return core_no_none


def unicum_set(A, text):
    """Оставляет множество из уникальных значений словарей"""
    temp_core = set(key.get(text) for key in A)
    return temp_core


def sorted_core(A, key):
    set_core = unicum_set(A, key)
    lst = [[j for j in A if (key, i) in j.items()] for i in set_core]
    return lst


def comparison_core(A):
    A = list(clean_of_core_none(A))
    char_core = []
    for i in sorted_core(A, 'core'):
        if len(i) == 1:
            char_core += i
        else:
            char_core += comparison_core2(i)
    char_core_sorted = sorted(char_core, key=lambda x: x['core'])
    return char_core_sorted


def search_values_weight_and_count(values, weights, counts):
    """Выбирает по весу и популярности, что оставить
    """
    N = len(values)
    data = list(zip(values, weights, counts))
    max_val = max(data, key=lambda x: x[1]/N*x[2])
    return max_val[0]


def comparison_core2(A):
    """Сортирует характеристики для записи в общую карточку модели
    """
    if not A:
        return
    N = len(A)
    if N == 1:
        return A
    elif compares(A, 'core') and compares(A, 'value'):
        return [A[0]]
    elif compares(A, 'core') and not compares(A, 'value'):
        if compares(A, 'core_amod0') or (unicum_set(A, 'core_amod0') == {None} and unicum_set(A, 'core_nmod0') == {None}):
            values = [i.get('value') for i in A]
            wieght = [i.get('weight') for i in A]
            count = [A.count(i) for i in A]
            max_value = search_values_weight_and_count(values, wieght, count)
            for n, i in enumerate(A):
                if i.get('value') == max_value:
                    return [A[n]]
        elif not compares(A, 'core_amod0') and unicum_set(A, 'core_amod0') != {None}:
            check_amod = []
            text_core = [i for i in filter(lambda x: x.get('core_amod0'), A)]
            values_text_core = unicum_set(text_core, 'value')
            text_no_core = [i for i in filter(lambda x: not x.get('core_amod0') and x.get('value') not in values_text_core, A)]
            if text_core and not compares(text_core, 'core_amod0'):
                for i in sorted_core(text_core, 'core_amod0'):
                    check_amod += comparison_core2(i)
                clean_from_duplicates = clean_of_duplicates(check_amod)
                return clean_from_duplicates
            elif text_core and compares(text_core, 'core_amod0'):
                check_amod += comparison_core2(text_core)
            if text_no_core:
                check_amod += comparison_core2(text_no_core)
            return check_amod
        elif compares(A, 'core_nmod0') or (unicum_set(A, 'core_nmod0') == {None}):
            values = [i.get('value') for i in A]
            wieght = [i.get('weight') for i in A]
            count = [A.count(i) for i in A]
            max_value = search_values_weight_and_count(values, wieght, count)
            for n, i in enumerate(A):
                if i.get('value') == max_value:
                    return [A[n]]
        elif not compares(A, 'core_nmod0') and unicum_set(A, 'core_nmod0') != {None}:
            check = []
            text_core = [i for i in filter(lambda x: x.get('core_nmod0'), A)]
            text_no_core = [i for i in filter(lambda x: not x.get('core_nmod0'), A)]
            if text_core and not compares(text_core, 'core_nmod0'):
                for i in sorted_core(text_core, 'core_nmod0'):
                    check += comparison_core2(i)
                clean_from_duplicates = clean_of_duplicates(check)
                return clean_from_duplicates
            elif text_core and compares(text_core, 'core_nmod0'):
                check += comparison_core2(text_core)
            if text_no_core:
                check += comparison_core2(text_no_core)
            return check
    elif not compares(A, 'core') and len(unicum_set(A, 'core')) == N:
        return A
    elif not compares(A, 'core') and unicum_set(A, 'core_amod0') == {None}:
        return A
    elif not compares(A, 'core'):
        if N == 2:
            return A
        elif N > 2:
            middle = N//2
            left_result = comparison_core(A[:middle])
            right_result = comparison_core(A[middle:])
            lst = right_result + left_result
            random.shuffle(lst)
            return comparison_core(lst)





