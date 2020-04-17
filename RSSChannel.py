import datetime
import requests
from time import sleep
from RSSItem import RSSItem
from Utils import clean_input, dirty_output, log
import login_utils

Debug = False

class RSSChannel:
    category = None
    copyright = None
    description = "Default Description"
    docs = "http://www.rssboard.org/rss-draft-1"

    enclosure_length = None
    enclosure_type = None
    enclosure_url = None

    generator = "https://github.com/k-barber/RSS-Generator"

    image_link = None
    image_title = None
    image_url = None

    items = []
    item_author = None
    item_category = None
    item_comments = None
    item_description = None
    item_guid = None
    item_link = None
    item_pattern = None
    item_pubDate = None
    item_source = None
    item_title = None

    language = "en-us"
    lastBuildDate = None
    link = "https://www.w3.org/about"
    managingEditor = None
    pubDate = None
    title = "Default Title"
    ttl = 60
    webMaster = None

    username = None
    password = None
    website = None

    def __str__(self):
        output = "    <channel>\n"

        # Required 
        if (self.title is not None):
            output += "        <title>" + dirty_output(self.title) + "</title>\n"
        if (self.link is not None):
            output += "        <link>" + dirty_output(self.link) + "</link>\n"
        if (self.description is not None):
            output += "        <description>" + dirty_output(self.description) + "</description>\n"

        # Optional
        if (self.category is not None):
            for cat in self.category:
                output += "        <category>" + dirty_output(cat) + "</category>\n"
        if (self.copyright is not None):
            output += "        <copyright>" + dirty_output(self.copyright) + "</copyright>\n"
        if (self.docs is not None):
            output += "        <docs>" + dirty_output(self.docs) + "</docs>\n"
        if (self.generator is not None):
            output += "        <generator>" + dirty_output(self.generator) + "</generator>\n"
        if (self.image_link is not None and self.image_title is not None and self.image_url is not None):
            output += "        <image>\n"
            output += "            <link>" + dirty_output(self.image_link) + "</link>\n"
            output += "            <title>" + dirty_output(self.image_title) + "</title>\n"
            output += "            <url>" + dirty_output(self.image_url) + "</url>\n"
            output += "        </image>\n"
        if (self.language is not None):
            output += "        <language>" + dirty_output(self.language) + "</language>\n"
        if (self.lastBuildDate is not None):
            output += "        <lastBuildDate>" + dirty_output(str(self.lastBuildDate)) + "</lastBuildDate>\n"
        if (self.managingEditor is not None):
            output += "        <managingEditor>" + dirty_output(self.managingEditor) + "</managingEditor>\n"
        if (self.pubDate is not None):
            output += "        <pubDate>" + dirty_output(str(self.pubDate)) + "</pubDate>\n"
        if (self.ttl is not None):
            output += "        <ttl>" + dirty_output(str(self.ttl)) + "</ttl>\n"
        if (self.webMaster is not None):
            output += "        <webMaster>" + dirty_output(self.webMaster) + "</webMaster>\n"
        
        if (len(self.items) != 0):
            for item in self.items:
                output += str(item)
        output +="    </channel>\n"
        return output

    def print(self):
        print("Category: " + str(self.category))
        print("Copyright: " + str(self.copyright))
        print("Description: " + str(self.description))
        print("Docs: " + str(self.docs))

        print("Enclosure_length: " + str(self.enclosure_length))
        print("Enclosure_type: " + str(self.enclosure_type))
        print("Enclosure_url: " + str(self.enclosure_url))

        print("Generator: " + str(self.generator))

        print("Image Link: " + str(self.image_link))
        print("Image Title: " + str(self.image_title))
        print("Image URL: " + str(self.image_url))

        print("Item_author: " + str(self.item_author))
        print("Item_category: " + str(self.item_category))
        print("Item_comments: " + str(self.item_comments))
        print("Item_description: " + str(self.item_description))
        print("item_guid: " + str(self.item_guid))
        print("Item_link: " + str(self.item_link))
        print("Item_pattern: " + str(self.item_pattern))
        print("Item_pubDate: " + str(self.item_pubDate))
        print("Item_source: " + str(self.item_source))
        print("Item_title: " + str(self.item_title))
        
        print("Language: " + str(self.language))
        print("Last Build Date: " + str(self.lastBuildDate))
        print("Link: " + str(self.link))
        print("Managing Editor: " + str(self.managingEditor))
        print("Pub Date: " + str(self.pubDate))
        print("Title: " + str(self.title))
        print("TTL: " + str(self.ttl))
        print("Web Master: " + str(self.webMaster))

        print("Website: " + str(self.website))
        print("Username: " + str(self.username))        

    def create_item(self, data):
        return RSSItem(
            data,
            title=self.item_title,
            link=self.item_link,
            description=self.item_description,
            author=self.item_author,
            category=self.item_category,
            comments=self.item_comments,
            enclosure_length=self.enclosure_length,
            enclosure_type=self.enclosure_type,
            enclosure_url=self.enclosure_url,
            guid=self.item_guid,
            pubDate=self.item_pubDate,
            source=self.item_source
        )

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
            
            if (prefix =='category'):
                cats = clean_input(line[semi:]).split(",")
                self.category = [cat.strip() for cat in cats]
            elif (prefix =='copyright'):
                self.copyright = clean_input(line[semi:])
            elif (prefix =='description'):
                self.description = clean_input(line[semi:])
            

            elif (prefix =='enclosure_length'):
                self.enclosure_length = clean_input(line[semi:])
            elif (prefix =='enclosure_type'):
                self.enclosure_type = clean_input(line[semi:])
            elif (prefix =='enclosure_url'):
                self.enclosure_url = clean_input(line[semi:])


            elif (prefix =='image_link'):
                self.image_link = clean_input(line[semi:])
            elif (prefix =='image_title'):
                self.image_title = clean_input(line[semi:])
            elif (prefix =='image_url'):
                self.image_url = clean_input(line[semi:])


            elif (prefix =='item_author'):
                self.item_author = clean_input(line[semi:])
            elif (prefix =='item_category'):
                self.item_category = clean_input(line[semi:])
            elif (prefix =='item_comments'):
                self.item_comments = clean_input(line[semi:])
            elif (prefix =='item_description'):
                self.item_description = clean_input(line[semi:])
            elif (prefix =='item_guid'):
                self.item_guid = clean_input(line[semi:])
            elif (prefix =='item_link'):
                self.item_link = clean_input(line[semi:])
            elif (prefix =='item_pattern'):
                self.item_pattern = clean_input(line[semi:])
            elif (prefix =='item_pubDate'):
                self.item_pubDate = clean_input(line[semi:])
            elif (prefix =='item_source'):
                self.item_source = clean_input(line[semi:])
            elif (prefix =='item_title'):
                self.item_title = clean_input(line[semi:])

            elif (prefix =='language'):
                self.language = clean_input(line[semi:])
            elif (prefix =='link'):
                self.link = clean_input(line[semi:])
            elif (prefix =='managingEditor'):
                self.managingEditor = clean_input(line[semi:])
            elif (prefix == 'title'):
                self.title = clean_input(line[semi:])
            elif (prefix =='ttl'):
                self.ttl = clean_input(line[semi:])
            elif (prefix =='webMaster'):
                self.webMaster = clean_input(line[semi:])

            elif (prefix =='username'):
                self.username = clean_input(line[semi:])
            elif (prefix =='website'):
                self.website = clean_input(line[semi:])
            elif (prefix =='password'):
                self.password = clean_input(line[semi:])

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

    def parse_item_text(self, item_text, pattern = None):
        if (Debug): print("Parsing Item Text")
        if (pattern is None):
            if (self.item_pattern is None):
                return
            item_pattern = self.item_pattern
        else:
            item_pattern = pattern
        output = []
        Left_capture_pattern_start_index = 0 #The position in the pattern
        capture_search_start_index = 0 #The position in the text

        num_fields_total = item_pattern.count("{%}")
        num_fields_captured = 0
        if (Debug): print("Total Fields: '" + str(num_fields_total) + "'")
        if (Debug): print("Item Text: '" + item_text + "'")
        if (Debug): print("Item Pattern: '" + item_pattern + "'")
        while(capture_search_start_index >= 0):
            if (Debug): print("==========================================")
            if (Debug): print("Left Capture Pattern Start Index: '" + str(Left_capture_pattern_start_index) + "'")
            Left_capture_pattern_stop_index = item_pattern.find("{", Left_capture_pattern_start_index)
            if (Debug): print("Left Capture Pattern Stop Index: '" + str(Left_capture_pattern_stop_index) + "'")
            Left_capture_pattern = item_pattern[Left_capture_pattern_start_index:Left_capture_pattern_stop_index]
            if (Debug): print("Left Capture Pattern: '" + Left_capture_pattern + "'")
            
            right_capture_pattern_start_index = item_pattern.find("}", Left_capture_pattern_stop_index)+1
            if (Debug): print("Right Capture Pattern Start Index: '" + str(right_capture_pattern_start_index) + "'")
            right_capture_pattern_stop_index = item_pattern.find("{", right_capture_pattern_start_index)
            if (Debug): print("Right Capture Pattern Stop Index: : '" + str(right_capture_pattern_stop_index) + "'")

            if (right_capture_pattern_stop_index > 0):
                right_capture_pattern = item_pattern[right_capture_pattern_start_index:right_capture_pattern_stop_index]
            else:
                right_capture_pattern = item_pattern[right_capture_pattern_start_index:]

            if (Debug): print("Right Capture Pattern: '" + right_capture_pattern + "'")

            capture_character = item_pattern[Left_capture_pattern_stop_index+1]
            if (Debug): print("Capture Character: '" + capture_character + "'")

            if (Debug): print("Capture Search Start Index: '" + str(capture_search_start_index) + "'")

            left_capture_pattern_found = item_text.find(Left_capture_pattern, capture_search_start_index)
            if (left_capture_pattern_found >= 0):
                capture_start_index =  left_capture_pattern_found + len(Left_capture_pattern)
            else :
                capture_start_index = -1
            if (Debug): print("Capture Start Index: '" + str(capture_start_index) + "'")

            capture_end_index = item_text.find(right_capture_pattern, capture_start_index)
            if (Debug): print("Capture End Index: '" + str(capture_end_index) + "'")

            if (left_capture_pattern_found >= 0 & capture_end_index >= 0):
                capture_search_start_index = capture_end_index
            if (capture_character == "%"):
                if (left_capture_pattern_found >= 0):
                    captured = clean_input(item_text[capture_start_index:capture_end_index])
                    if (Debug): print("Captured: '" + captured + "'")
                    output.append(captured)
                else:
                    output.append("")
                num_fields_captured += 1
            if (Debug): print(str(num_fields_captured) + " of " + str(num_fields_total) + " fields captured")
            if (num_fields_captured == num_fields_total):
                capture_search_start_index = -1
            Left_capture_pattern_start_index = right_capture_pattern_start_index
            if (Debug): print("==========================================")
        return output

    def parse_items(self, data, pattern = None):
        if (Debug): print("Parsing Items")
        output = []
        for text in data:
            output.append(self.parse_item_text(text, pattern))
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
        start = self.item_pattern.find("{")
        stop = self.item_pattern.rfind("}")
        if(start == -1 or stop == -1):
            return
        start_pattern = self.item_pattern[:start]
        stop_pattern = self.item_pattern[stop+1:]
        if(Debug): print(start_pattern)
        if(Debug): print(stop_pattern)

        if ((self.website is not None) & (self.username is not None) & (self.password is not None)):
            text = login_utils.multi_scrape(self.username, self.password, self.website, self.link)
            if (Debug): print(text)
            data = self.get_item_text(clean_input(text), start_pattern, stop_pattern)
            item_info = self.parse_items(data)
            for item in item_info:
                self.items.append(self.create_item(item))
            self.lastBuildDate = datetime.datetime.now()
            self.pubDate = datetime.datetime.now()
        else:
            response = None
            timer = 1
            count = 0
            while (response is None):
                try:
                    response = requests.get(self.link, headers = {'User-agent': 'RSS Generator Bot'})
                    text = response.text
                    if(Debug): print(text)
                    data = self.get_item_text(clean_input(text), start_pattern, stop_pattern)
                    item_info = self.parse_items(data)
                    for item in item_info:
                        self.items.append(self.create_item(item))
                    self.lastBuildDate = datetime.datetime.now()
                    self.pubDate = datetime.datetime.now()
                except Exception as err:
                    log("ERROR:")
                    log(str(err))
                    log("Retrying in " + str(timer) + " seconds.")
                    sleep(timer)
                    timer = timer * 2
                    if (count == 6):
                        break
                    else:
                        count += 1

    def test_pattern(self, pattern, text):
        try:
            self.item_pattern = clean_input(pattern)
            if(Debug): print("Item Pattern: '" + self.item_pattern + "'")
            first = self.item_pattern.find("{")
            if (first < 0):
                return None
            second = self.item_pattern.rfind("}")
            if (second < 0):
                return None
            start_pattern = self.item_pattern[:first]
            stop_pattern = self.item_pattern[second+1:]
            if(Debug): print("Start pattern: '" + start_pattern + "'")
            if(Debug): print("Stop pattern: '" + stop_pattern + "'")
            data = self.get_item_text(clean_input(text), start_pattern, stop_pattern)
            #if(Debug): print(data)
            item_info = self.parse_items(data)
            return item_info
        except Exception as e:
            print(e)
            return None

    def test_definition(self, pattern, text, title, link, description):
        if (pattern == None):
            return
        if (link == "https://www.w3.org/about"):
            return
        self.item_pattern = clean_input(pattern)
        if(Debug): print("Item Pattern: '" + self.item_pattern + "'")
        first = self.item_pattern.find("{")
        if (first < 0):
            return None
        second = self.item_pattern.rfind("}")
        if (second < 0):
            return None
        start_pattern = self.item_pattern[:first]
        stop_pattern = self.item_pattern[second+1:]
        if(Debug): print("Start pattern: '" + start_pattern + "'")
        if(Debug): print("Stop pattern: '" + stop_pattern + "'")
        data = self.get_item_text(clean_input(text), start_pattern, stop_pattern)
        if(Debug): print(data[0])
        item_info = self.parse_items(data[:3])
        if(Debug): print(item_info)
        iterator = 0
        items = []
        for item in item_info:
            items.append(RSSItem(
                    item,
                    title=title,
                    link=link,
                    description=description).toJSON())
        if(Debug): print(items)
        if (Debug): print("Test complete")
        return items

    def clear(self):
        self.category = None
        self.copyright = None
        self.description = "Default Description"
        self.docs = "http://www.rssboard.org/rss-draft-1"

        self.enclosure_length = None
        self.enclosure_type = None
        self.enclosure_url = None

        self.generator = "https://github.com/k-barber/RSS-Generator"

        self.image_link = None
        self.image_title = None
        self.image_url = None

        self.items = []
        self.item_author = None
        self.item_category = None
        self.item_comments = None
        self.item_description = None
        self.item_guid = None
        self.item_link = None
        self.item_pattern = None
        self.item_pubDate = None
        self.item_source = None
        self.item_title = None
        
        self.language = "en-us"
        self.lastBuildDate = None
        self.link = "https://www.w3.org/about"
        self.managingEditor = None
        self.pubDate = None
        self.title = "Default Title"
        self.ttl = 60
        self.webMaster = None

        self.username = None
        self.website = None
        self.password = None

    def print_definition(self):
        output = ""
        
        if (self.category is not None):
            output += "category:"
            for cat in self.category:
                output += cat + ","
            output = output[:-1]
            output += "\n"
        if (self.copyright is not None):
            output += "copyright:" + self.copyright + "\n"
        if (self.description is not None):
            output += "description:" + self.description + "\n"


        if (self.enclosure_length is not None):
            output += "enclosure_length:" + self.enclosure_length + "\n"
        if (self.enclosure_type is not None):
            output += "enclosure_type:" + self.enclosure_type + "\n"
        if (self.enclosure_url is not None):
            output += "enclosure_url:" + self.enclosure_url + "\n"

        if (self.image_link is not None and self.image_title is not None and self.image_url is not None):
            output += "image_link:" + self.image_link + "\n"
            output += "image_title:" + self.image_title + "\n"
            output += "image_url:" + self.image_url + "\n"


        if (self.item_author is not None):
            output += "item_author:" + self.item_author + "\n"
        if (self.item_category is not None):
            output += "item_category:" + self.item_category + "\n"
        if (self.item_comments is not None):
            output += "item_comments:" + self.item_comments + "\n"
        if (self.item_description is not None):
            output += "item_description:" + self.item_description + "\n"
        if (self.item_guid is not None):
            output += "item_guid:" + self.item_guid + "\n"
        if (self.item_link is not None):
            output += "item_link:" + self.item_link + "\n"
        if (self.item_pattern is not None):
            output += "item_pattern:" + self.item_pattern + "\n"
        if (self.item_pubDate is not None):
            output += "item_pubDate:" + self.item_pubDate + "\n"
        if (self.item_source is not None):
            output += "item_source:" + self.item_source + "\n"
        if (self.item_title is not None):
            output += "item_title:" + self.item_title + "\n"
        
        
        if (self.language is not None):
            output += "language:" + self.language + "\n"
        if (self.link is not None):
            output += "link:" + self.link + "\n"
        if (self.managingEditor is not None):
            output += "managingEditor:" + self.managingEditor + "\n"
        if (self.title is not None):
            output += "title:" + self.title + "\n"
        if (self.ttl is not None):
            output += "ttl:" + str(self.ttl) + "\n"
        if (self.webMaster is not None):
            output += "webMaster:" + self.webMaster + "\n"

        if (self.website is not None):
            output += "website:" + self.website + "\n"
        if (self.username is not None):
            output += "username:" + str(self.username) + "\n"
        if (self.password is not None):
            output += "password:" + self.password + "\n"

        return output