import requests
import itertools as it
from RSSChannel import RSSChannel
from datetime import datetime
from datetime import timedelta
import time
import sys

Debug = True

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
            <p><a href="/">Home</a> &gt; Feeds</p>
            <h1>K-Barber's RSS-Generator: Feeds</h1>
            <p>A list of your feeds:</p>
            <ul>
'''

bottom = '''
            </ul>
        </div>
    </div>
</body>
</html>
'''

def index_channels():
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


with  open('Feed_Definitions.txt') as fp:
    for key,group in it.groupby(fp,lambda line: line.startswith('~-~-~-~-')):
        if not key:
            group = list(group)
            channels.append(RSSChannel(group))

try:
    while True:
        now = datetime.now()
        print(time.asctime(), "- Updating Channels")
        for channel in channels:
            if (channel.lastBuildDate is not None):
                if (now >= channel.lastBuildDate + timedelta(minutes=int(channel.ttl))):
                    print("Updating " + channel.title)
                    channel.print()
                    channel.generate_items()
                    channel.save_channel()
            else:
                channel.print()
                channel.generate_items()
                channel.save_channel()
        index_channels()
        print(time.asctime(), "- Updating in 5 Minutes. Press 'Ctrl + C' to abort")
        time.sleep(300)
except KeyboardInterrupt:
    pass
print(time.asctime(), "- Stopping")
