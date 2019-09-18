import datetime
import requests
from RSSItem import RSSItem

Debug = False

class RSSChannel:
    #Required
    title = "Default Title"
    link = "https://www.w3.org/about"
    description = "Default Description"
    
    #Optional
    category = None
    copyright = None
    docs = "http://www.rssboard.org/rss-draft-1"
    generator = "https://github.com/k-barber/RSS-Generator"
    image_link = None
    image_title = None
    image_url = None
    language = "en-us"
    lastBuildDate = None
    managingEditor = None
    pubDate = None
    ttl = 60
    webMaster = None

    #Content
    items = []

    #Item Definition - Required
    item_pattern = None
    item_title = None
    item_link = None
    item_description = None

    #Item Definition - Optional
    item_author = None
    item_category = None
    item_comments = None
    item_enclosure = None
    item_guid = None
    item_pubDate = None
    item_source = None

    def __str__(self):
        output = "    <channel>\n"

        # Required 
        if (self.title is not None):
            output += "        <title>" + self.title + "</title>\n"
        if (self.link is not None):
            output += "        <link>" + self.link.replace("&", "&amp;") + "</link>\n"
        if (self.description is not None):
            output += "        <description>" + self.description + "</description>\n"

        # Optional
        if (self.category is not None):
            output += "        <category>" + self.category + "</category>\n"
        if (self.copyright is not None):
            output += "        <copyright>" + self.copyright + "</copyright>\n"
        if (self.docs is not None):
            output += "        <docs>" + self.docs + "</docs>\n"
        if (self.generator is not None):
            output += "        <generator>" + self.generator + "</generator>\n"
        if (self.image_link is not None and self.image_title is not None and self.image_url is not None):
            output += "        <image>\n"
            output += "            <link>" + self.image_link + "</link>\n"
            output += "            <title>" + self.image_title + "</title>\n"
            output += "            <url>" + self.image_url + "</url>\n"
            output += "        </image>\n"
        if (self.language is not None):
            output += "        <language>" + self.language + "</language>\n"
        if (self.lastBuildDate is not None):
            output += "        <lastBuildDate>" + str(self.lastBuildDate) + "</lastBuildDate>\n"
        if (self.managingEditor is not None):
            output += "        <managingEditor>" + self.managingEditor + "</managingEditor>\n"
        if (self.pubDate is not None):
            output += "        <pubDate>" + str(self.pubDate) + "</pubDate>\n"
        if (self.ttl is not None):
            output += "        <ttl>" + str(self.ttl) + "</ttl>\n"
        if (self.webMaster is not None):
            output += "        <webMaster>" + self.webMaster + "</webMaster>\n"
        
        if (len(self.items) != 0):
            for item in self.items:
                output += str(item)
        output +="    </channel>\n"
        return output

    def print(self):
        #Required
        print("Title: " + str(self.title))
        print("Link: " + str(self.link))
        print("Description: " + str(self.description))

        # Optional
        print("Category: " + str(self.category))
        print("Copyright: " + str(self.copyright))
        print("Docs: " + str(self.docs))
        print("Generator: " + str(self.generator))
        print("Image Link: " + str(self.image_link))
        print("Image Title: " + str(self.image_title))
        print("Image URL: " + str(self.image_url))
        print("Language: " + str(self.language))
        print("Last Build Date: " + str(self.lastBuildDate))
        print("Managing Editor: " + str(self.managingEditor))
        print("Pub Date: " + str(self.pubDate))
        print("TTL: " + str(self.ttl))
        print("Web Master: " + str(self.webMaster))

        #Item Definition - Required
        print("Item_pattern: " + str(self.item_pattern))
        print("Item_title: " + str(self.item_title))
        print("Item_link: " + str(self.item_link))
        print("Item_description: " + str(self.item_description))

        #Item Definition - Optional
        print("Item_author: " + str(self.item_author))
        print("Item_category: " + str(self.item_category))
        print("Item_comments: " + str(self.item_comments))
        print("Item_enclosure: " + str(self.item_enclosure))
        print("item_guid: " + str(self.item_guid))
        print("Item_pubDate: " + str(self.item_pubDate))
        print("Item_source: " + str(self.item_source))

    def create_item(self, data):
        return RSSItem(
            data,
            title=self.item_title,
            link=self.item_link,
            description=self.item_description,
            author=self.item_author,
            category=self.item_category,
            comments=self.item_comments,
            enclosure=self.item_enclosure,
            guid=self.item_guid,
            pubDate=self.item_pubDate,
            source=self.item_source
        )

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

    def __init__(self, data=None):
        self.items = []

        if data is None:
            if (Debug): self.print()
            return

        for line in data:

            semi = line.find(":")
            prefix = line[:semi]

            semi += 1
            
            # Unfortunately, Python does not include Switch

            # Required
            if (prefix == 'title'):
                self.title = self.clean_input(line[semi:])
            elif (prefix =='link'):
                self.link = self.clean_input(line[semi:])
            elif (prefix =='description'):
                self.description = self.clean_input(line[semi:])
            
            # Optional
            elif (prefix =='category'):
                self.category = self.clean_input(line[semi:])
            elif (prefix =='copyright'):
                self.category = self.clean_input(line[semi:])
            elif (prefix =='image_link'):
                self.image_link = self.clean_input(line[semi:])
            elif (prefix =='image_title'):
                self.image_title = self.clean_input(line[semi:])
            elif (prefix =='image_url'):
                self.image_url = self.clean_input(line[semi:])
            elif (prefix =='language'):
                self.language = self.clean_input(line[semi:])
            elif (prefix =='managingEditor'):
                self.managingEditor = self.clean_input(line[semi:])
            elif (prefix =='ttl'):
                self.ttl = self.clean_input(line[semi:])
            elif (prefix =='webMaster'):
                self.webMaster = self.clean_input(line[semi:])
            
            # Item Definition - Required
            elif (prefix =='item_pattern'):
                self.item_pattern = self.clean_input(line[semi:])
            elif (prefix =='item_title'):
                self.item_title = self.clean_input(line[semi:])
            elif (prefix =='item_link'):
                self.item_link = self.clean_input(line[semi:])
            elif (prefix =='item_description'):
                self.item_description = self.clean_input(line[semi:])

            # Item Definition - Optional
            elif (prefix =='item_author'):
                self.item_author = self.clean_input(line[semi:])
            elif (prefix =='item_category'):
                self.item_category = self.clean_input(line[semi:])
            elif (prefix =='item_comments'):
                self.item_comments = self.clean_input(line[semi:])
            elif (prefix =='item_enclosure'):
                self.item_enclosure = self.clean_input(line[semi:])
            elif (prefix =='item_guid'):
                self.item_guid = self.clean_input(line[semi:])
            elif (prefix =='item_pubDate'):
                self.item_pubDate = self.clean_input(line[semi:])
            elif (prefix =='item_source'):
                self.item_source = self.clean_input(line[semi:])
            
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

    def save_channel(self):

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
        self.lastBuildDate = datetime.datetime.now()
        self.pubDate = datetime.datetime.now()

    def test_pattern(self, pattern, text):
        try:
            self.item_pattern = pattern
            first = self.item_pattern.find("{")
            if (first < 0):
                return None
            second = self.item_pattern.rfind("}")+1
            if (second < 1):
                return None
            start_pattern = self.item_pattern[:first]
            stop_pattern = self.item_pattern[second:]
            data = self.get_item_text(text, start_pattern, stop_pattern)
            item_info = self.parse_items(data)
            return item_info
        except:
            return None