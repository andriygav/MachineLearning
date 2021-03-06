# -*- coding: utf-8 -*-
from nltk.tokenize import RegexpTokenizer
import pymorphy2


class ModelProcessor(object):
    def __init__(self, config):
        self._morph = pymorphy2.MorphAnalyzer()
        self._tokenizer = RegexpTokenizer('[a-zа-яёЁА-ЯA-Z]+|[^\w\s]|\d+')
    
    def processor(self, text):
        tokens = self._tokenizer.tokenize(text.lower())
        return list(map(lambda x: self._morph.parse(x)[0].normal_form, tokens))

    def __call__(self, text):
        return self.processor(text)