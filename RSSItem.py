import datetime

class RSSItem:
    # Required
    title = "Default Title"
    link = "https://www.w3.org/about"
    description = "Default Description"
    author = None
    guid = None
    pubDate = None
    data = None
    domain = None

    def replace(self):
        if (self.domain):
            self.title = self.title.replace("{%domain}", self.domain)
            self.link = self.link.replace("{%domain}", self.domain)
            self.description = self.description.replace("{%domain}", self.domain)
            self.guid = self.guid.replace("{%domain}", self.domain)
        for index, value in enumerate(self.data):
            self.title = self.title.replace("{%" + str(index + 1) + "}", value)
            self.link = self.link.replace("{%" + str(index + 1) + "}", value)
            self.description = self.description.replace("{%" + str(index + 1) + "}", value)
            self.guid = self.guid.replace("{%" + str(index + 1) + "}", value)

    def __init__(self, title, link, description, guid, domain, data):
        self.title = title
        self.link = link
        self.description = description
        self.data = data
        self.guid = guid
        self.domain = domain
        self.replace()
    
    def __str__(self):
        output = "<item>\n"
        if (self.title is not None):
            output += "<title>" + self.title + "</title>\n"
        if (self.link is not None):
            output += "<link>" + self.link + "</link>\n"
        if (self.description is not None):
            output += "<description>" + self.description + "</description>\n"
        if (self.guid is not None):
            output += "<guid>" + self.guid + "</guid>\n"
        output +="</item>"
        return output
    
