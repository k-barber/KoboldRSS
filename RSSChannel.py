import datetime

class RSSChannel:
    #Required
    title = "Default Title"
    link = "https://www.w3.org/about"
    description = "Default Description"
    
    #Content
    items = []

    #Optional
    language = "en-us"
    copyright = None
    managingEditor = None
    webMaster = None
    pubDate = datetime.datetime.now()
    lastBuildDate = datetime.datetime.now()
    category = None
    generator = None
    docs = "https://validator.w3.org/feed/docs/rss2.html"
    cloud = None
    ttl = None
    image = None
    textInput = None
    skipHours = None
    skipDates = None
