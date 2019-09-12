import requests
import itertools as it
from RSSChannel import RSSChannel
import datetime
import time
import sys

Debug = True

channels = []

with  open('Feed_Definitions.txt') as fp:
    for key,group in it.groupby(fp,lambda line: line.startswith('~-~-~-~-')):
        if not key:
            group = list(group)
            channels.append(RSSChannel(group))

while True:
    for channel in channels:
        print(channel)
        channel.generate_items()
        channel.save_feed()
    print("Waiting 5 Minutes")
    time.sleep(300)
