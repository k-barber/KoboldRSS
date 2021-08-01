from datetime import datetime
from RSSItem import RSSItem
from Utils import clean_input, create_folders_to_file, dirty_output
import os
import io
import re

Debug = False


class RSSChannel:
    browser_instance = None

    category = None
    copyright = None
    description = None
    path = "Feeds/"
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
    scrape_start_position = None
    item_pattern = None
    scrape_stop_position = None
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

    logged_title = None
    logged_URL = None

    delay = None

    def __str__(self):
        """Produces the xml formatted representation of the object"""
        output = "    <channel>\n"

        # Required
        if self.title is not None:
            output += "        <title>" + dirty_output(self.title) + "</title>\n"
        if self.link is not None:
            output += "        <link>" + dirty_output(self.link) + "</link>\n"
        if self.description is not None:
            output += (
                "        <description>"
                + dirty_output(self.description)
                + "</description>\n"
            )

        # Optional
        if self.category is not None:
            for cat in self.category:
                output += "        <category>" + dirty_output(cat) + "</category>\n"
        if self.copyright is not None:
            output += (
                "        <copyright>" + dirty_output(self.copyright) + "</copyright>\n"
            )
        if self.docs is not None:
            output += "        <docs>" + dirty_output(self.docs) + "</docs>\n"
        if self.generator is not None:
            output += (
                "        <generator>" + dirty_output(self.generator) + "</generator>\n"
            )
        if (
            self.image_link is not None
            and self.image_title is not None
            and self.image_url is not None
        ):
            output += "        <image>\n"
            output += "            <link>" + dirty_output(self.image_link) + "</link>\n"
            output += (
                "            <title>" + dirty_output(self.image_title) + "</title>\n"
            )
            output += "            <url>" + dirty_output(self.image_url) + "</url>\n"
            output += "        </image>\n"
        if self.language is not None:
            output += (
                "        <language>" + dirty_output(self.language) + "</language>\n"
            )
        if self.lastBuildDate is not None:
            output += (
                "        <lastBuildDate>"
                + dirty_output(str(self.lastBuildDate))
                + "</lastBuildDate>\n"
            )
        if self.managingEditor is not None:
            output += (
                "        <managingEditor>"
                + dirty_output(self.managingEditor)
                + "</managingEditor>\n"
            )
        if self.pubDate is not None:
            output += (
                "        <pubDate>" + dirty_output(str(self.pubDate)) + "</pubDate>\n"
            )
        if self.ttl is not None:
            output += "        <ttl>" + dirty_output(str(self.ttl)) + "</ttl>\n"
        if self.webMaster is not None:
            output += (
                "        <webMaster>" + dirty_output(self.webMaster) + "</webMaster>\n"
            )

        if len(self.items) != 0:
            for item in self.items:
                output += str(item)
        output += "    </channel>\n"
        return output

    def print(self):
        """Prints information about channel to STDout"""
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
        print("Start: " + str(self.scrape_start_position))
        print("Item_pattern: " + str(self.item_pattern))
        print("Stop: " + str(self.scrape_stop_position))
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

    def create_item(self, data):
        """generates an RSS Item

        Parameters:

        data (list): the fields of an item in the form [{%1}, {%2}, ...]
        """
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
            source=self.item_source,
        )

    def __init__(self, data=None, browser_instance=None):
        """generates an RSS Channel

        Parameters:

        data (string list): the variables of a channel in the format:
            item_title:{%6}
            language:en-ca
            link:https://google.com
            title:Google.com Feed
            ttl:30
        """
        self.items = []

        if data is None:
            if Debug:
                self.print()
            return

        for line in data:

            semi = line.find(":")
            prefix = line[:semi]

            semi += 1

            # Unfortunately, Python does not include Switch

            if prefix == "category":
                cats = clean_input(line[semi:]).split(",")
                self.category = [cat.strip() for cat in cats]
            elif prefix == "copyright":
                self.copyright = clean_input(line[semi:])
            elif prefix == "description":
                self.description = clean_input(line[semi:])
            elif prefix == "path":
                self.path = clean_input(line[semi:])

            elif prefix == "enclosure_length":
                self.enclosure_length = clean_input(line[semi:])
            elif prefix == "enclosure_type":
                self.enclosure_type = clean_input(line[semi:])
            elif prefix == "enclosure_url":
                self.enclosure_url = clean_input(line[semi:])

            elif prefix == "image_link":
                self.image_link = clean_input(line[semi:])
            elif prefix == "image_title":
                self.image_title = clean_input(line[semi:])
            elif prefix == "image_url":
                self.image_url = clean_input(line[semi:])

            elif prefix == "item_author":
                self.item_author = clean_input(line[semi:])
            elif prefix == "item_category":
                self.item_category = clean_input(line[semi:])
            elif prefix == "item_comments":
                self.item_comments = clean_input(line[semi:])
            elif prefix == "item_description":
                self.item_description = clean_input(line[semi:])
            elif prefix == "item_guid":
                self.item_guid = clean_input(line[semi:])
            elif prefix == "item_link":
                self.item_link = clean_input(line[semi:])
            elif prefix == "scrape_start_position":
                self.scrape_start_position = clean_input(line[semi:])
            elif prefix == "item_pattern":
                self.item_pattern = clean_input(line[semi:])
            elif prefix == "scrape_stop_position":
                self.scrape_stop_position = clean_input(line[semi:])
            elif prefix == "item_pubDate":
                self.item_pubDate = clean_input(line[semi:])
            elif prefix == "item_source":
                self.item_source = clean_input(line[semi:])
            elif prefix == "item_title":
                self.item_title = clean_input(line[semi:])

            elif prefix == "language":
                self.language = clean_input(line[semi:])
            elif prefix == "link":
                self.link = clean_input(line[semi:])
            elif prefix == "managingEditor":
                self.managingEditor = clean_input(line[semi:])
            elif prefix == "title":
                self.title = clean_input(line[semi:])
            elif prefix == "ttl":
                self.ttl = clean_input(line[semi:])
            elif prefix == "webMaster":
                self.webMaster = clean_input(line[semi:])

            elif prefix == "logged_title":
                self.logged_title = clean_input(line[semi:])
            elif prefix == "logged_URL":
                self.logged_URL = clean_input(line[semi:])

            elif prefix == "delay":
                self.delay = int(clean_input(line[semi:]))

            elif prefix == "last_build_date":
                self.lastBuildDate = datetime.fromtimestamp(
                    float(clean_input(line[semi:]))
                )

        if Debug:
            self.print()

    def generate_items(self, text, test=False):
        """Creates a list of items from the given text and item pattern

        Parameters:

        text (string): the text to scrape for items
        """

        partial_text = clean_input(text)
        
        if (
            (self.scrape_start_position is not None)
            and (self.scrape_start_position != "")
            and (partial_text.find(self.scrape_start_position) > -1)
        ):
            partial_text = partial_text[
                partial_text.find(self.scrape_start_position)
                + len(self.scrape_start_position) :
            ]

        if (
            (self.scrape_stop_position is not None)
            and (self.scrape_stop_position != "")
            and (partial_text.find(self.scrape_stop_position) > -1)
        ):
            partial_text = partial_text[: partial_text.find(self.scrape_stop_position)]
        
        try:
            re.compile(self.item_pattern)
        except re.error:
            return "ERROR"

        try:
            result = re.findall(self.item_pattern, partial_text, re.DOTALL)
        except Exception as err:
            exception_type = type(err).__name__
            print(exception_type)


        # Remove leading and trailing whitespace from matches
        stripped = []
        for match in result:
            if type(match) is tuple:
                stripped.append(tuple(group.strip() for group in match))
            else:
                stripped.append(tuple([match]))

        if test == True:
            return stripped

        self.items = []
        output = []

        for item_data in stripped:
            rss_item = self.create_item(item_data)
            self.items.append(rss_item)
            output.append(rss_item.toJSON())

        self.lastBuildDate = datetime.now()
        self.pubDate = datetime.now()

        return output

    def test_definition(self, pattern, text, title, link, description):
        if pattern == None:
            return
        if link == "https://www.w3.org/about":
            return
        self.item_pattern = pattern
        if Debug:
            print("Item Pattern: '" + self.item_pattern + "'")

        self.item_title = title
        self.item_link = link
        self.item_description = description
        items = self.generate_items(clean_input(text))
        return items[:3]

    def save_channel(self):
        """Creates the xml file of the channel"""

        output = """<?xml version="1.0" encoding="utf-8"?>\n<?xml-stylesheet type="text/xsl" href="/res/preview.xsl"?>\n<rss version="2.0">"""
        output += "\n" + str(self)

        output += "</rss>"

        file_name = os.path.join(
            self.path, self.title.replace(":", "~").replace(" ", "_") + ".xml"
        )

        create_folders_to_file(file_name)

        f = open(file_name, "wb")
        f.write(str.encode(output))
        f.close()

    def clear(self):
        """clear all the variables"""
        self.category = None
        self.copyright = None
        self.description = None
        self.path = None
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
        self.scrape_start_position = None
        self.item_pattern = None
        self.scrape_stop_position = None
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

        self.logged_title = None
        self.logged_URL = None

    def print_definition(self):
        """Produce a string representation of the channel for use in Feed_Definitions.txt"""
        output = ""

        if self.category is not None:
            output += "category:"
            for cat in self.category:
                output += cat + ","
            output = output[:-1]
            output += "\n"
        if self.copyright is not None:
            output += "copyright:" + self.copyright + "\n"
        if self.description is not None:
            output += "description:" + self.description + "\n"
        if self.path is not None:
            output += "path:" + self.path + "\n"

        if self.enclosure_length is not None:
            output += "enclosure_length:" + self.enclosure_length + "\n"
        if self.enclosure_type is not None:
            output += "enclosure_type:" + self.enclosure_type + "\n"
        if self.enclosure_url is not None:
            output += "enclosure_url:" + self.enclosure_url + "\n"

        if (
            self.image_link is not None
            and self.image_title is not None
            and self.image_url is not None
        ):
            output += "image_link:" + self.image_link + "\n"
            output += "image_title:" + self.image_title + "\n"
            output += "image_url:" + self.image_url + "\n"

        if self.item_author is not None:
            output += "item_author:" + self.item_author + "\n"
        if self.item_category is not None:
            output += "item_category:" + self.item_category + "\n"
        if self.item_comments is not None:
            output += "item_comments:" + self.item_comments + "\n"
        if self.item_description is not None:
            output += "item_description:" + self.item_description + "\n"
        if self.item_guid is not None:
            output += "item_guid:" + self.item_guid + "\n"
        if self.item_link is not None:
            output += "item_link:" + self.item_link + "\n"
        if self.scrape_start_position is not None:
            output += "scrape_start_position:" + self.scrape_start_position + "\n"
        if self.item_pattern is not None:
            output += "item_pattern:" + self.item_pattern + "\n"
        if self.scrape_stop_position is not None:
            output += "scrape_stop_position:" + self.scrape_stop_position + "\n"
        if self.item_pubDate is not None:
            output += "item_pubDate:" + self.item_pubDate + "\n"
        if self.item_source is not None:
            output += "item_source:" + self.item_source + "\n"
        if self.item_title is not None:
            output += "item_title:" + self.item_title + "\n"

        if self.language is not None:
            output += "language:" + self.language + "\n"
        if self.link is not None:
            output += "link:" + self.link + "\n"
        if self.managingEditor is not None:
            output += "managingEditor:" + self.managingEditor + "\n"
        if self.title is not None:
            output += "title:" + self.title + "\n"
        if self.ttl is not None:
            output += "ttl:" + str(self.ttl) + "\n"
        if self.webMaster is not None:
            output += "webMaster:" + self.webMaster + "\n"

        if self.logged_title is not None:
            output += "logged_title:" + self.logged_title + "\n"
        if self.logged_URL is not None:
            output += "logged_URL:" + str(self.logged_URL) + "\n"

        if (self.delay is not None) and (self.delay != 0):
            output += "delay:" + str(self.delay) + "\n"

        if self.lastBuildDate is not None:
            output += (
                "last_build_date:" + str(datetime.timestamp(self.lastBuildDate)) + "\n"
            )

        return output
