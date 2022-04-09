from Utils import dirty_output, unicoding, ampersanding
import re


class RSSItem:
    author = None
    category = None
    comments = None
    data = None
    description = "Default Description"

    enclosure_length = None
    enclosure_type = None
    enclosure_url = None

    guid = None
    link = "https://www.w3.org/about"
    pubDate = None
    source = None
    title = "Default Title"

    def replace(self):
        for index, value in enumerate(self.data):
            if self.author is not None:
                self.author = self.author.replace("{%" + str(index + 1) + "}", value)
            if self.category is not None:
                self.category = self.category.replace(
                    "{%" + str(index + 1) + "}", value
                )
            if self.comments is not None:
                self.comments = self.comments.replace(
                    "{%" + str(index + 1) + "}", value
                )
            if self.description is not None:
                self.description = self.description.replace(
                    "{%" + str(index + 1) + "}", value
                )

            if self.enclosure_length is not None:
                self.enclosure_length = self.enclosure_length.replace(
                    "{%" + str(index + 1) + "}", value
                )
            if self.enclosure_type is not None:
                self.enclosure_type = self.enclosure_type.replace(
                    "{%" + str(index + 1) + "}", value
                )
            if self.enclosure_url is not None:
                self.enclosure_url = self.enclosure_url.replace(
                    "{%" + str(index + 1) + "}", value
                )

            if self.guid is not None:
                self.guid = self.guid.replace("{%" + str(index + 1) + "}", value)
            if self.link is not None:
                self.link = self.link.replace("{%" + str(index + 1) + "}", value)
            if self.pubDate is not None and isinstance(self.pubDate, str):
                self.pubDate = self.pubDate.replace("{%" + str(index + 1) + "}", value)
            if self.source is not None:
                self.source = self.source.replace("{%" + str(index + 1) + "}", value)
            if self.title is not None:
                self.title = self.title.replace("{%" + str(index + 1) + "}", value)
        if self.category is not None:
            cats = self.category.split(",")
            self.category = [cat.strip() for cat in cats]

        result = re.search(r"<base href=[\"'](.*?)[\"'].*?>", self.description)
        if result:
            print("FOUND")
            self.description = self.description.replace(result.group(0), "")
            print(self.description)
            url = result.group(1)
            print(url)
            self.description = re.sub(r"href=[\"']", 'href="' + url, self.description)
            print(self.description)

        # if (self.author is not None and re.search(r"{%\d}", self.author)) or\
        #    (self.category is not None and re.search(r"{%\d}", self.category)) or\
        #    (self.comments is not None and re.search(r"{%\d}", self.comments)) or\
        #    (self.description is not None and re.search(r"{%\d}", self.description)) or\
        #    (self.enclosure_length is not None and re.search(r"{%\d}", self.enclosure_length)) or\
        #    (self.enclosure_type is not None and re.search(r"{%\d}", self.enclosure_type)) or\
        #    (self.enclosure_url is not None and re.search(r"{%\d}", self.enclosure_url)) or\
        #    (self.guid is not None and re.search(r"{%\d}", self.guid)) or\
        #    (self.link is not None and re.search(r"{%\d}", self.link)) or\
        #    (self.pubDate is not None and re.search(r"{%\d}", self.pubDate)) or\
        #    (self.source is not None and re.search(r"{%\d}", self.source)) or\
        #    (self.title is not None and re.search(r"{%\d}", self.title)):
        #        print("Error")

    def __init__(
        self,
        data,
        title=None,
        link=None,
        description=None,
        author=None,
        category=None,
        comments=None,
        guid=None,
        pubDate=None,
        source=None,
        enclosure_url=None,
        enclosure_length=None,
        enclosure_type=None,
    ):
        self.author = author
        self.category = category
        self.comments = comments
        self.data = data
        self.description = description

        self.enclosure_length = enclosure_length
        self.enclosure_type = enclosure_type
        self.enclosure_url = enclosure_url

        self.guid = guid
        self.link = link
        self.pubDate = pubDate
        self.source = source
        self.title = title

        self.replace()

    def toJSON(self):
        json_representation = {
            "author": self.author,
            "category": self.category,
            "comments": self.comments,
            "data": self.data,
            "description": self.description,
            "enclosure_length": self.enclosure_length,
            "enclosure_type": self.enclosure_type,
            "enclosure_url": self.enclosure_url,
            "guid": self.guid,
            "link": self.link,
            "pubDate": self.pubDate,
            "source": self.source,
            "title": self.title,
        }

        return json_representation

    def __str__(self):
        output = "        <item>\n"
        if self.author is not None:
            output += "            <author>" + dirty_output(self.author) + "</author>\n"
        if self.category is not None:
            for cat in self.category:
                output += "            <category>" + dirty_output(cat) + "</category>\n"
        if self.comments is not None:
            output += (
                "            <comments>" + dirty_output(self.comments) + "</comments>\n"
            )
        if self.description is not None:
            if self.description.startswith("<![CDATA["):
                output += (
                    "            <description>"
                    + ampersanding(unicoding(self.description))
                    + "</description>\n"
                )
            else:
                output += (
                    "            <description>"
                    + ampersanding(unicoding(self.description))
                    + "</description>\n"
                )

        if (
            self.enclosure_url is not None
            and self.enclosure_length is not None
            and self.enclosure_type is not None
        ):
            output += (
                '            <enclosure url="'
                + dirty_output(self.enclosure_url)
                + '" length="'
                + dirty_output(self.enclosure_length)
                + '" type="'
                + dirty_output(self.enclosure_type)
                + '" />\n'
            )

        if self.guid is not None:
            output += "            <guid>" + dirty_output(self.guid) + "</guid>\n"
        if self.link is not None:
            output += "            <link>" + dirty_output(self.link) + "</link>\n"
        if self.pubDate is not None:
            output += (
                "            <pubDate>"
                + dirty_output(str(self.pubDate))
                + "</pubDate>\n"
            )
        if self.source is not None:
            output += "            <source>" + dirty_output(self.source) + "</source>\n"
        if self.title is not None:
            output += "            <title>" + dirty_output(self.title) + "</title>\n"
        output += "        </item>\n"
        return output
