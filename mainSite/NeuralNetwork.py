import nltk
import tflearn
import tensorflow as tf
import numpy as np
import re

from nltk.stem.snowball import RussianStemmer
from nltk.tokenize import TweetTokenizer
from collections import Counter

from .AllMath import *
from .fileWork import *
from .settings import *


class NeuralNetwork:

    def __init__(self):
        self.model = self.build_model(learning_rate=0.75)
        self.stemer = RussianStemmer()
        self.regex = re.compile('[^а-яА-Я ]')
        self.stem_cache = {}
        self.stem_count = Counter()
        self.tokenizer = TweetTokenizer()

    def build_model(self, learning_rate=0.1):
        tf.reset_default_graph()
        net = tflearn.input_data([None, BIGRAMMS_VOCAB_SIZE + WORDS_VOCAB_SIZE])
        net = tflearn.fully_connected(net, 300, activation='ReLU')
        net = tflearn.fully_connected(net, 50, activation='ReLU')
        net = tflearn.fully_connected(net, 2, activation='softmax')
        regression = tflearn.regression(net, optimizer='Adam', learning_rate=learning_rate, loss='categorical_crossentropy')
        self.model = tflearn.DNN(net)
        self.model.load("model")
        return self.model

    """def get_stem(self, token):
        stem = self.stem_cache.get(token, None)
        if stem:
            return stem
        token = self.regex.sub('', token).lower()
        stem = self.stemer.stem(token)
        self.stem_cache[token] = stem
        return stem"""

    def get_stem(self, token):
        stem = self.stem_cache.get(token, None)
        if stem:
            return stem
        stem = self.stemmer.stem(token)
        self.stem_cache[token] = stem
        return stem

    def get_lemma(self, token):
        text = token[0] + " " + token[1]
        stem = self.lemmasCash.get(text, None)
        if stem:
            return stem
        # stem = myStem.lemmatize(token)
        self.lemmasCash[text] = text
        return text

    def article_to_vector(self, article, show_unknowns=False):
        vector = np.zeros(WORDS_VOCAB_SIZE + BIGRAMMS_VOCAB_SIZE, dtype=np.int_)
        for token in self.tokenizer.tokenize(article):
            word_idx = words_token_2_idx.get(token, None)
            if word_idx is not None:
                vector[word_idx] = 1
            elif show_unknowns:
                print("Unknown token: {}". format(token))
        for token in nltk.ngrams(nltk.word_tokenize(article), 2):
            stem = token[0] + ' ' + token[1]
            biramm_idx = biramm_token_2_idx.get(stem, None)
            if biramm_idx is not None:
                vector[biramm_idx + WORDS_VOCAB_SIZE] = 1
            elif show_unknowns:
                print("Unknown token: {}".format(token))
        return vector

    def article_to_vector_clearly(self, article, count_unknowns=True):
        vector = np.zeros(WORDS_VOCAB_SIZE + BIGRAMMS_VOCAB_SIZE, dtype=np.int_)
        unknown_word_count = 0
        unknown_word_sum = 0
        badWordsCounter = 0

        for token in self.tokenizer.tokenize(article):
            #badWord = badWordsDict.get(stem, None)
            badWord = badWordsDict.get(token, None)
            word_idx = words_token_2_idx.get(token, None)
            if badWord is not None:
                badWordsCounter += 1
            if word_idx is not None:
                vector[word_idx] = 1
            elif count_unknowns:
                #tone = word_token.get(stem, None)
                tone = word_token.get(token, None)
                if tone:
                    unknown_word_count += 1
                    if tone == 'NEUT':
                        unknown_word_sum += 0.5
                    elif tone == 'PSTV':
                        unknown_word_sum += 1
                    elif tone == 'NGTV':
                        unknown_word_sum += 0

        for token in nltk.ngrams(nltk.word_tokenize(article), 2):
            stem = token[0] + ' ' + token[1]
            biramm_idx = biramm_token_2_idx.get(stem, None)
            if biramm_idx is not None:
                vector[biramm_idx + WORDS_VOCAB_SIZE] = 1

        if unknown_word_count == 0:
            return [vector, None, badWordsCounter]
        return [vector, unknown_word_sum / unknown_word_count, badWordsCounter]

    def test_tweet(self, article):
        tweet_vector = self.article_to_vector(article, False)
        positive_prob = self.model.predict([tweet_vector])[0][1]

        if 0.35 < positive_prob < 0.66:
            return "нейтрально"
        elif positive_prob > 0.65:
            return "позитивно  " + str(int(((positive_prob * 100 - 65) / 35) * 100))
        else:
            return "негативно  " + str(int(((0.36 - positive_prob) / 0.36) * (-100)))

    def test_article_better(self, title, description):
        title_vector = self.article_to_vector(title, True)
        description_vector = self.article_to_vector(description, True)
        title_positive_prob = self.model.predict([title_vector])[0][1]
        description_positive_prob = self.model.predict([description_vector])[0][1]

        positive_prob = modifyProbe(probe_from_title=title_positive_prob, probe_from_desc=description_positive_prob)

        if 0.35 < positive_prob < 0.66:
            return "нейтрально"
        elif positive_prob > 0.65:
            return "позитивно  " + str(int(((positive_prob * 100 - 65) / 35) * 100))
        else:
            return "негативно  " + str(int(((0.36 - positive_prob) / 0.36) * (-100)))

    def test_article_the_best(self, title, description):
        title_vector = self.article_to_vector_clearly(title, True)
        description_vector = self.article_to_vector_clearly(description, True)
        title_positive_prob = self.model.predict([title_vector[0]])[0][1]
        description_positive_prob = self.model.predict([description_vector[0]])[0][1]
        positive_prob = modifyProbe(probe_from_title=title_positive_prob, probe_from_desc=description_positive_prob)

        if title_vector[1] is not None and description_vector[1] is not None:
            positive_prob = multipleAnswer(positive_prob, (title_vector[1] + description_vector[1]) / 2)
        elif title_vector[1] is not None and description_vector[1] is None:
            positive_prob = multipleAnswer(positive_prob, (title_vector[1]) / 2)
        elif title_vector[1] is None and description_vector[1] is not None:
            positive_prob = multipleAnswer(positive_prob, (description_vector[1]) / 2)

        if 0.35 < positive_prob < 0.66:
            return ["нейтрально", "info"]
        elif positive_prob > 0.65:
            return ["позитивно  ", "success"]
        else:
            return ["негативно  ", "danger"]

    def test_article_the_best_modern(self, title, description):
        title_vector = self.article_to_vector_clearly(title, True)
        description_vector = self.article_to_vector_clearly(description, True)
        title_positive_prob = self.model.predict([title_vector[0]])[0][1]
        description_positive_prob = self.model.predict([description_vector[0]])[0][1]
        positive_prob = modifyProbe(probe_from_title=title_positive_prob, probe_from_desc=description_positive_prob)
        print(description)
        print(title_positive_prob)
        print(description_positive_prob)
        print("---------------------------------------------------------------------")
        if title_vector[2] > 0:
            positive_prob = positive_prob * (1 - WEIGHT_OF_THE_WORSE_WORDS)
        if title_vector[1] is not None and description_vector[1] is not None:
            positive_prob = multipleAnswer(positive_prob, (title_vector[1] + description_vector[1]) / 2)
        elif title_vector[1] is not None and description_vector[1] is None:
            positive_prob = multipleAnswer(positive_prob, (title_vector[1]) / 2)
        elif title_vector[1] is None and description_vector[1] is not None:
            positive_prob = multipleAnswer(positive_prob, (description_vector[1]) / 2)

        if 0.35 < positive_prob < 0.66:
            return ["нейтрально", "info"]
        elif positive_prob > 0.65:
            return ["позитивно  " + str(int(((positive_prob * 100 - 65) / 35) * 100)), "success"]
        else:
            return ["негативно  " + str(int(((0.36 - positive_prob) / 0.36) * (-100))), "danger"]

    def test_article_the_best_api(self, title, description):
        title_vector = self.article_to_vector_clearly(title, True)
        description_vector = self.article_to_vector_clearly(description, True)
        title_positive_prob = self.model.predict([title_vector[0]])[0][1]
        description_positive_prob = self.model.predict([description_vector[0]])[0][1]

        positive_prob = modifyProbe(probe_from_title=title_positive_prob, probe_from_desc=description_positive_prob)

        if title_vector[1] is not None and description_vector[1] is not None:
            positive_prob = multipleAnswer(positive_prob, (title_vector[1] + description_vector[1]) / 2)
        elif title_vector[1] is not None and description_vector[1] is None:
            positive_prob = multipleAnswer(positive_prob, (title_vector[1]) / 2)
        elif title_vector[1] is None and description_vector[1] is not None:
            positive_prob = multipleAnswer(positive_prob, (description_vector[1]) / 2)

        return positive_prob
