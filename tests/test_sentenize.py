import unittest

from sentenize import *


class TestStringMethods(unittest.TestCase):

    def test_replace_latin_letters(self):
        text = "cекции"
        assert replace_latin_letters(text) == "секции"

    def test_cleans_the_text1_1(self):
        text1 = ' FOO\n'
        assert primary_text_cleaning(text1) == ' FOO '

        text2 = '\xa0FOOØ'
        assert primary_text_cleaning(text2) == ' FOO '

    def test_cleans_the_text1_2(self):
        text1 = '0. 5'
        assert primary_text_cleaning(text1) == '0.5'

    def test_cleans_the_text1_3(self):
        text1 = '0,5'
        assert primary_text_cleaning(text1) == '0.5'

    def test_cleans_the_text1_4(self):
        text1 = '100 В, 15 В'
        assert primary_text_cleaning(text1) == '100 В, 15 В'

    def test_cleans_the_text1_5(self):
        text1 = '0, 5 В'
        assert primary_text_cleaning(text1) == '0.5 В'

    def test_cleans_the_text1_6(self):
        text1 = '°C'
        assert secondary_text_cleaning(text1) == 'C'

    def test_primary_text_cleaning1_5(self):
        text1 = "при ø 22 мм на 42 % больше"
        assert primary_text_cleaning(text1) == 'при диаметр 22 мм на 42 % больше'

    def test_primary_text_cleaning1_6(self):
        text1 = "водородным показателем рН 6.5...9.5"
        assert primary_text_cleaning(text1) == 'водородным показателем рН 6.5 - 9.5'

    def test_cleans_the_text2(self):
        text1 = '\n()=:Ø（）•~'
        assert secondary_text_cleaning(text1) == ''

    def test_cleans_the_text3(self):
        text1_1 = 'Привет – привет'
        assert secondary_text_cleaning(text1_1) == 'Привет привет'

    def test_cleans_the_text4(self):
        text1_2 = '1000 – 2000'
        assert secondary_text_cleaning(text1_2) == '1000 – 2000'

    def test_cleans_the_text5(self):
        text2 = '+/- max не более +/- min не менее'
        assert secondary_text_cleaning(text2) == '     '

    def test_cleans_the_text6(self):
        text10 = 'ммМощность'
        assert secondary_text_cleaning(text10) == 'мм Мощность'

    def test_cleans_the_text7(self):
        text14 = 'мммощность'
        assert secondary_text_cleaning(text14) == 'мм мощность'

    def test_cleans_the_text8(self):
        text11 = 'кгс/см2'
        assert secondary_text_cleaning(text11) == 'кгс/см2'

    def test_cleans_the_text9(self):
        text12 = '0,3Коэффициент'
        assert secondary_text_cleaning(text12) == '0,3 Коэффициент'

    def test_cleans_the_text20(self):
        text20 = 'м2Сила'
        assert secondary_text_cleaning(text20) == 'м2 Сила'

    def test_cleans_the_text21(self):
        text20 = 'Трансформатор ТСМ560 12шт'
        assert secondary_text_cleaning(text20) == 'Трансформатор 12шт'

    def test_cleans_the_text22(self):
        text20 = '1200Х730 мм'
        assert secondary_text_cleaning(text20) == '1200 Х 730 мм'

    def test_cleans_the_text23(self):
        text20 = 'ДхГхВ'
        assert secondary_text_cleaning(text20) == ''

    def test_cleans_the_text24(self):
        text20 = 'ДхШ'
        assert secondary_text_cleaning(text20) == ''

    def test_cleans_the_text25(self):
        text20 = '10 ~ 20'
        assert secondary_text_cleaning(text20) == '10 - 20'

    def test_parser_dot(self):
        text1 = 'привет Привет'
        assert separate_sentences(text1) == ['привет ', 'Привет']

        text2 = 'Текст1; текст2'
        assert separate_sentences(text2) == ['', 'Текст1', ' текст2']

        text3 = 'текст -текст2'
        assert separate_sentences(text3) == ['текст ', 'текст2']

    def test_replace_volt(self):
        text = 'Напряжение двигателя 100 в'
        assert replace_volt(text) == 'Напряжение двигателя 100 В '

    def test_replace_gabarit(self):
        text = 'Габариты 10 10 10 мм'
        assert replace_gabarit(text) == 'Габариты 10x10x10 мм'

    def test_replace_gabarit2(self):
        text = 'Габариты 10 10 мм'
        assert replace_gabarit(text) == 'Габариты 10x10 мм'

    def test_replace_gabarit3(self):
        text = 'Размеры 10 10 мм'
        assert replace_gabarit(text) == 'Размеры 10x10 мм'

    def test_replace_gabarit4(self):
        text = 'Габаритный размер 1200 Х 700х1120 мм'
        assert replace_gabarit(text) == 'Габаритный размер 1200x700x1120 мм'

    def test_replace_gabarit5(self):
        text = "Максимальный размер 1мм - 125cИнструкция "
        assert replace_gabarit(text) == 'Максимальный размер 1мм - 125cИнструкция '

    def test_split_text_sentenize_and_is_number1(self):
        text = 'Производительность кубов (Атм) 5180'
        assert split_text_sentence_and_is_number(text) == ['Производительность кубов Атм 5180']

    def test_split_text_sentenize_and_is_number2(self):
        text = "Ролик диаметр 50.6 мм с толщиной стенки 1.5 мм. длина 500 мм - 387 руб. 2"
        assert split_text_sentence_and_is_number(text) == [
            'Ролик диаметр 50.6 мм с толщиной стенки 1.5 мм. длина 500 мм - 387 руб. 2']

    def test_delet_stop_words(self):
        text = 'Привет может быть'
        assert delete_stop_words(text) == 'Привет'

    def test_is_number_and_measures1(self):
        text = '100 В'
        assert is_number_and_measures(text) == True

    def test_is_number_and_measures2(self):
        text = '100'
        assert is_number_and_measures(text) == False

    def test_is_number1(self):
        text = '100'
        assert is_number(text) == True

    def test_is_number2(self):
        text = ' 100/5 '
        assert is_number(text) == True

    def test_is_number3(self):
        text = '100,5'
        assert is_number(text) == True

    def test_is_number4(self):
        text = '100,5 м'
        assert is_number(text) == False

    def test_create_cores_from_structural_data1(self):
        text = "{'Страна-производитель': 'Россия', 'Диаметр': '3 мм', 'Вес': '0.025 кг'}"
        assert create_cores_from_structural_data(text) == [
            {'core': 'страна-производитель', 'name': 'Страна-производитель', 'value': 'Россия', 'weight': 2.5},
            {'core': 'диаметр', 'name': 'Диаметр', 'value': 3, 'measure': 'мм', 'weight': 2.5},
            {'core': 'вес', 'name': 'Вес', 'value': 0.025, 'measure': 'кг', 'weight': 2.5}]

    def test_create_cores_from_structural_data2(self):
        text = "{'Страна-производитель': 'Россия', 'Диаметр, мм': '3', 'Вес': '0.025 кг', 'Артикул': '123'}"
        assert create_cores_from_structural_data(text) == [
            {'core': 'страна-производитель', 'name': 'Страна-производитель', 'value': 'Россия', 'weight': 2.5},
            {'core': 'диаметр', 'name': 'Диаметр', 'value': 3, 'measure': 'мм', 'weight': 2.5},
            {'core': 'вес', 'name': 'Вес', 'value': 0.025, 'measure': 'кг', 'weight': 2.5},
            {'core': 'артикул', 'name': 'Артикул', 'value': '123', 'weight': 2.5}]

    def test_create_cores_from_structural_data3(self):
        text = "{'Страна-производитель': 'Россия', 'Диаметр, мм': '3', 'Вес': '0.025 кг'}"
        assert create_cores_from_structural_data(text) == [
            {'core': 'страна-производитель', 'name': 'Страна-производитель', 'value': 'Россия', 'weight': 2.5},
            {'core': 'диаметр', 'name': 'Диаметр', 'value': 3, 'measure': 'мм', 'weight': 2.5},
            {'core': 'вес', 'name': 'Вес', 'value': 0.025, 'measure': 'кг', 'weight': 2.5}]

    def test_create_cores_from_structural_data4(self):
        text = "{'Вес': '0.025 танн'}"
        assert create_cores_from_structural_data(text) == [
            {'core': 'вес', 'name': 'Вес', 'value': 0.025, 'measure': 'танн', 'weight': 2.5}]

    def test_create_cores_from_structural_data5(self):
        text = "{'Вес': '06.2022 по'}"
        assert create_cores_from_structural_data(text) == [
            {'core': 'вес', 'name': 'Вес', 'value': 6.2022, 'measure': 'по', 'weight': 2.5}]

    def test_create_cores_from_structural_data6(self):
        text = """{"Вес, кг": "0,02"}"""
        assert create_cores_from_structural_data(text) == [
            {'core': 'вес', 'name': 'Вес', 'value': 0.02, 'measure': 'кг', 'weight': 2.5}]

    def test_create_cores_from_structural_data7(self):
        text = """{"Производительность кубов, м час": "5180"}"""
        assert create_cores_from_structural_data(text) == [
            {'core': 'производительность', 'core_nmod0': 'куб', 'name': 'Производительность кубов', 'value': 5180,
             'measure': 'ч', 'weight': 2.5}]

    def test_create_cores_from_structural_data8(self):
        text = """{"Производительность кубов (Атм)": "5180"}"""
        assert create_cores_from_structural_data(text) == [
            {'core': 'производительность', 'core_nmod0': 'куб', 'name': 'Производительность кубов', 'value': 5180,
             'measure': 'Атм', 'weight': 2.5}]

    def test_create_cores_from_structural_data9(self):
        text = """{"Производительность кубов (Атм),": "5180"}"""
        assert create_cores_from_structural_data(text) == [
            {'core': 'производительность', 'core_nmod0': 'куб', 'name': 'Производительность кубов', 'value': 5180,
             'measure': 'Атм', 'weight': 2.5}]

    def test_create_cores_from_structural_data10(self):
        text = """{"Ток":"500А"}"""
        assert create_cores_from_structural_data(text) == [
            {'core': 'ток', 'name': 'Ток', 'value': '500А', 'weight': 2.5}]

    def test_create_cores_from_structural_data11(self):
        text = """{"Ток":"Электромагнитный"}"""
        assert create_cores_from_structural_data(text) == [
            {'core': 'ток', 'name': 'Ток', 'value': 'Электромагнитный', 'weight': 2.5}]

    def test_create_cores_from_structural_data12(self):
        text = """{"Возможности поставок": "2 шт./неделя"}"""
        assert create_cores_from_structural_data(text) == [
            {'core': 'возможность', 'core_nmod0': 'поставка', 'name': 'Возможности поставок', 'value': 2,
             'measure': 'шт./неделя', 'weight': 2.5}]

    def test_create_cores_from_structural_data13(self):
        text = """{"Температурный режим":
            "низкотемпературные (от -15 до -25°С)"}"""
        assert create_cores_from_structural_data(text) == [
            {'core': 'режим', 'core_amod0': 'температурный', 'name': 'Температурный режим', 'value': 'от -15 до -25',
             'measure': '°С', 'weight': 2.5}]

    def test_create_cores2(self):
        text = " Габаритный размер   1200Х700х1120 мм "
        assert create_cores(text) == [{'core': 'размер', 'name': 'Габаритный размер', 'value': '1200x700x1120', 'measure': 'мм', 'weight': 1.5}]

    def test_create_cores3(self):
        text = "Температура перекачиваемой воды от +1 до +40 ⁰С"
        assert create_cores(text) == [{'core': 'температура', 'core_nmod0': 'перекачивать', 'core_nmod_nmod0': 'вода', 'name': 'Температура перекачиваемой воды', 'value': 'от +1 до +40', 'measure': '°C', 'weight': 1.5}]

    def test_del_repeat_measures(self):
        text = "Габариты в упаковке 1100 мм х 700 мм х 1100 мм"
        assert delete_repeat_measures(text) == "Габариты в упаковке 1100  х 700  х 1100 мм"

    def test_del_repeat_measures2(self):
        text = "Температурный режим от -15C до -25C"
        assert delete_repeat_measures(text) == "Температурный режим от -15 до -25C"


if __name__ == '__main__':
    unittest.main()
