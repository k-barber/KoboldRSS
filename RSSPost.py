import datetime

class RSSPost:
    # Required
    title = "Default Title"
    link = "https://www.w3.org/about"
    description = "Default Description"
    author = None
    guid = None
    pubDate = datetime.datetime.now()

    def __init__(self, data):
        pass
    
    def __str__(self):
        pass
    
