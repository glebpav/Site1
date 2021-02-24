from .settings import *


def multipleAnswer(tone_from_nn, tone_from_unknown_words):
    return tone_from_nn * (1 - WEIGHT_OF_UNKNOWN_WORDS) + tone_from_unknown_words * WEIGHT_OF_UNKNOWN_WORDS


def modifyProbe(probe_from_title, probe_from_desc):
    return probe_from_title * (1 - INFLUENCE_OF_DESCRIPTION) + probe_from_desc * INFLUENCE_OF_DESCRIPTION
