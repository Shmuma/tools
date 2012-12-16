# -*- coding: utf-8 -*-

import re
import md5
import time
import random
import urllib
import datetime
import logging
from HTMLParser import HTMLParser


# User-Agent: Python-urllib/1.17
def wget (url, random_sleep=True):
    for i in range (10):
        try:
            delay = random.randint (5, 10)
            logging.info ("wget %s, sleep for %d sec" % (url, delay))
            # sleep for random amount of seconds to reduce server's load
            time.sleep (delay)
            fd = urllib.urlopen (url)
            #    opener = urllib2.build_opener ()
            #    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            #    fd = opener.open (url)
            res = fd.read ()
            fd.close ()
            return res
        except IOError:
            logging.info ("Error, retry %d" % i)
            continue



class ProtografParser (HTMLParser):
    """
    Parses page and collects all articles links
    """
    def __init__ (self, data):
        HTMLParser.__init__ (self)
        self.kindergarden = set ()
        self.links = set ()
        self.feed (data)
        self.close ()        


    def handle_starttag (self, tag, attrs):
        if tag == 'a':
            for name, val in attrs:               
                if name == 'href' and val.startswith ('/protograf/'):
                    if val in self.kindergarden:
                        self.links.add (val)
                    else:
                        self.kindergarden.add (val)



class ArticleParser (HTMLParser):
    title = None
    date = None
    text = ""
    images = None

    # state
    title_coming = False
    date_coming = False
    inside_content = 0

    def __init__ (self, data):
        HTMLParser.__init__ (self)
        self.images = {}
        self.feed (data)
        self.close ()


    def tweak_image (self, attrs):
        url_src = dict (attrs).get ('src', None)
        if url_src == None:
            return ""
        if url_src[0] == '/':
            url_src = u'http://sgolub.ru' + url_src
        ext = url_src.split ('.')[-1]
        dest = md5.new (url_src.encode ('utf-8')).hexdigest () + "." + ext
        self.images[dest] = url_src
        return "<img src=\"%s\"/>" % dest

    def handle_starttag (self, tag, attrs):
        if self.inside_content > 0:
            self.inside_content += 1
            if tag == 'img':
                self.text += self.tweak_image (attrs)
            else:
                self.text += "<%s %s>" % (tag, " ".join (map (lambda a: "%s='%s'" % a, attrs)))
            return
        att = dict (attrs)
        if tag == "h1" and att.get ('class') == "main-page-title":
            self.title_coming = True
        if tag == "span" and att.get ('class') == "date":
            self.date_coming = True
        if tag == 'div' and att.get ('class') == 'content clear-block':
            self.inside_content += 1


    def handle_endtag (self, tag):
        if self.title_coming and tag == "h1":
            self.title_coming = False
        if self.date_coming and tag == "span":
            self.date_coming = False
        if self.inside_content > 0:
            self.text += "</%s>" % tag
            self.inside_content -= 1


    def handle_data (self, data):
        if self.title_coming:
            self.title = data
        if self.date_coming:
            self.date = data
        if self.inside_content > 0:
            self.text += data


    def handle_entityref (self, name):
        if self.inside_content > 0:
            self.text += "&%s;" % name


    def handle_charref (self, name):
        if self.inside_content > 0:
            self.text += "&#%s;" % name



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
