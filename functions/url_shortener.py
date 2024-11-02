import pyshorteners

def shorten_url(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)