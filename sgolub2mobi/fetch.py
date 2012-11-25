# -*- coding: utf-8 -*-

"""
Download data for book generation
"""
import os
import sys
import datetime
from web import wget, ArticleParser
import cPickle as pickle


def download_article (url):
    """
    By url, download and parse article. Return tuple with (title, date, content)
    """
    data = wget (url)
    parser = ArticleParser (data.decode ("utf-8"))
    return parser.title, parser.date, parser.text


def parse_date (s):
    v = s.split (" ")
    d = int (v[0])
    mn = v[1]
    y = int (v[2])
    m2d = { "Январь": 1,
            "Февраль": 2,
            "Март": 3,
            "Апрель": 4,
            "Май": 5,
            "Июнь": 6,
            "Июль": 7,
            "Август": 8,
            "Сентябрь": 9,
            "Октябрь": 10,
            "Ноябрь": 11,
            "Декабрь": 12 }
    return datetime.date (year=y, month=m2d[mn.encode ('utf-8')], day=d)


data = []        

for art in sys.stdin:
    art = art.strip ()
    title, date, content = download_article (art)
    dt = parse_date (date)
    data.append ((dt, title, content))
    print art

data.sort ()

with open ("posts.dat", "w+") as fd:
    pickle.dump (data, fd)
