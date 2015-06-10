# -*- coding: utf-8 -*-
__author__ = 'Denis Titusov, dtitusov@naumen.ru'

import sys
import os
from bs4 import BeautifulSoup

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from config import config

class ParsingError(Warning):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Parser(object):
    def __init__(self, url):
        self.url = url
        self.config = config

    def get_text(self, url=None):
        if self.url is None and url is None:
            raise ParsingError('No url specified')
        elif self.url is None:
            self.url = url
        self.page = urllib2.urlopen(self.url)
        soup = BeautifulSoup(self.page)
        self.html = soup.prettify('utf-8')
        text_list = []
        for tags in config.ARTICLE_TAGS:
            divs = soup.findAll('div', tags)
            if divs:
                break
        else:
            raise ParsingError('Article could not be parsed')
        for div in divs:
            if not div.findAll('p'):
                self.raw_text = divs[0].text
                return self.raw_text
            for p in div.findAll('p'):
                temp_text = p.text
                for a in p.findAll('a'):
                    a_href = '{0} [{1}]'.format(a.string, a.get('href'))
                    temp_text = temp_text.replace(a.string, a_href)
                text_list.append(temp_text)
        self.raw_text = '\n'.join(text_list)
        return self.raw_text

    def format_text(self):
        text_list = [line.split(' ') for line in self.raw_text.split('\n')]
        result_list = [] * len(text_list)
        for index in range(len(text_list)):
            length = 0
            result_list.append([])
            for word in text_list[index]:
                length += len(word)
                length += 1
                if length > self.config.MAX_LENGTH:
                    result_list[index].append('\n')
                    result_list[index].append(word)
                    length = len(word) + 1
                else:
                    result_list[index].append(word)
            else:
                result_list[index].append('\n')
        formatted_list = [' '.join(lst).replace('\n ', '\n').replace(' \n', '\n') for lst in result_list]
        self.text = '\n'.join(formatted_list)
        return self.text

    def get_file_name(self):
        path = self.url.replace('http://', '').replace('https://', '')
        self.file_path = os.path.normpath('examples/{0}'.format(path))
        self.html_filename = os.path.normpath('{0}/original.html'.format(self.file_path))
        self.txt_filename = os.path.normpath('{0}/parsed.txt'.format(self.file_path))
        self.create_folders()

    def create_folders(self):
        dir = self.file_path
        if not os.path.isdir(dir):
            os.makedirs(dir)

    def save_file(self):
        self.get_file_name()
        with open(self.html_filename, 'bw') as original:
            original.write(self.html)
        with open(self.txt_filename, 'bw') as parsed:
            parsed.write(self.text.encode('utf-8'))

if __name__ == '__main__':
    url = sys.argv[1]
    parser = Parser(url)
    parser.get_text()
    formatted = parser.format_text()
    parser.save_file()