import os
import sys
import cPickle as pickle
import logging
import datetime

from lib import db

def parse_dt (s, next_month=False):
    v = s.split ('-')
    year = int (v[0])
    month = int (v[1])
    if next_month:
        month += 1
        if month > 12:
            year += 1
            month = 1
    return datetime.date (year=year, month=month, day=1)


logging.basicConfig (format="%(asctime)s: %(message)s", level=logging.INFO)

# parse arguments
dt_from = dt_to = None

if len (sys.argv) == 1:
    logging.info ("Export all posts")
elif len (sys.argv) == 3:
    dt_from = parse_dt (sys.argv[1])
    dt_to = parse_dt (sys.argv[2], True) - datetime.timedelta (days=1)
    logging.info ("Export posts from %s to %s" % (dt_from, dt_to))
else:
    print "Usage: generate.py [YYYY-MM YYYY-MM]"
    sys.exit (0)

blog_db = db.BlogDB ("/mnt/heap/misc/sgolub")
blog_db.load ()

# write data
result_dir = "res"

os.mkdir (result_dir)

entries = []

for me in blog_db.meta.values ():
    if dt_from != None:
        if dt_from <= me.date and dt_to >= me.date:
            entries.append (me)
    else:
        entries.append (me)

entries.sort (cmp=lambda a, b: cmp (a.date, b.date))

idx = 0
toc_list = ""

for e in entries:
    idx += 1
    out_name = "%05d.html" % idx
    toc_list += "<a href='%s'>%s: %s</a><br/>\n" % (out_name, e.date, e.title)
    with open (os.path.join (result_dir, out_name), "w+") as fd:
        fd.write ("<html><body>\n")
        fd.write ("<h1>%s: %s</h1>" % (e.date, e.title))
        fd.write (blog_db.posts[e.url])
        fd.write ("</body></html>\n")
    for key in e.images:
        if key in blog_db.images:
            with open (os.path.join (result_dir, key), "wb+") as fd:
                fd.write (blog_db.images[key])
        else:
            print "Image %s not in img db, skip" % key

with open (os.path.join (result_dir, "index.html"), "w+") as fd:
    fd.write ("""
<html>
   <body>
     <h1>Table of Contents</h1>
     <p style="text-indent:0pt">
%s
     </p>
   </body>
</html>
""" % toc_list)
