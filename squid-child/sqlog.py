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
    "192.168.2.11" : "ksu-m-1",
    "192.168.2.20" : "ksu-m-2",
}

timelines = []
cur_timelines = {}
hosts = {}
hr_dt_counts = {}

for l in sys.stdin:
    v = re.split("\s+", l)
    ts = float(v[0])
    client = v[2]
    addr = v[6]
    
    client = names.get(client, client)
    dt = datetime.datetime.fromtimestamp(ts)
    hr_dt = dt.replace(minute=0, second=0, microsecond=0)

    url = urlparse(addr)
    
    if url.netloc.find("accu-weather.com") >= 0 or len(url.netloc) == 0 or url.netloc.find("msftncsi.com") >= 0:
        continue

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
    
    if client not in hr_dt_counts:
        hr_dt_counts[client] = {}
    client_hr_dt = hr_dt_counts[client]
    if hr_dt not in client_hr_dt:
        client_hr_dt[hr_dt] = url.netloc
    else:
        client_hr_dt[hr_dt] += " '%s'" % url.netloc

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

    for hr_dt in sorted(hr_dt_counts[client].keys()):
        print "\t%s: %s" % (hr_dt, hr_dt_counts[client][hr_dt])
    print

for client in hosts.keys():
    print "Top for %s" % client
    vals = [v for v in hosts[client].iteritems()]
    vals.sort(key=lambda v: v[1], reverse=True)
    for domain, count in vals[:30]:
        if count > 10 and len(domain) > 0:
            print "\t%s: %d" % (domain, count)
