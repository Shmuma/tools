"""
Squid childred report

Calculates timeline for known clients and domain frequencies
"""
import sys
import re
import datetime
from urlparse import urlparse
from pprint import pprint

names = {
    "192.168.2.151": "jul-1",
    "192.168.2.153": "jul-2",
    "192.168.2.152": "ksu-1",
    "192.168.2.154": "ksu-2",
}

timelines = []
cur_timelines = {}
hosts = {}

for l in sys.stdin:
    v = re.split("\s+", l)
    ts = float(v[0])
    client = v[2]
    addr = v[6]
    
    client = names.get(client, client)
    dt = datetime.datetime.fromtimestamp(ts)

    url = urlparse(addr)
    
    if not client in hosts:
        hosts[client] = {}

    count = hosts[client].get(url.netloc, 0)
    hosts[client][url.netloc] = count+1

    tl = cur_timelines.get(client, (None, None))
    if tl[0] is None:
        tl = (dt, dt)
    elif dt - tl[1] > datetime.timedelta(hours=1):
        timelines.append((client, tl))
        tl = (dt, dt)
    else:
        tl = (tl[0], dt)
    cur_timelines[client] = tl

for client in cur_timelines.keys():
    tl = cur_timelines[client]
    timelines.append((client, tl))



for client in hosts.keys():
    print "Timelines for " + client
    prev_d = None
    for cl, tl in timelines:
        if cl != client:
            continue
        if prev_d is not None and prev_d != tl[0].day:
            print
        print "\t%s: %s -> %s" % (client, tl[0], tl[1])
        prev_d = tl[1].day
    print

for client in hosts.keys():
    print "Top for %s" % client
    vals = [v for v in hosts[client].iteritems()]
    vals.sort(key=lambda v: v[1], reverse=True)
    for domain, count in vals[:30]:
        if count > 10 and len(domain) > 0:
            print "\t%s: %d" % (domain, count)
