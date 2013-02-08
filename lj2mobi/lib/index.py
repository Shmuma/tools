import web

from HTMLParser import HTMLParser


class LJIndex (object):
    blog = None
    
    def __init__ (self, blog):
        self.blog = blog

    def all (self):
        """
        Yield all posts in the given blog
        """
        for year in self._years ():
            for mon in range (1, 12):
                for date, url in self._posts (year, mon):
                    yield (date, url)


    def _years (self):
        """
        Yield all years with posts
        """
        cal = web.wget ("http://%s.livejournal.com/calendar" % self.blog)
        parser = LJCalendarYearsParser (cal)
        for y in parser.years:
            yield y
        

    def _posts (self, year, mon):
        idx_data = web.wget ("http://%s.livejournal.com/%04d/%02d/" % (self.blog, year, mon))

        parser = LJCalendarIndexParser (idx_data)
        for day, url in parser.posts:
            yield ("%4d-%02d-%02d" % (year, mon, day), url)
        
        

class LJCalendarYearsParser (HTMLParser):
    def __init__ (self, data):
        HTMLParser.__init__ (self)
        self.years = []
        self.in_div = False
        self.in_ul = False
        self.in_li = False

        self.feed (data)
        self.close ()


    def handle_starttag (self, tag, attrs):
        att = dict (attrs)

        if tag == "div" and att.get ("id") == "alpha-inner":
            self.in_div = True
        elif tag == "ul" and self.in_div:
            self.in_ul = True
        elif self.in_ul and tag == "li":
            self.in_li = True


    def handle_data (self, data):
        if self.in_div and self.in_ul and self.in_li and len (data) > 0:
            self.years.append (int (data))


    def handle_endtag (self, tag):
        if tag == "div":
            self.in_div = False
        if tag == "li":
            self.in_li = False
        if tag == "ul":
            self.in_ul = False


class LJCalendarIndexParser (HTMLParser):
    def __init__ (self, data):
        HTMLParser.__init__ (self)

        self.posts = []
        self.in_dl = False
        self.in_dd = False
        self.in_dt = False
        self.date = None

        self.feed (data)
        self.close ()


    def handle_starttag (self, tag, attrs):
        att = dict (attrs)

        if tag == "dl":
            self.in_dl = True
        elif tag == "dt" and self.in_dl:
            self.in_dt = True
        elif tag == "dd" and self.in_dl:
            self.in_dd = True
        elif tag == "a" and self.in_dd:
            self.posts.append ((int (self.date), att.get ("href")))

        
    def handle_endtag (self, tag):
        if tag == "dl":
            self.in_dl = False
        if tag == "dd":
            self.in_dd = False
        if tag == "dt":
            self.in_dt = False


    def handle_data (self, data):
        if self.in_dl and self.in_dt:
            self.date = data
