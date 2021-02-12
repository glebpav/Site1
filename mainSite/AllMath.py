

def multiple_answer(tone_from_nn, tone_from_unknown_words):
    return tone_from_nn * (1 - WEIGHT_OF_UNKNOWN_WORDS) + tone_from_unknown_words * WEIGHT_OF_UNKNOWN_WORDS

def modify_probe(probe_from_title, probe_from_desc):
    return probe_from_title * (1 - INFLUENCE_OF_DESCRIPTION) + probe_from_desc * INFLUENCE_OF_DESCRIPTION