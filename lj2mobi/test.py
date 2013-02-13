from lib import index
from lib import web
import dateutil.parser


blog = index.LJIndex ("polustanok")

#for url in blog.all ():
#    print url

#for date, url in blog._posts (2011, 11):
#    print date, url

data = web.wget ("http://pesen-net.livejournal.com/70540.html")
a_parser = web.ArticleParser (data.decode ("utf-8"), "http://pesen-net.livejournal.com")
print a_parser.title
print a_parser.images
print a_parser.text

