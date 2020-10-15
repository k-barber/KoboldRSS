import requests
import itertools as it
from RSSChannel import RSSChannel
from datetime import datetime, timedelta
from Utils import log
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
    chrome = None
    stop_event = None
    start_time = None
    channels = []

    def __init__(self, shell_param, debug, chrome_instance):
        self.debug_mode = debug
        self.shell = shell_param
        self.chrome = chrome_instance
        self.shell.print_generator_output("Hello World!")
        self.start_time = datetime.now()
        log("Generator start time: " + str(self.start_time))
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
        self.shell.print_generator_output("Feed_Definitions.txt defines the following:")
        with open('Feed_Definitions.txt') as fp:
            for key, group in it.groupby(fp, lambda line: line.startswith('~-~-~-~-')):
                if not key:
                    group = list(group)
                    channel = RSSChannel(group)
                    self.shell.print_generator_output(channel.title)
                    self.channels.append(channel)

    def update_channels(self):
        now = datetime.now()
        modified = datetime.fromtimestamp(os.path.getmtime('Feed_Definitions.txt'))
        if (modified >= self.start_time):
            self.shell.print_generator_output("Feed Definitions have been updated, regenerating feed list")
            self.start_time = now
            self.create_channels()
        self.index_channels()
        self.shell.print_generator_output("Updating Channels")
        for channel in self.channels:
            if (channel.lastBuildDate is not None):
                if (now >= channel.lastBuildDate + timedelta(minutes=int(channel.ttl))):
                    self.shell.print_generator_output("Updating " + channel.title)
                    if (self.debug_mode): channel.print()
                    channel.generate_items()
                    channel.save_channel()
            else:
                self.shell.print_generator_output("Updating " + channel.title)
                if (self.debug_mode): channel.print()
                channel.generate_items()
                channel.save_channel()
        self.shell.print_generator_output("Updating in 5 Minutes. Press 'Ctrl + C' to abort")