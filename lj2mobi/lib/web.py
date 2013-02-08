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
#            delay = random.randint (1, 2)
#            logging.info ("wget %s, sleep for %d sec" % (url, delay))
            logging.info ("wget %s" % url)
            # sleep for random amount of seconds to reduce server's load
#            time.sleep (delay)
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



class LJIndexParser (HTMLParser):
    """
    Parses page and collects all articles links
    """
    def __init__ (self, data):
        HTMLParser.__init__ (self)
        self.entry_title = False

        self.links = set ()
        self.feed (data)
        self.close ()        


    def handle_starttag (self, tag, attrs):
        att = dict (attrs)
        if tag == 'dt' and att.get ('class') == 'entry-title':
            self.entry_title = True
            
        if tag == 'a' and self.entry_title:
            self.links.add (att['href'])


    def handle_endtag (self, tag):
        if tag == 'dt':
            self.entry_title = False



class ArticleParser (HTMLParser):
    title = ""
    date = None
    text = ""
    images = None

    inside_title = False
    inside_content = 0
    br_last = False

    def __init__ (self, data, blog_url):
        HTMLParser.__init__ (self)
        self.images = {}
        self.blog_url = blog_url
        self.feed (data)
        self.close ()


    def tweak_image (self, attrs):
        url_src = dict (attrs).get ('src', None)
        if url_src == None:
            return ""
        if url_src[0] == '/':
            url_src = self.blog_url.encode ('utf-8') + url_src
        ext = url_src.split ('.')[-1]
        if ext.find ('/') >= 0:
            ext = "jpg"
        dest = md5.new (url_src.encode ('utf-8')).hexdigest () + "." + ext
        self.images[dest] = url_src
        return "<img src=\"%s\"/>" % dest


    def handle_starttag (self, tag, attrs):
        att = dict (attrs)
        if tag == "img":
            if self.inside_content > 0:
                self.text += self.tweak_image (attrs)

        if tag == 'abbr' and att.get ('class') == 'updated':
            self.date = att.get ('title')

        if tag == "meta" and att.get ("name") == "title":
            self.title = att.get ("content")

        if tag == 'dt' and att.get ('class') == 'entry-title':
            self.inside_title = True

        if tag == 'br' and self.inside_content > 0 and not self.br_last:
            self.text += "<br><br>"
            self.br_last = True

        if tag == 'div' and att.get ('class') in ['entry-content', 'b-singlepost-body']:
            self.inside_content += 1


    def handle_endtag (self, tag):
        if self.inside_title and tag == 'dt':
            self.inside_title = False
        if self.inside_content > 0 and tag == 'div':
            self.inside_content -= 1


    def __handle_text (self, text):
        if self.inside_content > 0:
            self.text += text
        elif self.inside_title:
            self.title += text
        self.br_last = False


    def handle_data (self, data):
        self.__handle_text (data)


    def handle_entityref (self, name):
        self.__handle_text ("&%s;" % name)


    def handle_charref (self, name):
        self.__handle_text ("&#%s;" % name)



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
