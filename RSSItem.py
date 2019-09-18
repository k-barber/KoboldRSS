import datetime

class RSSItem:
    # Required
    title = "Default Title"
    link = "https://www.w3.org/about"
    description = "Default Description"

    # Other
    data = None

    # Optional
    author = None
    category = None
    comments = None
    enclosure = None
    guid = None
    pubDate = None
    source = None

    def replace(self):
        for index, value in enumerate(self.data):
            # Required
            self.title = self.title.replace("{%" + str(index + 1) + "}", value)
            self.link = self.link.replace("{%" + str(index + 1) + "}", value)
            self.description = self.description.replace("{%" + str(index + 1) + "}", value)

            # Optional
            if (self.author is not None): self.author = self.author.replace("{%" + str(index + 1) + "}", value)
            if (self.category is not None): self.category = self.category.replace("{%" + str(index + 1) + "}", value)
            if (self.comments is not None): self.comments = self.comments.replace("{%" + str(index + 1) + "}", value)
            if (self.enclosure is not None): self.enclosure = self.enclosure.replace("{%" + str(index + 1) + "}", value)
            if (self.guid is not None): self.guid = self.guid.replace("{%" + str(index + 1) + "}", value)
            if (self.pubDate is not None and isinstance(self.pubDate, str)): self.pubDate = self.pubDate.replace("{%" + str(index + 1) + "}", value)
            if (self.source is not None): self.source = self.source.replace("{%" + str(index + 1) + "}", value)

    def __init__(self, data, title=None, link=None, description=None, author=None, category=None, comments=None, enclosure=None, guid=None, pubDate=None, source=None):
        # Required
        self.title = title
        self.link = link
        self.description = description

        # Other
        self.data = data
        
        # Optional
        self.author = author
        self.category = category
        self.comments = comments
        self.enclosure = enclosure
        self.guid = guid
        self.pubDate = pubDate
        self.source = source
        
        #if (self.pubDate == None):
        #    self.pubDate = datetime.datetime.now()

        self.replace()
    
    def __str__(self):
        output = "        <item>\n"
        if (self.title is not None):
            output += "            <title>" + self.title + "</title>\n"
        if (self.link is not None):
            output += "            <link>" + self.link.replace("&", "&amp;") + "</link>\n"
        if (self.description is not None):
            output += "            <description>" + self.description + "</description>\n"
        if (self.author is not None):
            output += "            <author>" + self.author + "</author>\n"
        if (self.category is not None):
            output += "            <category>" + self.category + "</category>\n"
        if (self.comments is not None):
            output += "            <comments>" + self.comments + "</comments>\n"
        if (self.enclosure is not None):
            output += "            <enclosure>" + self.enclosure + "</enclosure>\n"
        if (self.guid is not None):
            output += "            <guid>" + self.guid + "</guid>\n"
        if (self.pubDate is not None):
            output += "            <pubDate>" + str(self.pubDate) + "</pubDate>\n"
        if (self.source is not None):
            output += "            <source>" + self.source + "</source>\n"
        output +="        </item>\n"
        return output
    
