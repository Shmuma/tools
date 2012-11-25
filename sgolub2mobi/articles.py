"""
Extracts list of all articles
"""
import sys
import urllib
from HTMLParser import HTMLParser



def wget (url):
    fd = urllib.urlopen (url)
    res = fd.read ()
    fd.close ()
    return res



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

from_page = 0
to_page = 0

if len (sys.argv) == 2:
    from_page = to_page = int (sys.argv[1])
elif len (sys.argv) == 3:
    from_page = int (sys.argv[1])
    to_page = int (sys.argv[2])

url = "http://sgolub.ru/protograf?page=%d"

for idx in range (from_page, to_page+1):
    data = wget (url % idx)
    parser = ProtografParser (data)
    for u in parser.links:
        print "http://sgolub.ru%s" % u
