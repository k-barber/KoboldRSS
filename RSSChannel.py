import datetime
import requests
from RSSItem import RSSItem

Debug = False

class RSSChannel:
    #Required
    title = "Default Title"
    link = "https://www.w3.org/about"
    description = "Default Description"
    
    #Content
    items = []

    #Optional
    language = "en-us"
    pubDate = datetime.datetime.now()
    lastBuildDate = datetime.datetime.now()
    generator = "https://github.com/k-barber/RSS-Manager"
    docs = "https://validator.w3.org/feed/docs/rss2.html"
    ttl = 60
    image = None
    domain = None

    #Item Definition
    item_pattern = None
    item_title = None
    item_link = None
    item_description = None
    item_guid = None

    def __str__(self):
        output = "<channel>\n"
        if (self.title is not None):
            output += "<title>" + self.title + "</title>\n"
        if (self.link is not None):
            output += "<link>" + self.link.replace("&", "&amp;") + "</link>\n"
        if (self.description is not None):
            output += "<description>" + self.description + "</description>\n"
        if (self.language is not None):
            output += "<language>" + self.language + "</language>\n"
        if (self.ttl is not None):
            output += "<ttl>" + self.ttl + "</ttl>\n"
        if (len(self.items) != 0):
            for item in self.items:
                output += str(item)
        output +="</channel>"
        return output

    def print(self):
        print("Title: " + self.title)
        print("Link: " + self.link)
        print("Description: " + self.description)
        print("Language: " + self.language)
        print("PubDate: " + str(self.pubDate))
        print("BildDate: " + str(self.lastBuildDate))
        print("Generator: " + self.generator)
        print("Doc: " + self.docs)
        print("Ttl: " + str(self.ttl))
        print("Image: " + str(self.image))
        print("Item Pattern: " + str(self.item_pattern) + "\n")
        print("item_title: " + str(self.item_title) + "\n")
        print("item_link: " + str(self.item_link) + "\n")
        print("item_description: " + str(self.item_description) + "\n")
        print("item_guid: " + str(self.item_guid) + "\n")

    def create_item(self, data):
        return RSSItem(self.item_title, self.item_link, self.item_description, self.item_guid, self.domain, data)

    def clean_input(self, text):
        text = text.strip()
        text = text.replace("&amp;", "&")
        text = text.replace("&gt;", ">")
        text = text.replace("&lt;", "<")
        text = text.replace("&nbsp;", " ")
        text = text.replace("&quot;", '"')
        text = text.replace("&apos;", "'")
        text = text.replace("&#62;", ">")
        text = text.replace("&#60;", "<")
        text = text.replace("&#160;", " ")
        text = text.replace("&#34;", '"')
        text = text.replace("&#39", "'")
        return text

    def __init__(self, data):
        for line in data:
            if line.startswith('title:'):
                self.title = self.clean_input(line[6:])
            if line.startswith('link:'):
                self.link = self.clean_input(line[5:])
            if line.startswith('description:'):
                self.description = self.clean_input(line[12:])
            if line.startswith('language:'):
                self.language = self.clean_input(line[9:])
            if line.startswith('ttl:'):
                self.ttl = self.clean_input(line[4:])
            if line.startswith('item_pattern:'):
                self.item_pattern = self.clean_input(line[13:])
            if line.startswith('item_title:'):
                self.item_title = self.clean_input(line[11:])
            if line.startswith('item_link:'):
                self.item_link = self.clean_input(line[10:])
            if line.startswith('item_description:'):
                self.item_description = self.clean_input(line[17:])
            if line.startswith('item_guid:'):
                self.item_guid = self.clean_input(line[10:])
            if line.startswith('domain:'):
                self.domain = self.clean_input(line[7:])
            self.items = []
        if (Debug): self.print()

    def get_item_text(self, text, start_pattern, stop_pattern):
        start = 0
        if Debug: print("Getting Image Data")
        item_data = []
        while(start >= 0):
            start = text.find(start_pattern, start)
            stop = text.find(stop_pattern, start)
            if (start > 0):
                item_data.append(text[start:stop+len(stop_pattern)])
                start += 1
        return item_data

    def parse_item_text(self, item_text):
        if (Debug): print("Parsing Item Text")
        if (self.item_pattern == None):
            return
        output = []
        pattern_start = 0
        start = 0
        item_pattern = self.item_pattern
        if (Debug): print("Item Pattern: " + item_pattern)
        while(start >= 0):
            left_start = pattern_start
            if (Debug): print("left_start: " + str(left_start))
            left_stop = item_pattern.find("{", pattern_start)
            if (Debug): print("left_stop: " + str(left_stop))
            left = item_pattern[left_start:left_stop]
            
            right_start = item_pattern.find("}", left_stop)+1
            if (Debug): print("right_start: " + str(right_start))
            right_stop = item_pattern.find("{", right_start)
            if (Debug): print("right_stop: " + str(right_stop))

            if (right_stop > 0):
                right = item_pattern[right_start:right_stop]
            else:
                right = item_pattern[right_start:]

            if (Debug): print("Left: " + left)
            if (Debug): print("Right: " + right)

            stop = item_text.find(right, start)

            if (Debug): print("Char: " + item_pattern[left_stop+1])
            if (item_pattern[left_stop+1] == "%"):
                field = self.clean_input(item_text[item_text.find(left, start) + len(left): stop])
                if (Debug): print("Field: " + field)
                output.append(field)
            elif (Debug):
                field = self.clean_input(item_text[item_text.find(left, start) + len(left): stop])
                print("Field: " + field)
            
            pattern_start = right_start
            if (Debug): print("pattern_start: " + str(pattern_start))
            start = stop
            if (Debug): print("start: " + str(start))
        return output

    def parse_items(self, data):
        output = []
        for text in data:
            output.append(self.parse_item_text(text))
        return output

    def save_feed(self):

        output = '''<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet type="text/xsl" href="/res/preview.xsl"?>
<rss version="2.0">'''
        output += "\n" + str(self)

        output += "</rss>"

        f = open("Feeds/" + self.title.replace(":", "~").replace(" ", "_") + ".xml", "wb")
        f.write(str.encode(output))
        f.close()

    def generate_items(self):
        if (self.item_pattern == None):
            return
        if (self.link == "https://www.w3.org/about"):
            return
        if (len(self.items) > 0):
            self.items = []
        start_pattern = self.item_pattern[:self.item_pattern.find("{")]
        stop_pattern = self.item_pattern[self.item_pattern.rfind("}")+1:]
        if(Debug): print(start_pattern)
        if(Debug): print(stop_pattern)

        response = requests.get(self.link)
        text = response.text
        data = self.get_item_text(text, start_pattern, stop_pattern)
        item_info = self.parse_items(data)
        for item in item_info:
            self.items.append(self.create_item(item))
