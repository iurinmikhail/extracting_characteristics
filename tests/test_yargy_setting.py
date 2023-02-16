import json
from yargy_setting import *
import unittest


class TestStringMethods(unittest.TestCase):

    @staticmethod
    def show_json(parser_file):
        """
        Функция для тестов
        Выводит на экран json.
        """
        data = [i.fact.as_json for i in parser_file]
        print(json.dumps(data, indent=2, ensure_ascii=False))

    @staticmethod
    def get_dict_result_digit(parser_file):
        """
        Функция для тестов
        Выводит на экран json.
        """
        data = [i.fact for i in parser_file][0]
        return data

    @staticmethod
    def get_dict_result(parser_file):
        """
        Функция для тестов
        Выводит на экран json.
        """
        try:
            data = [i.fact.as_json for i in parser_file][0]
        except IndexError:
            data = {}
        return dict(data)

    def test_clean_measures(self):
        text = 'Ватт двигателя'
        assert clean_product(text) == 'Двигатель'

        text = 'ватт двигателя'
        assert clean_product(text) == 'Двигатель'

        text = 'КП'
        assert clean_product(text) == None

        text = 'литр'
        assert clean_product(text) == None

    def test_replaces_particles1(self):
        text = 'м час'
        assert replaces_particles(text) == 'м/ч'

    def test_replaces_particles2(self):
        text = 'м в час'
        assert replaces_particles(text) == 'м/ч'

    def test_clean_prtf1(self):
        text = "И мощностью 1 шт 10 ватт в час"
        assert clean_prtf(text) == 'мощностью 1 шт 10 ватт в час'

    def test_clean_prtf2(self):
        text = "Срок изготовления до 21 дня "
        assert clean_prtf(text) == "Срок изготовления до 21 дня "

    def test_show_json1(self):
        text = " И напряж 1 шт 10 ватт в час"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Напряжа', 'value': 10, 'measure': 'Вт/ч'}

    def test_show_json2(self):
        text = "Мощность двигателя 1 шт 10 ватт в час"
        parser_file = parser_characteristics.findall(text)
        self.get_dict_result(parser_file) == {'name': 'Мощность двигателя', 'value': 10, 'measure': 'Вт/ч'}

    def test_show_json3(self):
        text = 'Опыт работы в больших проектах!\\nСрок изготовления до 21 дня '
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Срок изготовления', 'value': 'до 21', 'measure': 'дня'}

    def test_show_json4(self):
        text = "длиной 100 м"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Длина', 'value': 100, 'measure': 'м'}

    def test_show_json4_1(self):
        text = "Ролик диаметр 50.6 м с кругом"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Ролик диаметр', 'value': 50.6, 'measure': 'м'}

    def test_show_json5(self):
        text = "длиной более 100 м"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Длина', 'value': 'более 100', 'measure': 'м'}

    def test_show_json7(self):
        text = "100,1"
        parser_file = parser_value.findall(text)
        assert self.get_dict_result_digit(parser_file) == 100.1

    def test_show_json8(self):
        text = "100 до 1"
        parser_file = parser_value.findall(text)
        assert self.get_dict_result_digit(parser_file) == 100

    def test_show_json11(self):
        text = "Мощность двигателя 10 тонн час"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Мощность двигателя', 'value': 10, 'measure': 'т/ч'}

    def test_show_json12(self):
        text = "Мощность двигателя 10 м2"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Мощность двигателя', 'value': 10, 'measure': 'м2'}

    def test_show_json14(self):
        text = "Производительность кубов м в час 5180"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Производительность кубов', 'value': 5180, 'measure': 'ч'}

    def test_show_json10(self):
        text = "100 м2"
        parser_file = parser_measure_and_value.findall(text)
        assert self.get_dict_result(parser_file) == {'value': 100, 'measure': 'м2'}

    def test_show_json13(self):
        text = "100 м2 в час"
        parser_file = parser_measure_and_value.findall(text)
        assert self.get_dict_result(parser_file) == {'value': 100, 'measure': 'м2/ч'}

    def test_show_json15(self):
        text = "Аккумулятор  24/240 В/Ач"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Аккумулятор', 'value': '24/240', 'measure': 'В/Ач'}

    def test_parser_characteristics12(self):
        text = "Габаритный размер 1200х700х1120 мм"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Габаритный размер', 'value': '1200х700х1120', 'measure': 'мм'}

    def test_parser_characteristics13(self):
        text = "Скорость передвижения с грузом без груза 5.8/6 км/ч"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Скорость передвижения грузом без груза', 'value': '5.8/6',
                                                  'measure': 'км/ч'}


    def test_parser_characteristics14(self):
        text = "при диаметр 30 мм на 80 % больше"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Диаметр', 'value': 30, 'measure': 'мм'}

    def test_parser_characteristics15(self):
        text = "Температура перекачиваемой воды от +1 до +40 С"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Температура перекачиваемой воды', 'value': 'от +1 до +40', 'measure': '°C'}

    def test_parser_characteristics16(self):
        text = "экономный расход клеевого состава от 70 до 240 грамм на квадратный метр"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Экономный расход клеевого состава', 'value': 'от 70 до 240', 'measure': 'г/м2'}

    def test_parser_characteristics17(self):
        text = "экономный расход клеевого состава от 70 до 240 грамм в час"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Экономный расход клеевого состава', 'value': 'от 70 до 240', 'measure': 'г/ч'}

    def test_parser_characteristics18(self):
        text = "Крановые от 1.4 до 22 кВт"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Крановый', 'value': 'от 1.4 до 22', 'measure': 'кВт'}

    def test_parser_characteristics19(self):
        text = "Крановые от 14 до 2.2 кВт"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Крановый', 'value': 'от 14 до 2.2', 'measure': 'кВт'}

    def test_parser_characteristics20(self):
        text = "Производительностью 15куб.м./час"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Производительность', 'value': 15, 'measure': 'м3/ч'}

    def test_parser_characteristics21(self):
        text = "Объем 3.7 м. куб"
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Объём', 'value': 3.7, 'measure': 'м3'}

    def test_parser_characteristics22(self):
        text = "Точность позиционирования ± 0.3 мм "
        parser_file = parser_characteristics.findall(text)
        assert self.get_dict_result(parser_file) == {'name': 'Точность позиционирования', 'value': '± 0.3', 'measure': 'мм'}
if __name__ == '__main__':
    unittest.main()