import unittest
from create_card_modeles import *


class TestStringMethods(unittest.TestCase):
    @staticmethod
    def main_create_card_modeles(A):
        card_core = comparison_core(A)
        card_name_value_measure = get_name_value_measure(card_core)
        return card_name_value_measure

    def test_comparison_core1(self):
        """
        Нет отличий core и value выведи одно
        """
        text = [{
            "core": "напряжение",
            "core_nmod0": "двигатель",
            "core_amod0": "Максимальное",
            "name": "Максимальное напряжение двигателя",
            "value": "240",
            "measure": "В",
            "weight": 1
        },
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Максимальное",
                "name": "Максимальное напряжение двигателя",
                "value": "240",
                "measure": "В", "weight": 1
            }]
        assert comparison_core(text) == [{
            "core": "напряжение",
            "core_nmod0": "двигатель",
            "core_amod0": "Максимальное",
            "name": "Максимальное напряжение двигателя",
            "value": "240",
            "measure": "В", "weight": 1
        }]

    def test_comparison_core2(self):
        """
        Если core динаковый, value разный и amod разный, то выведи оба
        """
        text = [
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Максимальное",
                "name": "Максимальное напряжение двигателя",
                "value": "240",
                "measure": "В", "weight": 1
            },
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Минимальный",
                "name": "Минимальное напряжение двигателя",
                "value": "200",
                "measure": "В", "weight": 1
            }
        ]
        assert sorted(comparison_core(text), key=lambda x: x['name']) == sorted([
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Максимальное",
                "name": "Максимальное напряжение двигателя",
                "value": "240",
                "measure": "В", "weight": 1
            },
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Минимальный",
                "name": "Минимальное напряжение двигателя",
                "value": "200",
                "measure": "В", "weight": 1
            }
        ], key=lambda x: x['name'])

    def test_comparison_core3(self):
        """
        Если core одинаковый
        """
        text = [{
            "core": "напряжение",
            "core_nmod0": "двигатель",
            "core_amod0": "Минимальный",
            "name": "Минимальное напряжение двигателя",
            "value": "240",
            "measure": "В", "weight": 1
        },
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Минимальный",
                "name": "Минимальное напряжение двигателя",
                "value": "200",
                "measure": "В", "weight": 1
            },
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Минимальный",
                "name": "Минимальное напряжение двигателя",
                "value": "240",
                "measure": "В", "weight": 1
            },
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Минимальный",
                "name": "Минимальное напряжение двигателя",
                "value": "230",
                "measure": "В", "weight": 1
            }]
        assert comparison_core(text) == [{
            "core": "напряжение",
            "core_nmod0": "двигатель",
            "core_amod0": "Минимальный",
            "name": "Минимальное напряжение двигателя",
            "value": "240",
            "measure": "В", "weight": 1
        }]

    def test_comparison_core4(self):
        text = [{
            "core": "ток",
            "core_nmod0": "двигатель",
            "core_amod0": "Минимальный",
            "name": "Минимальное ток двигателя",
            "value": "240",
            "measure": "А", "weight": 1
        },
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Минимальный",
                "name": "Минимальное напряжение двигателя",
                "value": "200",
                "measure": "В", "weight": 1
            },
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Минимальный",
                "name": "Минимальное напряжение двигателя",
                "value": "240",
                "measure": "В", "weight": 1
            },
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Минимальный",
                "name": "Минимальное напряжение двигателя",
                "value": "200",
                "measure": "В", "weight": 1
            }]
        assert sorted(comparison_core(text), key=lambda x: x['core']) == sorted([
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Минимальный",
                "name": "Минимальное напряжение двигателя",
                "value": "200",
                "measure": "В", "weight": 1
            },
            {
                "core": "ток",
                "core_nmod0": "двигатель",
                "core_amod0": "Минимальный",
                "name": "Минимальное ток двигателя",
                "value": "240",
                "measure": "А", "weight": 1
            }
        ], key=lambda x: x['core'])

    def test_comparison_core5(self):
        text = [
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Минимальный",
                "name": "Минимальное напряжение двигателя",
                "value": "240",
                "measure": "В", "weight": 1
            },
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "name": "напряжение двигателя",
                "value": "230",
                "measure": "В", "weight": 1
            }]
        sorted(comparison_core(text), key=lambda x: x['core']) == sorted([
            {
                'core': 'напряжение',
                'core_nmod0': 'двигатель',
                'core_amod0': 'Минимальный',
                'name': 'Минимальное напряжение двигателя',
                'value': '240', 'measure': 'В', "weight": 1
            },
            {
                'core': 'напряжение',
                'core_nmod0': 'двигатель',
                'name': 'напряжение двигателя',
                'value': '230', 'measure': 'В', "weight": 1
            }
        ], key=lambda x: x['core'])

    def test_comparison_core6(self):
        text = [
            {
                'core': 'core4',
                'name': 'core4',
                'value': 8,
                'measure': 'м', "weight": 1
            },
            {
                'core': 'core5',
                'name': 'core5',
                'value': 35,
                'measure': '%', "weight": 1
            },
            {
                'core': 'core2',
                'name': 'core2',
                'value': '1.0–4.0', 'measure': 'мм', "weight": 1
            },
            {
                'core': 'core5',
                'name': 'core5',
                'value': 8, 'measure': 'м', "weight": 1
            },
            {
                'core': 'core5',
                'name': 'core5',
                'value': 35,
                'measure': '%', "weight": 1
            },
            {
                'core': 'core3',
                'name': 'core3',
                'value': 8,
                'measure': 'м', "weight": 1
            },
            {
                'core': 'core2',
                'name': 'core2',
                'value': '1.0–4.0',
                'measure': 'мм', "weight": 1
            },
            {
                'core': 'core2',
                'name': 'core2',
                'value': '1.0–4.0',
                'measure': 'мм', "weight": 1
            },
            {
                'core': 'core4',
                'name': 'core4',
                'value': 8,
                'measure': 'м', "weight": 1
            },
            {
                'core': 'core1',
                'name': 'core1',
                'value': 8,
                'measure': 'м', "weight": 1
            },
        ]

        assert sorted(comparison_core(text), key=lambda x: x['core']) == sorted(
            [{'core': 'core1', 'name': 'core1', 'value': 8, 'measure': 'м', "weight": 1},
             {'core': 'core2', 'name': 'core2', 'value': '1.0–4.0', 'measure': 'мм', "weight": 1},
             {'core': 'core3', 'name': 'core3', 'value': 8, 'measure': 'м', "weight": 1},
             {'core': 'core4', 'name': 'core4', 'value': 8, 'measure': 'м', "weight": 1},
             {'core': 'core5', 'name': 'core5', 'value': 35, 'measure': '%', "weight": 1}], key=lambda x: x['core'])

    def test_comparison_core6_1(self):
        text = [
            {
                'core': 'core5',
                'name': 'core5',
                'value': 35,
                'measure': '%', "weight": 1
            },
            {
                'core': 'core5',
                'name': 'core5',
                'value': 8, 'measure': 'м', "weight": 1
            },
            {
                'core': 'core5',
                'name': 'core5',
                'value': 35,
                'measure': '%', "weight": 1
            },

        ]

        assert comparison_core(text) == [{
            'core': 'core5',
            'name': 'core5',
            'value': 35,
            'measure': '%', "weight": 1
        }]

    def test_comparison_core7(self):
        text = [{
            'core': 'вес',
            'name': 'Вес',
            'value': 15, 'measure': 'кг/м', "weight": 1
        }, {
            'core': 'давление',
            'core_amod0': 'максимальный',
            'name': 'Максимальное давление',
            'value': 60, 'measure': 'бар', "weight": 1
        }, {
            'core': 'длина',
            'name': 'Длина',
            'value': 15,
            'measure': 'м', "weight": 1
        }, {
            'core': 'диаметр',
            'core_amod0': 'внешний',
            'name': 'Внешний диаметр',
            'value': 16, 'measure': 'мм', "weight": 1
        }, {
            'core': 'диаметр',
            'core_amod0': 'внутренний',
            'name': 'Внутренний диаметр',
            'value': 10, 'measure': 'мм', "weight": 1
        }]
        assert sorted(comparison_core(text), key=lambda x: x['name']) == sorted(
            [{'core': 'вес', 'name': 'Вес', 'value': 15, 'measure': 'кг/м', "weight": 1},
             {'core': 'давление', 'core_amod0': 'максимальный', 'name': 'Максимальное давление', 'value': 60,
              'measure': 'бар', "weight": 1},
             {'core': 'длина', 'name': 'Длина', 'value': 15, 'measure': 'м', "weight": 1},
             {'core': 'диаметр', 'core_amod0': 'внешний', 'name': 'Внешний диаметр', 'value': 16, 'measure': 'мм',
              "weight": 1},
             {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Внутренний диаметр', 'value': 10,
              'measure': 'мм', "weight": 1}], key=lambda x: x['name'])

    def test_comparison_core8(self):
        text = [
            {'core': 'вес', 'name': 'Вес', 'value': 15, 'measure': 'кг/м', "weight": 1},
            {'core': 'давление', 'core_amod0': 'максимальный', 'name': 'Максимальное давление', 'value': 60,
             'measure': 'бар', "weight": 1},
            {'core': 'длина', 'name': 'Длина', 'value': 15, 'measure': 'м', "weight": 1},
            {'core': 'диаметр', 'core_amod0': 'внешний', 'name': 'Внешний диаметр', 'value': 16, 'measure': 'мм',
             "weight": 1},
            {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Внутренний диаметр', 'value': 10, 'measure': 'мм',
             "weight": 1},
            {'core': 'вес', 'name': 'Вес', 'value': 15, 'measure': 'кг/м', "weight": 1},
            {'core': 'давление', 'core_amod0': 'максимальный', 'name': 'Максимальное давление', 'value': 60,
             'measure': 'бар', "weight": 1},
            {'core': 'длина', 'name': 'Длина', 'value': 15, 'measure': 'м', "weight": 1},
            {'core': 'диаметр', 'core_amod0': 'внешний', 'name': 'Внешний диаметр', 'value': 16, 'measure': 'мм',
             "weight": 1},
            {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Внутренний диаметр', 'value': 10, 'measure': 'мм',
             "weight": 1},
            {'core': 'вес', 'name': 'Вес', 'value': 15, 'measure': 'кг/м', "weight": 1},
            {'core': 'давление', 'core_amod0': 'максимальный', 'name': 'Максимальное давление', 'value': 60,
             'measure': 'бар', "weight": 1},
            {'core': 'длина', 'name': 'Длина', 'value': 15, 'measure': 'м', "weight": 1},
            {'core': 'диаметр', 'core_amod0': 'внешний', 'name': 'Внешний диаметр', 'value': 16, 'measure': 'мм',
             "weight": 1},
            {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Внутренний диаметр', 'value': 10, 'measure': 'мм',
             "weight": 1}]

        assert sorted(comparison_core(text), key=lambda x: x['name']) == sorted(
            [
                {
                    'core': 'диаметр',
                    'core_amod0': 'внешний',
                    'name': 'Внешний диаметр',
                    'value': 16,
                    'measure': 'мм', "weight": 1
                },
                {
                    'core': 'диаметр',
                    'core_amod0': 'внутренний',
                    'name': 'Внутренний диаметр',
                    'value': 10,
                    'measure': 'мм', "weight": 1
                },
                {
                    'core': 'давление',
                    'core_amod0': 'максимальный',
                    'name': 'Максимальное давление',
                    'value': 60,
                    'measure': 'бар', "weight": 1
                },
                {
                    'core': 'вес',
                    'name': 'Вес',
                    'value': 15,
                    'measure': 'кг/м', "weight": 1
                },
                {
                    'core': 'длина',
                    'name': 'Длина',
                    'value': 15,
                    'measure': 'м', "weight": 1
                }
            ], key=lambda x: x['name'])

    def test_comparison_core9_1(self):
        text = [
            {
                'core': 'core5',
                'core_nmod0': 'nmod1',
                'name': 'core5',
                'value': 35,
                'measure': '%', "weight": 1
            },
            {
                'core': 'core5',
                'core_nmod0': 'nmod2',
                'name': 'core5',
                'value': 8, 'measure': 'м', "weight": 1
            },
            {
                'core': 'core5',
                'core_nmod0': 'nmod1',
                'name': 'core5',
                'value': 35,
                'measure': '%', "weight": 1
            }
        ]

        assert sorted(comparison_core(text), key=lambda x: x['core_nmod0']) == sorted(
            [{'core': 'core5', 'core_nmod0': 'nmod2', 'name': 'core5', 'value': 8, 'measure': 'м', "weight": 1},
             {'core': 'core5', 'core_nmod0': 'nmod1', 'name': 'core5', 'value': 35, 'measure': '%', "weight": 1}
             ], key=lambda x: x['core_nmod0'])

    def test_comparison_core9(self):
        text = [
            {'core': 'габарит',
             'core_nmod0': 'редуктор',
             'core_nmod1': 'вид',
             'name': 'Габариты редуктора собранном виде',
             'value': '260х195х56',
             'measure': 'мм', "weight": 1
             },
            {
                'core': 'габарит',
                'core_nmod0': 'упаковка',
                'core_nmod_amod0': 'индивидуальный',
                'name': 'Габариты индивидуальной упаковки',
                'value': '185х200х60', 'measure': 'мм', "weight": 1
            },
            {
                'core': 'вес',
                'core_nmod0': 'нетто',
                'name': 'Вес нетто',
                'value': 1.46,
                'measure': 'кг', "weight": 1
            },
            {
                'core': 'вес',
                'core_nmod0': 'брутто',
                'name': 'Вес брутто',
                'value': 1.52,
                'measure': 'кг', "weight": 1
            },
            {
                'core': 'винт',
                'core_nmod0': 'крепление',
                'core_nmod_amod0': 'прижимный',
                'name': 'Винт крепления прижимной',
                'value': '10х1,5',
                'measure': 'M', "weight": 1
            },
            {
                'core': 'винт',
                'core_nmod0': 'крепление',
                'core_nmod_amod0': 'прижимный',
                'name': 'Винт крепления прижимной',
                'value': '10х1,5', 'measure': 'M', "weight": 1
            },
            {
                'core': 'вес',
                'core_nmod0': 'нетто',
                'name': 'Вес нетто',
                'value': 1.46,
                'measure': 'кг', "weight": 1
            },
            {
                'core': 'габарит',
                'core_nmod0': 'редуктор',
                'core_nmod1': 'вид',
                'name': 'Габариты редуктора собранном виде',
                'value': '260х195х56',
                'measure': 'мм', "weight": 1
            },
            {
                'core': 'вес',
                'core_nmod0': 'брутто',
                'name': 'Вес брутто',
                'value': 1.52,
                'measure': 'кг', "weight": 1
            },
            {
                'core': 'габарит',
                'core_nmod0': 'упаковка',
                'core_nmod_amod0': 'индивидуальный',
                'name': 'Габариты индивидуальной упаковки',
                'value': '185х200х60',
                'measure': 'мм', "weight": 1
            }
        ]
        assert len(sorted(comparison_core(text), key=lambda x: x['name'])) == len(sorted(
            [{'core': 'вес', 'core_nmod0': 'брутто', 'name': 'Вес брутто', 'value': 1.52, 'measure': 'кг', "weight": 1},
             {'core': 'вес', 'core_nmod0': 'нетто', 'name': 'Вес нетто', 'value': 1.46, 'measure': 'кг', "weight": 1},
             {'core': 'винт', 'core_nmod0': 'крепление', 'core_nmod_amod0': 'прижимный',
              'name': 'Винт крепления прижимной', 'value': '10х1,5', 'measure': 'M', "weight": 1},
             {'core': 'габарит', 'core_nmod0': 'упаковка', 'core_nmod_amod0': 'индивидуальный',
              'name': 'Габариты индивидуальной упаковки', 'value': '185х200х60', 'measure': 'мм', "weight": 1},
             {'core': 'габарит', 'core_nmod0': 'редуктор', 'core_nmod1': 'вид',
              'name': 'Габариты редуктора собранном виде', 'value': '260х195х56', 'measure': 'мм', "weight": 1}]
            , key=lambda x: x['name']))

    def test_comparison_core10(self):
        text = [
            {
                'core': 'январь',
                'name': 'января',
                'value': 2022,
                'measure': 'года', "weight": 1
            },
            {
                'core': 'трчп',
                'core_amod0': 'передвижной',
                'name': 'ручная червячная передвижная ТРЧП',
                'value': 10.0,
                'measure': 'т', "weight": 1
            },
            {
                'core': 'трчп',
                'name': 'ТРЧП',
                'value': 9,
                'measure': 'м', "weight": 1
            },
            {
                'core': 'трчп',
                'core_amod0': 'передвижной',
                'name': 'ручная червячная передвижная ТРЧП',
                'value': 6,
                'measure': 'м', "weight": 1
            }
        ]
        assert sorted(comparison_core(text), key=lambda x: x['name']) == sorted([{'core': 'трчп',
                                                                                  'core_amod0': 'передвижной',
                                                                                  'name': 'ручная червячная передвижная ТРЧП',
                                                                                  'value': 10.0, 'measure': 'т',
                                                                                  "weight": 1},
                                                                                 {'core': 'январь', 'name': 'января',
                                                                                  'value': 2022, 'measure': 'года',
                                                                                  "weight": 1},
                                                                                 {'core': 'трчп', 'name': 'ТРЧП',
                                                                                  'value': 9, 'measure': 'м',
                                                                                  "weight": 1}],
                                                                                key=lambda x: x['name'])

    def test_comparison_core11(self):
        text = [{'core': 'диаметр', 'core_amod0': 'внешний', 'name': 'Внешний диаметр', 'value': 16, 'measure': 'мм',
                 "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Внутренний диаметр', 'value': 25.6,
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Внутренний диаметр', 'value': 7.8,
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Внутренний диаметр', 'value': 32,
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Внутренний диаметр', 'value': 'от 50 до 600',
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Внутренний диаметр', 'value': 11.2,
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Внутренний диаметр', 'value': 10,
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Внутренний диаметр от', 'value': 'до 400',
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'core_nmod0': 'рукав',
                 'name': 'Внутренний диаметр рукава', 'value': 150, 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'core_nmod0': 'шланг',
                 'name': 'Внутренний диаметр шланга', 'value': 8, 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'core_nmod0': 'шланг',
                 'name': 'Внутренний диаметр шланга', 'value': 18, 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'core_nmod0': 'шланг',
                 'name': 'Внутренний диаметр шланга', 'value': 32, 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'core_nmod0': 'шланг',
                 'name': 'Внутренний диаметр шланга', 'value': 16, 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Диаметр внутренний', 'value': 63,
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Диаметр внутренний', 'value': 30,
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'внутренний', 'name': 'Диаметр внутренний', 'value': 32,
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'наружный', 'name': 'Наружный диаметр', 'value': 11.6,
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'наружный', 'name': 'Наружный диаметр', 'value': 16, 'measure': 'мм',
                 "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'наружный', 'name': 'Наружный диаметр', 'value': 31.6,
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'наружный', 'core_nmod0': 'шланг', 'name': 'Наружный диаметр шланга',
                 'value': 24, 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'наружный', 'core_nmod0': 'шланг', 'name': 'Наружный диаметр шланга',
                 'value': 40, 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'наружный', 'core_nmod0': 'шланг', 'name': 'Наружный диаметр шланга',
                 'value': 23, 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'наружный', 'core_nmod0': 'шланг', 'name': 'Наружный диаметр шланга',
                 'value': 14, 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'номинальный', 'name': 'Номинальный диаметр', 'value': 8,
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'номинальный', 'name': 'Номинальный диаметр', 'value': 12,
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'номинальный', 'name': 'Номинальный диаметр', 'value': 25,
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'резиновый', 'name': 'Рукава резиновые диаметром', 'value': 'до 13',
                 'measure': 'мм', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'наружный', 'name': 'наружный диаметр', 'value': 41, 'measure': 'мм',
                 "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'наружный', 'name': 'наружный диаметр', 'value': 163,
                 'measure': 'мм', "weight": 1}]
        stack = []

        assert len([i for i in sorted(comparison_core(text), key=lambda x: x['name']) if i['core'] == 'диаметр']) == 5

    def test_comparison_core12(self):
        text = [{'core': 'длина', 'name': 'Длина', 'value': 460, 'measure': 'мм', "weight": 1},
                {'core': 'джет', 'name': 'Джет Р', 'value': 1, 'measure': 'А', "weight": 1},
                {'core': 'габарит', 'name': 'Габариты', 'value': '460х150х70', 'measure': 'мм', "weight": 1},
                {'core': 'вес', 'name': 'Вес', 'value': 0.75, 'measure': 'кг', "weight": 1},
                {'core': 'толщина', 'core_nmod0': 'рез', 'name': 'Толщина реза', 'value': 100, 'measure': 'мм',
                 "weight": 1},
                {'core': 'толщина', 'core_nmod0': 'рез', 'name': 'Толщина реза', 'value': 'до 100', 'measure': 'мм',
                 "weight": 1},
                {'core': 'толщина', 'name': 'Толщина', 'value': 100, 'measure': 'мм', "weight": 1}] + [
                   {'core': 'длина', 'name': 'Длина', 'value': 460, 'measure': 'мм', "weight": 1},
                   {'core': 'джет', 'name': 'Джет Р', 'value': 1, 'measure': 'А', "weight": 1},
                   {'core': 'габарит', 'name': 'Габариты', 'value': '460х150х70', 'measure': 'мм', "weight": 1},
                   {'core': 'вес', 'name': 'Вес', 'value': 0.75, 'measure': 'кг', "weight": 1},
                   {'core': 'толщина', 'core_nmod0': 'рез', 'name': 'Толщина реза', 'value': 100, 'measure': 'мм',
                    "weight": 1},
                   {'core': 'толщина', 'core_nmod0': 'рез', 'name': 'Толщина реза', 'value': 'до 100', 'measure': 'мм',
                    "weight": 1},
                   {'core': 'толщина', 'name': 'Толщина', 'value': 100, 'measure': 'мм', "weight": 1}]

        assert len([i for i in sorted(comparison_core(text), key=lambda x: x['name']) if i['core'] == 'толщина']) == 2

    def test_comparison_core13(self):
        text = [{
            "core": "мощность",
            "name": "Мощность",
            "value": 3,
            "measure": "кВт",
            "weight": 3
        },
            {
                "core": "мощность",
                "name": "Мощность",
                "value": 1,
                "measure": "А",
                "weight": 1
            },
            {
                "core": "мощность",
                "name": "Мощность",
                "value": 1,
                "measure": "А",
                "weight": 1
            }
        ]

        assert sorted(comparison_core(text), key=lambda x: x['name']) == [{'core': 'мощность', 'name': 'Мощность', 'value': 3, 'measure': 'кВт', 'weight': 3}]

    def test_comparison_core14(self):
        text = [
            {
                'core': 'core5',
                'name': 'core5',
                'value': 35,
                'measure': '%', "weight": 1
            },
            {
                'core': 'core5',
                'name': 'core5',
                'value': 40, 'measure': '%', "weight": 3
            },
            {
                'core': 'core5',
                'name': 'core5',
                'value': 35,
                'measure': '%', "weight": 1
            }
        ]

        assert comparison_core(text) == [{'core': 'core5', 'name': 'core5', 'value': 40, 'measure': '%', 'weight': 3}]

    def test_comparison_core15(self):
        text = [
            {
                'core': 'core5',
                'name': 'core5',
                'value': 35,
                'measure': '%', "weight": 1
            },
            {
                'core': 'core5',
                'core_amod0': 'core5',
                'name': 'core5',
                'value': 40, 'measure': '%', "weight": 3
            },
            {
                'core': 'core5',
                'core_nmod0': 'core5',
                'name': 'core5',
                'value': 50,
                'measure': '%', "weight": 1
            }
        ]

        assert comparison_core(text) == [{'core': 'core5', 'core_amod0': 'core5', 'name': 'core5', 'value': 40, 'measure': '%', 'weight': 3}, {'core': 'core5', 'core_nmod0': 'core5', 'name': 'core5', 'value': 50, 'measure': '%', 'weight': 1}, {'core': 'core5', 'name': 'core5', 'value': 35, 'measure': '%', 'weight': 1}]

    def test_comparison_core16(self):
        text = [
        {
            "core": "производительность",
            "name": "Производительность",
            "value": "0,5 – 4,8 1,1",
            "measure": "м3/час",
            "weight": 1
        },
            {
            "core": "производительность",
            "core_amod0": "максимальный",
            "name": "Максимальная производительность",
            "value": 300,
            "measure": "л/мин",
            "weight": 1
        },
        {
            "core": "производительность",
            "name": "Производительность",
            "value": 300,
            "measure": "л.мин",
            "weight": 3
        },
            {
                "core": "производительность",
                "core_amod0": "максимальный",
                "name": "Максимальная производительность",
                "value": 300,
                "measure": "л/мин",
                "weight": 1
            }
        ]

        assert comparison_core(text) == [{'core': 'производительность', 'core_amod0': 'максимальный', 'name': 'Максимальная производительность', 'value': 300, 'measure': 'л/мин', 'weight': 1}, {'core': 'производительность', 'name': 'Производительность', 'value': '0,5 – 4,8 1,1', 'measure': 'м3/час', 'weight': 1}]


    def test_get_name_value_measure1(self):
        """
        Проверка преобразования нескольких характеристик в списке в словарь без core
        """
        text = [{
            "core": "напряжение",
            "core_nmod0": "двигатель",
            "core_amod0": "Максимальное",
            "name": "Максимальное напряжение двигателя",
            "value": "240",
            "measure": "В", "weight": 1
        },
            {
                "core": "напряжение",
                "core_nmod0": "двигатель",
                "core_amod0": "Максимальное",
                "name": "Максимальное напряжение двигателя",
                "value": "240",
                "measure": "В", "weight": 1
            }]
        assert get_name_value_measure(text) == [
            {
                'name': 'Максимальное напряжение двигателя',
                'value': '240',
                'measure': 'В'
            },
            {
                'name': 'Максимальное напряжение двигателя',
                'value': '240',
                'measure': 'В'
            }
        ]

    def test_get_name_value_measure2(self):
        """
        Преобразование характеристики без списка в список без core
        """
        text = {
            "core": "напряжение",
            "core_nmod0": "двигатель",
            "core_amod0": "Максимальное",
            "name": "Максимальное напряжение двигателя",
            "value": "240",
            "measure": "В", "weight": 1
        }
        assert get_name_value_measure(text) == [
            {'name': 'Максимальное напряжение двигателя', 'value': '240', 'measure': 'В'}]

    def test_max_count_values1(self):
        text = ['100', '200', '200']
        assert max_count_values(text) == '200'

    def test_max_count_values2(self):
        text = [100, '200', '200']
        assert max_count_values(text) == '200'

    def test_max_count_values3(self):
        text = ['100x100', '200', '200']
        assert max_count_values(text) == '200'

    def test_max_count_values4(self):
        text = ['100x100', '100 - 200', 'от 100 до 200']
        assert max_count_values(text) == '100x100'

    def test_main_create_card_modeles(self):
        text = [
            {
                'core': 'двигатель',
                'name': 'Двигатель',
                'value': 380,
                'measure': 'В', "weight": 1
            },
            {
                'core': 'диаметр',
                'core_amod0': 'максимальный',
                'core_nmod0': 'арматура', 'name': 'максимальный диаметр арматуры',
                'value': 1, 'measure': 'А', "weight": 1
            },
            {
                'core': 'вес',
                'name': 'Вес',
                'value': 520,
                'measure': 'кг', "weight": 1
            }
        ]
        assert sorted(self.main_create_card_modeles(text), key=lambda x: x['name']) == sorted([
            {
                'name': 'Вес',
                'value': 520,
                'measure': 'кг'
            },
            {
                'name': 'Двигатель',
                'value': 380,
                'measure': 'В'
            },
            {
                'name': 'максимальный диаметр арматуры',
                'value': 1,
                'measure': 'А'
            }
        ], key=lambda x: x['name'])

    def test_main_create_card_modeles2(self):
        text = [
            {
                'core': 'core4',
                'name': 'core4',
                'value': 8,
                'measure': 'м', "weight": 1
            },
            {
                'core': 'core1',
                'name': 'core1',
                'value': 35,
                'measure': '%', "weight": 1
            },
            {
                'core': 'core2',
                'name': 'core2',
                'value': '1.0–4.0', 'measure': 'мм', "weight": 1
            },
            {
                'core': 'core3',
                'name': 'core3',
                'value': 8, 'measure': 'м', "weight": 1
            },
            {
                'core': 'core3',
                'name': 'core3',
                'value': 8, 'measure': 'м', "weight": 1
            },
            {
                'core': 'core2',
                'name': 'core2',
                'value': '1.0–4.0',
                'measure': 'мм', "weight": 1
            }
        ]
        assert sorted([i['name'] for i in self.main_create_card_modeles(text)]) == sorted(
            ['core2', 'core3', 'core4', 'core1'])

    def test_main_create_card_modeles3(self):
        text = [{'core': 'двигатель', 'name': 'Двигатель', 'value': 380, 'measure': 'В', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'максимальный', 'core_nmod0': 'арматура',
                 'name': 'максимальный диаметр арматуры', 'value': 1, 'measure': 'А', "weight": 1},
                {'core': 'вес', 'name': 'Вес', 'value': 520, 'measure': 'кг', "weight": 1},
                {'core': 'двигатель', 'name': 'Двигатель', 'value': 380, 'measure': 'В', "weight": 1},
                {'core': 'диаметр', 'core_amod0': 'максимальный', 'core_nmod0': 'арматура',
                 'name': 'максимальный диаметр арматуры', 'value': 1, 'measure': 'А', "weight": 1},
                {'core': 'вес', 'name': 'Вес', 'value': 520, 'measure': 'кг', "weight": 1}]
        assert sorted(self.main_create_card_modeles(text), key=lambda x: x['name']) == sorted(
            [{'name': 'Вес', 'value': 520, 'measure': 'кг'},
             {'name': 'максимальный диаметр арматуры', 'value': 1, 'measure': 'А'},
             {'name': 'Двигатель', 'value': 380, 'measure': 'В'}], key=lambda x: x['name'])

    def test_clean_of_core_none(self):
        text = [{'core': None}, {'core': 'core'}]
        assert list(clean_of_core_none(text)) == [{'core': 'core'}]

    def test_search_values_wieght_and_count(self):
        values = ['A', 'B', 'B', 'C', 'C']
        wieght = [1, 2.5, 2.5, 1, 1]
        count = [values.count(i) for i in values]
        assert search_values_weight_and_count(values, wieght, count) == "B"

    def test_search_values_wieght_and_count2(self):
        values = ['A', 'B', 'C']
        wieght = [1, 1.5, 2.5]
        count = [values.count(i) for i in values]
        assert search_values_weight_and_count(values, wieght, count) == 'C'

    def test_search_values_wieght_and_count3(self):
        values = ['A', 'B', 'C']
        wieght = [1, 1, 2.5]
        count = [values.count(i) for i in values]
        assert search_values_weight_and_count(values, wieght, count) == 'C'

    def test_search_values_wieght_and_count4(self):
        values = ['A', 'B', 'C']
        wieght = [1, 1, 1]
        count = [values.count(i) for i in values]
        assert search_values_weight_and_count(values, wieght, count) == 'A'

    def test_search_values_wieght_and_count5(self):
        values = ['A', 'A', 'B', 'B', 'C']
        wieght = [2.5, 2.5, 2.5, 1]
        count = [values.count(i) for i in values]
        assert search_values_weight_and_count(values, wieght, count) == 'A'

    def test_search_values_wieght_and_count6(self):
        values = ['A', 'C', 'B']
        wieght = [1.5, 1, 1]
        count = [values.count(i) for i in values]
        assert search_values_weight_and_count(values, wieght, count) == 'A'

    def test_search_values_wieght_and_count7(self):
        values = ['A', 'C', 'B', 'D']
        wieght = [1.5, 1, 1, 1]
        count = [values.count(i) for i in values]
        assert search_values_weight_and_count(values, wieght, count) == 'A'

    def test_search_values_wieght_and_count8(self):
        values = ['A', 'C', 'C']
        wieght = [1.5, 1, 1]
        count = [values.count(i) for i in values]
        assert search_values_weight_and_count(values, wieght, count) == 'C'

    def test_search_values_wieght_and_count9(self):
        values = ['A', 'B', 'B', 'B']
        wieght = [1.5, 1, 1, 1]
        count = [values.count(i) for i in values]
        assert search_values_weight_and_count(values, wieght, count) == 'B'

    def test_search_values_wieght_and_count10(self):
        values = ['A', 'A', 'B', 'B']
        wieght = [1, 1, 1, 1]
        count = [values.count(i) for i in values]
        assert search_values_weight_and_count(values, wieght, count) == 'A'

    def test_search_values_wieght_and_count11(self):
        values = ['A', 'B', 'B']
        wieght = [2.5, 1.5, 1.5]
        count = [values.count(i) for i in values]
        assert search_values_weight_and_count(values, wieght, count) == 'B'

    def test_search_values_wieght_and_count12(self):
        values = ['A', 'B', 'B', 'B']
        wieght = [2.5, 1, 1, 1]
        count = [values.count(i) for i in values]
        assert search_values_weight_and_count(values, wieght, count) == 'B'