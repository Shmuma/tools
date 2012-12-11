import os
import shelve
import logging


class BlogDB (object):
    """
    Blog database
    """
    
    dirname = None
    meta = None
    posts = None
    images = None


    def __init__ (self, dirname):
        self.dirname = dirname


    def __del__ (self):
        del self.meta
        del self.posts
        del self.images


    def load (self):
        logging.info ("Start DB load from '%s'" % self.dirname)
        self.meta = shelve.open (os.path.join (self.dirname, "meta.shelf"), writeback=True)
        logging.info ("Loaded %d meta entries" % len (self.meta))
        self.posts = shelve.open (os.path.join (self.dirname, "posts.shelf"))
        logging.info ("Loaded %d posts" % len (self.posts))
        self.images = shelve.open (os.path.join (self.dirname, "images.shelf"))
        logging.info ("Loaded %d images" % len (self.images))


    def add_meta (self, me):
        self.meta[me.url] = me


    def add_text (self, url, text):
        self.posts[url] = text


    def add_image (self, name, data):
        self.images[name] = data


class MetaEntry (object):
    """
    Data about one blog post
    """
    
    def __init__ (self, date, title, url, images=[]):
        self.date = date
        self.title = title
        self.url = url
        self.images = images
        
