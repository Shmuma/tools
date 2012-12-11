import os
import sys
import cPickle as pickle

print "Load posts data..."
with open ("posts.dat", "r") as fd:
    data = pickle.load (fd)
    images = pickle.load (fd)

print "Have %d posts and %d images" % (len (data), len (images))

# write data
result_dir = "res"

os.mkdir (result_dir)

toc_list = ""

idx = 0

for e in data:
    date, title, content, images_keys = e
#    if date.year != 2012:
#        continue
    idx += 1
    out_name = "%05d.html" % idx
    toc_list += "<a href='%s'>%s: %s</a><br/>\n" % (out_name.encode ('utf-8'), date, title.encode ('utf-8'))
    with open (os.path.join (result_dir, out_name), "w+") as fd:
        fd.write ("<html><body>\n")
        fd.write ("<h1>%s: %s</h1>" % (date, title.encode ("utf-8")))
        fd.write (content.encode ('utf-8'))
        fd.write ("</body></html>\n")
    for key in images_keys:
        if key in images:
            with open (os.path.join (result_dir, key), "wb+") as fd:
                fd.write (images[key])
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
