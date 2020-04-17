import requests
import itertools as it
from RSSChannel import RSSChannel
from datetime import datetime, timedelta
from Utils import log
import os
import time
import sys

Debug = False

log("Hello World!")

start_time = datetime.now()

log("Code start time: " + str(start_time))
channels = []

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


def index_channels():
    global channels
    f = open("Pages/Feeds.html", "wb")
    output = top
    for channel in channels:
        title = channel.title.replace(":", "~").replace(" ", "_")
        output += '''                <li>
                    <a href="/Feeds/''' + title + '.xml">' + title + '''.xml</a>
                </li>
'''
    output += bottom
    f.write(str.encode(output))
    f.close()


def create_channels():
    global channels
    channels = []
    log("Feed_Definitions.txt defines the following:")
    with open('Feed_Definitions.txt') as fp:
        for key, group in it.groupby(fp, lambda line: line.startswith('~-~-~-~-')):
            if not key:
                group = list(group)
                channel = RSSChannel(group)
                log(channel.title)
                channels.append(channel)

create_channels()
try:
    while True:
        now = datetime.now()
        modified = datetime.fromtimestamp(os.path.getmtime('Feed_Definitions.txt'))
        if (modified >= start_time):
            log("Feed Definitions have been updated, regenerating feed list")
            start_time = now
            create_channels()

        log("Updating Channels")
        for channel in channels:
            if (channel.lastBuildDate is not None):
                if (now >= channel.lastBuildDate + timedelta(minutes=int(channel.ttl))):
                    log("Updating " + channel.title)
                    if (Debug): channel.print()
                    channel.generate_items()
                    channel.save_channel()
            else:
                log("Updating " + channel.title)
                if (Debug): channel.print()
                channel.generate_items()
                channel.save_channel()
        index_channels()
        log("Updating in 5 Minutes. Press 'Ctrl + C' to abort")
        time.sleep(300)
except KeyboardInterrupt:
    pass
log("Stopping")
