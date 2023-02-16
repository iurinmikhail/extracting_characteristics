"""Находит core из текста
"""

import json
import os

import pymorphy2
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    Doc
)

morph = pymorphy2.MorphAnalyzer()
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
syntax_parser = NewsSyntaxParser(emb)
morph_tagger = NewsMorphTagger(emb)


def extract_stop_words() -> set:
    """Извлекает список слов из файла txt. На выходе множество
    Для исключения попадания их в core
    """
    path_stop_words = 'sources/stop_words.txt'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conf_path = os.path.join(dir_path, path_stop_words)
    with open(conf_path, "r", encoding='utf-8') as file:
        texts = file.readlines()
    return set([i.strip() for i in texts])


stop_words = extract_stop_words()


def parse_dependency(text) -> list:
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    dependency = []
    for doc_token in doc.tokens:
        s = json.dumps(doc_token.__dict__, ensure_ascii=False)
        extract_json = json.loads(s)
        extract_json['id'] = extract_json['id'][-1]
        extract_json['head_id'] = extract_json['head_id'][-1]
        dependency.append(extract_json)
    return dependency


def extract_core_normal() -> set:
    """Извлекает список слов из файла txt. На выходе множество.
    Для первичного извлечения core
     """
    path_core_normal = 'sources/core_norm.txt'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conf_path = os.path.join(dir_path, path_core_normal)
    with open(conf_path, "r", encoding='utf-8') as file:
        texts = file.readlines()
        core_normal_set = set([i.strip() for i in texts])
    return core_normal_set


def create_set_words(doc):
    """
    Создает множество лемматизированных слов
    """
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
    tokens_set = set([_.lemma for _ in doc.tokens])
    return tokens_set


def search_core_step1(tokens_set):
    """
    На вход получает множество из лемматизированных слов наименования характеристики
    и множество стандартных наименований величин. Находит совпадения
    """
    core_normal_set = extract_core_normal()
    core_extract = tokens_set & core_normal_set
    return core_extract


def search_core_children(core: str, doc):
    """
    На вход подается список  из
    DocToken(stop=3, text='Вес', id='1_1', head_id='1_0', rel='root', pos='NOUN', feats=<Inan,Nom,Masc,Sing>, lemma='вес')
    и core - главное слово в предложении. Функция находит зависимые слова
    """
    doc.parse_syntax(syntax_parser)
    doc.sents[0].syntax
    core_children = {}
    for i in doc.tokens:
        if core == i.lemma and i.lemma not in stop_words:
            head = i.id
            count_name_core_amond = 0
            count_name_core_nmond = 0
            for children in doc.tokens:
                if children.lemma in core_children.values() or children.lemma == core or children.lemma in stop_words:
                    continue
                elif head == children.head_id \
                        and children.pos == 'ADJ' \
                        and children.id != head \
                        and children.pos != 'ADP':
                    core_amod = children.lemma
                    name_core_amod = f'core_amod{count_name_core_amond}'
                    core_children[name_core_amod] = core_amod
                    count_name_core_amond += 1
                elif head == children.head_id \
                        and children.pos == 'NOUN' \
                        and children.id != head \
                        and children.pos != 'ADP':
                    core_nmod = children.lemma
                    name_core_nmod = f'core_nmod{count_name_core_nmond}'
                    core_children[name_core_nmod] = core_nmod
                    count_name_core_nmond += 1
                    count_name_core_nmod_amod = 0
                    count_name_core_nmod_nmod = 0
                    for children_nmod in doc.tokens:
                        if children_nmod.lemma not in core_children.values() \
                                and children.id == children_nmod.head_id \
                                and children_nmod.pos == 'ADJ' \
                                and children_nmod.id != head \
                                and children_nmod.pos != 'ADP' \
                                and children_nmod.lemma not in stop_words:
                            core_nmod_amod = children_nmod.lemma
                            name_core_nmod_amod = f'core_nmod_amod{count_name_core_nmod_amod}'
                            core_children[name_core_nmod_amod] = core_nmod_amod
                            count_name_core_nmod_amod += 1
                        elif children_nmod.lemma not in core_children.values() \
                                and children.id == children_nmod.head_id \
                                and children_nmod.pos == 'NOUN' \
                                and children_nmod.id != head \
                                and children_nmod.pos != 'ADP' \
                                and children_nmod.lemma not in stop_words:
                            core_nmod_nmod = children_nmod.lemma
                            name_core_nmod_nmod = f'core_nmod_nmod{count_name_core_nmod_nmod}'
                            core_children[name_core_nmod_nmod] = core_nmod_nmod
                            count_name_core_nmod_nmod += 1
                elif head == children.head_id \
                        and children.id != head \
                        and children.pos != 'ADP' :
                    core_mod = children.lemma
                    if children.pos == 'NOUN' and 'core_nmod0' not in core_children.keys():
                        core_children['core_nmod0'] = core_mod
                    elif children.pos == 'ADJ' and 'core_amod0' not in core_children.keys():
                        core_children['core_amod0'] = core_mod
                elif (children.rel == 'root' or children.id == children.head_id or children.rel == "obj") \
                         \
                        and children.pos != 'ADP':
                    core_mod = children.lemma
                    if children.pos == 'NOUN' and 'core_nmod0' not in core_children.keys():
                        core_children['core_nmod0'] = core_mod
                    elif children.pos == 'ADJ' and 'core_amod0' not in core_children.keys():
                        core_children['core_amod0'] = core_mod

    return core_children


def search_core(text) -> dict:
    """
    Из предложения выбирает core - главное слово. Находит зависимые слова и записывает в один словарь
    """
    doc = Doc(text)
    doc.segment(segmenter)
    doc.parse_syntax(syntax_parser)
    doc.tag_morph(morph_tagger)
    tokens_set = create_set_words(doc)
    core_step1 = search_core_step1(tokens_set)
    dct_core = {}
    if core_step1 and len(core_step1) == 1:
        core = core_step1.pop()
        dct_core['core'] = core
        dct_core_children = search_core_children(core, doc)
        dct_core |= dct_core_children
        return dct_core
    sent = doc.sents[0]
    for token in sent.syntax:
        for i in token:
            word = morph.parse(i.text)[0]
            word_normal = word.normal_form
            if (i.rel == 'root' or i.id == i.head_id) \
                    and word.tag.POS == 'NOUN' \
                    and len(i.text) >= 3 \
                    and i.text.lower() not in stop_words:
                core = word_normal
                dct_core['core'] = core
                dct_core |= search_core_children(core, doc)
                return dct_core
            elif word.tag.POS == 'NOUN' \
                    and (word.tag.case == 'nomn' or word.tag.case == 'accs') \
                    and len(i.text) >= 3 \
                    and i.text.lower() not in stop_words:
                core = word_normal
                dct_core['core'] = core
                dct_core |= search_core_children(core, doc)
                return dct_core
    dct_core['core'] = None
    return dct_core





