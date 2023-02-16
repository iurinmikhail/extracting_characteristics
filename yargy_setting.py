import re
import pymorphy2
from yargy.record import Record
from yargy import rule, Parser, or_
from yargy.predicates import eq, type, in_, gram
from yargy.pipelines import morph_pipeline
from yargy.interpretation import fact
import mysql_command as mysql

morph = pymorphy2.MorphAnalyzer()


def extract_measures_base_from_database() -> list:
    """Формирует список (из базы данных) единиц измерения для проверки measures
    """
    query = f'SELECT name_measure FROM measures_base;'
    db = mysql.CommandMySQL()
    texts = db.execute_read_query(query)
    measures_base = [''.join(i) for i in texts]
    return measures_base


measures_name = extract_measures_base_from_database()


class Synonyms(Record):
    __attributes__ = ['name', 'synonyms']

    def __init__(self, name, synonyms=()):
        self.name = name
        self.synonyms = synonyms


Characteristics = fact(
    'Characteristics',
    ['core', 'name', 'value', 'measure']
)

Measures = fact(
    'Measures',
    ['measure']
)

Values = fact(
    'Value',
    ['value']
)
# Добавление синонимов.
# Например: Synonyms('атм', ['Ат', 'атмосфер']) Заменит 'Ат' и'атмосфер' на 'атм'
name_synonyms = [
    Synonyms('м/ч', ['м час']),
    Synonyms('т/ч', ['тонн час']),
    Synonyms('атм', ['Ат', 'атмосфер']),
    Synonyms('мин.', ['минут', 'минуту']),
    Synonyms('кг', ['кил', 'кил', 'к/г', 'кгг', 'kg', 'килограмм', 'Кг']),
    Synonyms('Вт', ['втв', 'вт3', 'ввт', 'Ватт', 'ватт', 'W']),
    Synonyms('г', ['гр', 'грамм']),
    Synonyms('град', ['гра', 'градусов']),
    Synonyms('Гц', ['Герц']),
    Synonyms('дюйм', ['дюйма']),
    Synonyms('кВт', ['квтв',  'КВт']),
    Synonyms('л', ['литро', 'литров', 'литр']),
    Synonyms('л/мин', ['л/миин', 'л/ми', 'л.мин']),
    Synonyms('м', ['m', 'м\'', 'м«', 'метра', 'метр', 'метров']),
    Synonyms('м/мин', ['м/минн', 'm/мин', 'м?/ми']),
    Synonyms('м3', ['m3', 'м.куб.', 'метров кубический', 'куб.м.', 'м. куб']),
    Synonyms('м3/ч', ['м3/ча']),
    Synonyms('мл', ['миллили']),
    Synonyms('мм', ['мили', 'ммм', 'mm', 'миллим', 'ммвн', 'мил', 'ммили', 'милим', 'млм', 'мm', 'миллиметров', 'Мм']),
    Synonyms('мм/мин', ['мм/ми']),
    Synonyms('мм2', ['mm2']),
    Synonyms('м2', ['m2', 'квадратный метр', 'кв.м', 'квм']),
    Synonyms('об/сек', ['o/s']),
    Synonyms('об/мин', ['об/ми', 'о/мин', 'Об/мин']),
    Synonyms('руб.', ['руб', 'рулей', 'рублей']),
    Synonyms('см', ['cm', 'сантиметр']),
    Synonyms('см2', ['cm2']),
    Synonyms('т', ['тн', 'тонн»', 'тонн', 'тонны']),
    Synonyms('шт', ['ш', 'штук']),
    Synonyms('ч', ['час']),
    Synonyms('°C', ['градус цельсия', 'C', 'С', '0С']),
    Synonyms('В', ['вольт', 'v', 'V']),
    Synonyms('год выпуска', ['г.в']),
    Synonyms('кг/ч', ['кг пара час.']),
    Synonyms('кВА', ['ква', 'кВа']),
    Synonyms('МВт', ['мвт']),
    Synonyms('циклов/мин', ['циклов мин']),
    Synonyms('дней', ['к.д.']),
    Synonyms(','.join(measures_name))
]

names = []
mapping = {}
for record in name_synonyms:
    name = record.name
    names.append(name)
    mapping[name] = name
    for synonym in record.synonyms:
        names.append(synonym)
        mapping[synonym] = name

NAME_SYNONYMS = morph_pipeline(names)
NAME = morph_pipeline(measures_name)


def split_text(text):
    """Разделяет единицы измерения
    """
    return re.split(r"\sна\s|\sв\s|/", text)


def replaces_particles(text):
    """Заменяет предлог на "/"Например: кг в см, заменяет на кг/см
    """
    replaces_text = []
    words_list = split_text(text)
    for word in words_list:
        if word in mapping:
            replaces_text.append(mapping.get(word))
        else:
            replaces_text.append(word)
    text_replaces = '/'.join(replaces_text)
    return text_replaces if text_replaces != '/' else None


NAMES = or_(
    rule(
        NAME_SYNONYMS,
        or_(eq('в'), eq('на')),
        NAME_SYNONYMS
    ).interpretation(
        Characteristics.measure.custom(replaces_particles)
    ),
    rule(
        NAME, or_(eq('в'), eq('на')), NAME
    ).interpretation(
        Characteristics.measure.custom(replaces_particles)
    ),
    rule(
        NAME
    ).interpretation(
        Characteristics.measure.custom(replaces_particles)
    )
)

UNIT = or_(
    rule(
        NAMES
    ),
    rule(
        NAMES, eq('.').optional()
    ),
    rule(
        or_(eq('('), eq('[')).optional(), NAMES, or_(eq(')'), eq(']')).optional()
    )
)

INT = type('INT')

DIGIT = rule(INT).interpretation(
    Characteristics.value.custom(int)
)

FLOAT = rule(
    INT,
    in_(",."),
    INT
).interpretation(
    Characteristics.value.custom(lambda _: float(_.replace(' ', '').replace(',', '.')))
)

RANGE = or_(
    rule(
        or_(eq("более"), eq("от")), in_("—-+±").optional(),
        INT,
        or_(eq('менее'), eq('до')), in_("—-+±").optional(),
        INT
    ),
    rule(
        or_(eq("более"), eq("от")), in_("-—+±").optional(),
        INT, in_(".,"), INT,
        or_(eq('менее'), eq('до')), in_("-—+±").optional(),
        INT
    ),
    rule(
        or_(eq("более"), eq("от")), in_("-—+±").optional(),
        INT,
        or_(eq('менее'), eq('до')), in_("-—+±").optional(),
        INT, in_(".,"), INT
    ),
    rule(
        INT, in_("+— –-х×xX/"), INT
    ),
    rule(
        INT, in_(".,"), INT,
        in_("+–— -×xX/"),
        INT, in_(".,"), INT,
    ),
    rule(
        eq("от"),
        INT, in_(".,"), INT,
        eq('до'),
        INT, in_(".,"), INT,
    ),
    rule(
        or_(eq("от"), eq("до"), eq("более"), eq('менее'), eq("минус"), eq('±'), eq('плюс'), eq('+'), eq('-')),
        INT
    ),
    rule(
        or_(eq("от"), eq("до"), eq("более"), eq('менее'), eq("минус"), eq('±'), eq('плюс'), eq('+'), eq('-')),
        INT, in_(".,"), INT
    )

).interpretation(
    Characteristics.value.custom(lambda _: _.replace(',', '.'))
)

DUBLE_INT = rule(
    INT,
    INT
).interpretation(
    Characteristics.value.custom(lambda _: _.split()[1])
)

FRACTION_INT_3 = rule(
    INT,
    in_("+–—/-×хxxX "),
    INT,
    in_("–—/-×xхxX ").optional(),
    INT
).interpretation(
    Characteristics.value.custom(lambda _: _.replace(',', '.'))
)

FRACTION_INT_4 = rule(
    INT,
    in_("+–—/-×хxxX "),
    INT,
    in_("–—/-×xхxX ").optional(),
    INT,
    in_("–/—-×xхxX ").optional(),
    INT
).interpretation(
    Characteristics.value.custom(lambda _: _.replace(',', '.'))
)

FRACTION_INT_FLOAT = or_(
    rule(
    INT,
    in_("–—+/-×хxxX "),
    INT, in_(".,"), INT
),
    rule(
    INT, in_(".,"), INT,
    in_("–—+/-×хxxX "),
    INT
)
).interpretation(
    Characteristics.value.custom(lambda _: _.replace(',', '.'))
)


def parser_fraction_float(value):
    """Между числами ставит "/" """
    a, b, c = value.split('/')
    return f"{a}/{b}/{c}"


FRACTION_FLOAT = rule(
    INT, in_(',.'), INT,
    in_("/-—–×хxxX"),
    INT, in_(',.'), INT,
    in_("/-—–×xхxX").optional(),
    INT, in_(',.'), INT
).interpretation(
    Characteristics.value.custom(lambda _: _.replace(' ', '').replace(',', '.'))
)

VALUE = or_(
    DIGIT,
    FLOAT,
    RANGE,
    FRACTION_INT_3,
    FRACTION_INT_4,
    FRACTION_FLOAT,
    FRACTION_INT_FLOAT
).interpretation(Values.value)

SEP_MEASURE = in_(':)\n= -')

MEASURE = or_(
    rule(
        VALUE.interpretation(Characteristics.value),
        SEP_MEASURE.optional(),
        UNIT
    ),
    rule(
        UNIT,
        SEP_MEASURE.optional(),
        VALUE.interpretation(Characteristics.value)
    )
).interpretation(
    Characteristics
)

NOUN = gram('NOUN')
ADJF = gram('ADJF')
PREP = gram('PREP')
PRTF = gram('PRTF')  # частица
PRTS = gram('PRTS')
VERB = gram('VERB')


def clean_prtf(text: str) -> str:
    text = re.sub(r'[Пп]ри\s(?=\w+)', "", text)
    return re.sub('(\A[а-яА-Я]) (.*)', r'\2', text)


def clean_product(text):
    """Очищает наименование от слов меньше двух букв, от стоп-слов,
    приводит в нормальную форму одно слово. Делает наименование с большой буквы
    """
    if len(text) <= 2:
        return None
    clean_text = []
    for word in text.split():
        if word.lower() not in measures_name and word.lower() not in names:
            clean_text.append(word)
    text_cleared_of_measures = ' '.join(clean_text)
    text_clean = clean_prtf(text_cleared_of_measures)
    if text_clean:
        if len(text_clean.split()) == 1:
            word = morph.parse(text_clean)[0]
            word_normal = word.normal_form
            return word_normal.capitalize()
        return text_clean.capitalize()
    return None

PRODUCT = or_(
    rule(VERB, PREP.optional(), NOUN, PREP.optional(), NOUN, PREP.optional()),
    rule(NOUN.repeatable(), PREP.optional(), PRTS.optional(), PREP.optional(), NOUN.repeatable()),
    rule(PRTF.optional(), PREP.optional(), ADJF.repeatable().optional(), PREP.optional(), PRTF.optional(),
         PREP.optional(),
         NOUN.repeatable(), PREP.optional(), PRTF.optional(), PREP.optional(), ADJF.optional(), PREP.optional(),
         NOUN.optional(), PREP.optional(), ADJF.optional(), PREP.optional(), NOUN.repeatable()),
    rule(ADJF.optional(), PREP.optional(), NOUN.repeatable(), PREP.optional(), ADJF.optional(), PREP.optional(), ),
    rule(ADJF.repeatable().optional(), PREP.optional(), NOUN.repeatable(), PREP.optional()),
    rule(NOUN.repeatable(), VERB),
    rule(ADJF),
    rule(PRTF, PREP.optional(), NOUN)
).interpretation(
    Characteristics.name.custom(clean_product)
)

SEP = in_('-:,.–')


CHARACTERISTICS = or_(
    rule(
        PRODUCT,
        MEASURE
    ),
    rule(
        PRODUCT,
        SEP.optional(),
        MEASURE),
    rule(
        PRODUCT,
        SEP.optional(),
        MEASURE,
        SEP.optional(),
        MEASURE
    )
).interpretation(Characteristics)

parser_characteristics = Parser(CHARACTERISTICS)
parser_measure_and_value = Parser(MEASURE)

parser_value = Parser(VALUE)

