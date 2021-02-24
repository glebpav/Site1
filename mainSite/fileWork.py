import re
from pymystem3 import Mystem
from .settings import *

f = open(WORDS_VOCAB_PATH, 'r')
wordsVocab = f.read().split(";")
f.close()
f = open(BIGRAMMS_VOCAB_PATH, 'r')
birammVocab = f.read().split(";")
f.close()
f = open('word_tone.txt', 'r')
word_tone = f.read().split()
f.close()
f = open('badWordsVocab.txt', 'r')
badWordsVocab = f.read().split()
f.close()

word_token = {}
badWordsDict = {}
stem_cache = {}
lemmasCash = {}
regex = re.compile('[^а-яА-Я <break>]')
myLemm = Mystem()

words_token_2_idx = {wordsVocab[i].replace(';', ''): i for i in range(WORDS_VOCAB_SIZE)}
biramm_token_2_idx = {birammVocab[i].replace(';', ''): i for i in range(BIGRAMMS_VOCAB_SIZE)}


for word in word_tone:
    mas = word.split(";")
    dict = {mas[0]: mas[1]}
    word_token.update(dict)

for word in badWordsVocab:
    badWordsDict.update({word: word})