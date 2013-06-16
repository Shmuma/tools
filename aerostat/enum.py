import urllib
import re
import sys

base_url = "http://aquarium.lipetsk.ru/MESTA/mp3/Aerostat/"

def gen_index ():
    fd = urllib.urlopen (base_url)
    res = fd.read ()
    d = []
    for l in res.split ('\n'):
        l = l.strip ()
        if l.find ('[DIR]') != -1 and l.find ('Parent Directory') == -1:
            r = re.search ("Aerostat_vol_\d+", l)
            if r:
                d.append (r.group (0))
    fd.close ()

    d.sort (lambda a, b: int (a.split ('_')[2]) - int (b.split ('_')[2]))
    return d


def get_mp3 (d):
    fd = urllib.urlopen (base_url + d)
    res = fd.read ()
    cand = None
    for l in res.split ('\n'):
        l = l.strip ()
        if l.find ('[SND]') != -1:
            r = re.search ("a href=\"([^\"]+)\"", l)
            if r.group(1).endswith (".mp3"):
                if cand == None or len (cand) > len (r.group (1)):
                    cand = r.group (1)
    
    return cand


if len (sys.argv) == 1:
    f = 0
else:
    f = int (sys.argv[1])

for d in gen_index ():   
    index = int (d.split ('_')[2])
    if index >= f:
        u = base_url + d + "/" + get_mp3 (d)
        print "wget -c '%s' -O Aerostat_%03d.mp3" % (u, index)
