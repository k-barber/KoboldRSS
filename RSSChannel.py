import datetime

class RSSChannel:
    #Required
    title = "Default Title"
    link = "https://www.w3.org/about"
    description = "Default Description"
    
    #Content
    items = []

    language = "en-us"
    pubDate = None
    lastBuildDate = None
    generator = "https://github.com/k-barber/RSS-Manager"
    docs = "https://validator.w3.org/feed/docs/rss2.html"
    ttl = 60
    image = None

    def __str__(self):
        output = "<channel>\n"
        if (self.title is not None):
            output += "<title>" + self.title + "</title>\n"
        if (self.link is not None):
            output += "<link>" + self.link + "</link>\n"
        if (self.description is not None):
            output += "<description>" + self.description + "</description>\n"
        if (self.language is not None):
            output += "<language>" + self.language + "</language>\n"
        if (self.ttl is not None):
            output += "<ttl>" + self.ttl + "</ttl>\n"
        output +="</channel>"
        return output


    def __init__(self, data):
        for line in data:
            if line.startswith('title:'):
                self.title = line[6:].strip()
            if line.startswith('link:'):
                self.link = line[5:].strip()
            if line.startswith('description:'):
                self.description = line[12:].strip()
            if line.startswith('language:'):
                self.language = line[9:].strip()
            if line.startswith('ttl:'):
                self.ttl = line[4:].strip()
