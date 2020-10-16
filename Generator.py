import requests
import itertools as it
from RSSChannel import RSSChannel
from datetime import datetime, timedelta
import os
import time
import sys

top = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="/Pages/styles.css">
    <title>RSS-Generator: Feeds</title>
</head>

<body>
    <a href="/"><img src="/Img/Bocchi.png" id="bocchi"/></a>
    <div id="container">
        <div>
            <a href="http://www.rssboard.org/rss-draft-1" target="_blank"><img id="icon" src="/Img/RSS.png"></a>
            <p><a href="/">Home</a> &gt; My Feeds</p>
            <h1>K-Barber's RSS-Generator: My Feeds</h1>
            <p>A list of your feeds:</p>
            <ul>
'''

bottom = '''
            </ul>
            <button onclick="refresh()">Refresh</button>
        </div>
    </div>
    <script>
        function refresh() {
            location.reload(true);
        }
    </script>
</body>
</html>
'''

class GeneratorInstance:

    debug_mode = False
    shell = None
    chrome_instance = None
    stop_event = None
    start_time = None
    channels = []

    def log(self, text):
        self.shell.print_generator_output(text)

    def __init__(self, shell_param, debug, chrome_instance):
        self.debug_mode = debug
        self.shell = shell_param
        self.chrome_instance = chrome_instance
        self.start_time = datetime.now()
        self.log("Generator starts")
        self.create_channels()

    def index_channels(self):
        global channels
        f = open("Pages/Feeds.html", "wb")
        output = top
        for channel in self.channels:
            title = channel.title.replace(":", "~").replace(" ", "_")
            output += '''                <li>
                        <a href="/Feeds/''' + title + '.xml">' + title + '''.xml</a>
                    </li>
    '''
        output += bottom
        f.write(str.encode(output))
        f.close()

    def quit(self):
        print("Generator shutting down")
        self.stop_event.set()


    def create_channels(self):
        self.channels = []
        if self.debug_mode: self.log("Feed_Definitions.txt defines the following:")
        with open('Feed_Definitions.txt') as fp:
            for key, group in it.groupby(fp, lambda line: line.startswith('~-~-~-~-')):
                if not key:
                    group = list(group)
                    channel = RSSChannel(group)
                    if self.debug_mode: self.log(channel.title)
                    self.channels.append(channel)

    def check_for_updates(self):
        now = datetime.now()
        modified = datetime.fromtimestamp(os.path.getmtime('Feed_Definitions.txt'))
        if (modified >= self.start_time):
            self.log("Feed Definitions have been updated, regenerating feed list")
            self.start_time = now
            self.create_channels()

    def update_channels(self, stop_signal, generator_stopped_signal):
        now = datetime.now()
        self.log("Updating Channels")
        for channel in self.channels:
            if(not stop_signal.is_set()):
                if (channel.lastBuildDate is not None):
                    if (now >= channel.lastBuildDate + timedelta(minutes=int(channel.ttl))):
                        self.generate_items(channel)
                else:
                    self.generate_items(channel)
        if (stop_signal.is_set()):
            self.log("Cancelled Update")
            generator_stopped_signal.set()
        else:
            self.log("Updating in 5 Minutes")

    def generate_items(self, channel):
        text = ""
        self.log("Updating " + channel.title)
        
        if ((channel.website is not None) & (channel.username is not None) & (channel.password is not None)):
            if (channel.delay is not None):
                text = self.chrome_instance.multi_scrape(channel.username, channel.password, channel.website, channel.link, delay=channel.delay)
            else:
                text = self.chrome_instance.multi_scrape(channel.username, channel.password, channel.website, channel.link)
            if (self.debug_mode): self.log(text)
        elif ((channel.delay is not None) and (channel.delay > 0)):
            text = self.chrome_instance.generic_scrape(channel.link, channel.delay)
            if (self.debug_mode): self.log(text)
        else:
            response = None
            timer = 1
            count = 0
            while (response is None):
                try:
                    response = requests.get(channel.link, headers = {'User-agent': 'RSS Generator Bot'})
                    text = response.text
                    if(self.debug_mode): self.log(text)
                except Exception as err:
                    self.log("ERROR:")
                    self.log(str(err))
                    self.log("Retrying in " + str(timer) + " seconds.")
                    time.sleep(timer)
                    timer = timer * 2
                    if (count == 6):
                        break
                    else:
                        count += 1
        channel.generate_items(text)
        channel.save_channel()
