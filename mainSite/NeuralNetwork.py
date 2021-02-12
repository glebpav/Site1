import tflearn
import tensorflow as tf
import numpy as np
import re

from nltk.stem.snowball import RussianStemmer
from nltk.tokenize import TweetTokenizer
from collections import Counter
from .AllMath import *


class NeuralNetwork:

    def __init__(self, vocabSize):
        self.build_model(learning_rate=0.75)
        self.model.load("model")
        self.stemer = RussianStemmer()
        self.regex = re.compile('[^а-яА-Я ]')
        self.stem_cache = {}
        self.stem_count = Counter()
        self.tokenizer = TweetTokenizer()
        self.vocabSize = vocabSize

    def build_model(self, learning_rate=0.1):
        tf.reset_default_graph()
        net = tflearn.input_data([None, self.vocabSize])
        net = tflearn.fully_connected(net, 300, activation='ReLU')
        net = tflearn.fully_connected(net, 50, activation='ReLU')
        net = tflearn.fully_connected(net, 2, activation='softmax')
        regression = tflearn.regression(net, optimizer='Adam', learning_rate=learning_rate, loss='categorical_crossentropy')
        self.model = tflearn.DNN(net)
        self.model.load("model")
        return self.model

    def get_stem(self, token):
        stem = self.stem_cache.get(token, None)
        if stem:
            return stem
        token = self.regex.sub('', token).lower()
        stem = self.stemer.stem(token)
        self.stem_cache[token] = stem
        return stem

    def article_to_vector(self, article, show_unknowns=False):
        vector = np.zeros(self.vocabSize , dtype=np.int_)
        for token in self.tokenizer.tokenize(article):
            stem = self.get_stem(token)
            idx = self.token_2_idx.get(stem, None)
            if idx is not None:
                vector[idx] = 1
                vector[idx] = 1

        return vector



    def article_to_vector_clearly(self, article, count_unknowns=True):
        vector = np.zeros(self.vocabSize, dtype=np.int_)
        unknown_word_count = 0
        unknown_word_sum = 0
        badWordsCounter = 0

        for token in self.tokenizer.tokenize(article):
            stem = self.get_stem(token)
            badWord = badWordsDict.get(stem, None)
            idx = self.token_2_idx.get(stem, None)

            if badWord is not None:
                # print(badWord)
                badWordsCounter += 1

            if idx is not None:
                vector[idx] = 1
            elif count_unknowns:
                tone = word_token.get(stem, None)
                if tone:
                    unknown_word_count += 1
                    if tone == 'NEUT':
                        unknown_word_sum += 0.5
                    elif tone == 'PSTV':
                        unknown_word_sum += 1
                    elif tone == 'NGTV':
                        unknown_word_sum += 0

        # print(badWordsCounter)
        if unknown_word_count == 0:
            return [vector, None, badWordsCounter]
        return [vector, unknown_word_sum / unknown_word_count, badWordsCounter]

    def test_tweet(article):
        tweet_vector = article_to_vector(article, False)
        positive_prob = model.predict([tweet_vector])[0][1]

        if 0.35 < positive_prob < 0.66:
            return "нейтрально"
        elif positive_prob > 0.65:
            return "позитивно  " + str(int(((positive_prob * 100 - 65) / 35) * 100))
        else:
            return "негативно  " + str(int(((0.36 - positive_prob) / 0.36) * (-100)))

    def test_article_better(title, description):
        title_vector = article_to_vector(title, True)
        description_vector = article_to_vector(description, True)
        title_positive_prob = model.predict([title_vector])[0][1]
        description_positive_prob = model.predict([description_vector])[0][1]

        positive_prob = modify_probe(probe_from_title=title_positive_prob, probe_from_desc=description_positive_prob)

        if 0.35 < positive_prob < 0.66:
            return "нейтрально"
        elif positive_prob > 0.65:
            return "позитивно  " + str(int(((positive_prob * 100 - 65) / 35) * 100))
        else:
            return "негативно  " + str(int(((0.36 - positive_prob) / 0.36) * (-100)))

    def test_article_the_best(title, description):
        title_vector = article_to_vector_clearly(title, True)
        description_vector = article_to_vector_clearly(description, True)
        title_positive_prob = model.predict([title_vector[0]])[0][1]
        description_positive_prob = model.predict([description_vector[0]])[0][1]
        # print(title_positive_prob)

        positive_prob = modify_probe(probe_from_title=title_positive_prob, probe_from_desc=description_positive_prob)

        if title_vector[1] is not None and description_vector[1] is not None:
            positive_prob = multiple_answer(positive_prob, (title_vector[1] + description_vector[1]) / 2)
        elif title_vector[1] is not None and description_vector[1] is None:
            positive_prob = multiple_answer(positive_prob, (title_vector[1]) / 2)
        elif title_vector[1] is None and description_vector[1] is not None:
            positive_prob = multiple_answer(positive_prob, (description_vector[1]) / 2)

        if 0.35 < positive_prob < 0.66:
            return ["нейтрально", "info"]
        elif positive_prob > 0.65:
            return ["позитивно  ", "success"]
        else:
            return ["негативно  ", "danger"]

    def test_article_the_best_modern(title, description):
        title_vector = article_to_vector_clearly(title, True)
        description_vector = article_to_vector_clearly(description, True)
        title_positive_prob = model.predict([title_vector[0]])[0][1]
        description_positive_prob = model.predict([description_vector[0]])[0][1]
        # print(title_positive_prob)
        # print(title_vector[2])

        positive_prob = modify_probe(probe_from_title=title_positive_prob, probe_from_desc=description_positive_prob)

        if title_vector[2] > 0:
            positive_prob = positive_prob * (1 - WEIGHT_OF_THE_WORSE_WORDS)
            # print("applied OK")

        if title_vector[1] is not None and description_vector[1] is not None:
            positive_prob = multiple_answer(positive_prob, (title_vector[1] + description_vector[1]) / 2)
        elif title_vector[1] is not None and description_vector[1] is None:
            positive_prob = multiple_answer(positive_prob, (title_vector[1]) / 2)
        elif title_vector[1] is None and description_vector[1] is not None:
            positive_prob = multiple_answer(positive_prob, (description_vector[1]) / 2)

        if 0.35 < positive_prob < 0.66:
            return ["нейтрально", "info"]
        elif positive_prob > 0.65:
            return ["позитивно  " + str(int(((positive_prob * 100 - 65) / 35) * 100)), "success"]
        else:
            return ["негативно  " + str(int(((0.36 - positive_prob) / 0.36) * (-100))), "danger"]

    def test_article_the_best_api(title, description):
        title_vector = article_to_vector_clearly(title, True)
        description_vector = article_to_vector_clearly(description, True)
        title_positive_prob = model.predict([title_vector[0]])[0][1]
        description_positive_prob = model.predict([description_vector[0]])[0][1]

        positive_prob = modify_probe(probe_from_title=title_positive_prob, probe_from_desc=description_positive_prob)

        if title_vector[1] is not None and description_vector[1] is not None:
            positive_prob = multiple_answer(positive_prob, (title_vector[1] + description_vector[1]) / 2)
        elif title_vector[1] is not None and description_vector[1] is None:
            positive_prob = multiple_answer(positive_prob, (title_vector[1]) / 2)
        elif title_vector[1] is None and description_vector[1] is not None:
            positive_prob = multiple_answer(positive_prob, (description_vector[1]) / 2)

        return positive_prob
