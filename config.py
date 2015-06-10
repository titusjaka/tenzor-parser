# -*- coding: utf-8 -*-
__author__ = 'Denis Titusov, dtitusov@naumen.ru'

import os

class Config(object):
    def __init__(self):
        self.MAX_LENGTH = 80
        self.ARTICLE_TAGS = (
            {'itemprop': 'articleBody'},
            {'property': 'articleBody'},
            {'class': 'article'},
            {'class': 'content'},
            {'class': 'text'}
        )
config = Config()
