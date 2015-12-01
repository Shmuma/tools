#!/usr/bin/env python
"""
Cambridge pronunciation extractor
"""
import argparse
import urllib2
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("word", type=str, help="Word to save pronunciation")

args = parser.parse_args()
print args

URL = "http://dictionary.cambridge.org/pronunciation/english/%s" % args.word

page = urllib2.urlopen(URL).read()

soup = BeautifulSoup(page, "html.parser")
mp3_url = None
for div in soup.find_all("div"):
    mp3 = div.get('data-src-mp3')
    if mp3 is not None and mp3.find("uk") >= 0:
        mp3_url = mp3

uk_div = soup.find('div', {'class': 'big-pron-uk-container'})
ipa = uk_div.find('span', {'class': 'ipa'})
if ipa is not None:
    print "/" + ipa.get_text() + "/"

file_name = "%s.mp3" % args.word

with open(file_name, "w+") as fd:
    mp3_data = urllib2.urlopen(mp3_url).read()
    fd.write(mp3_data)

print "MP3 saved in " + file_name


