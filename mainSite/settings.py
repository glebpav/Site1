""" ----------------------  some settings  ---------------------------- """

WORDS_VOCAB_SIZE = 7000
BIGRAMMS_VOCAB_SIZE = 7000

WEIGHT_OF_UNKNOWN_WORDS = 0.15
INFLUENCE_OF_DESCRIPTION = 0.68
WEIGHT_OF_THE_WORSE_WORDS = 0.50  # этот коэффициент уменьшает конечную тональность на заданную долю
PAGE_NUM = 1  # количество страниц затрагиваемых при поиске новостей


WORDS_VOCAB_PATH = 'words_vocab.txt'
BIGRAMMS_VOCAB_PATH = 'bigrammVocab.txt'
BAD_WORDS_VOCAB_PATH = 'badWordsVocab.txt'

DEFAULT_SITES_FOR_MOBILE = "Lenta;РИА Новости;РБК;Meduza"   # список сайтов, добавляемых каждому новому пользователю
sites = {"Lenta", "РИА Новости", "РБК", "Meduza"}  # список новостных ресурсов
