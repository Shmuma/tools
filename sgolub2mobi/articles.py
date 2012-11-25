"""
Extracts list of all articles
"""
import sys

from web import wget, ProtografParser

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
