import sys

import dateutil.parser
import logging
from lib import socks
import socket
from lib import db
from lib import web
from lib import index

# setup socks proxy
#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, "127.0.0.1", 9050)
#socket.socket = socks.socksocket

if len (sys.argv) != 2:
    print "Usage: refresh_carendar.py lj_blog_name"
    sys.exit (0)
ljname = sys.argv[1]

# logging
logging.basicConfig (format="%(asctime)s: %(message)s", level=logging.INFO)

db_path = "/mnt/heap/misc/ljblogs/%s" % ljname
#db_path = "db/%s" % ljname

blog_url = "http://%s.livejournal.com" % ljname

blog_db = db.BlogDB (db_path)
blog_db.load ()

blog = index.LJIndex (ljname)

# parse all pages
for str_date, url in blog.all ():
    if url in blog_db.meta:
        logging.info ("Post %s is already in DB, skip" % url)
    else:
        logging.info ("Process post %s" % url)
        data = web.wget (url)
        a_parser = web.ArticleParser (data.decode ("utf-8"), blog_url)
        date = dateutil.parser.parse (str_date)
        images = [img.encode ('utf-8') for img in a_parser.images.keys ()]
        me = db.MetaEntry (date, a_parser.title.encode ('utf-8'), url, images)

        logging.info ("Process %d images" % len (a_parser.images))

        for dest, src in a_parser.images.iteritems ():
            try:
                image_data = web.wget (src.encode ('utf-8'))
                blog_db.add_image (dest.encode ('utf-8'), image_data)
            except IOError:
                pass

        # add to meta last
        blog_db.add_meta (me)
        blog_db.add_text (url, a_parser.text.encode ('utf-8'))
        
