import requests
import itertools as it
from RSSChannel import RSSChannel

Debug = True




channels = []

with  open('Feed_Definitions.txt') as fp:
    for key,group in it.groupby(fp,lambda line: line.startswith('~-~-~-~-')):
        if not key:
            group = list(group)
            #print(group)
            channels.append(RSSChannel(group))

for channel in channels:
    print(channel)
    channel.generate_items()
    print(channel)
    channel.save_feed()
