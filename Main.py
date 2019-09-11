import requests
import itertools as it
from RSSPost import RSSPost
from RSSChannel import RSSChannel

Debug = True

def get_image_data(text, start_pattern, stop_pattern, global_pattern=""):
    start = text.find(global_pattern)
    if Debug: print("Getting Image Data")
    image_data = []
    while(start >= 0):
        start = text.find(start_pattern, start)
        stop = text.find(stop_pattern, start)
        if (start > 0):
            image_data.append(text[start:stop])
            start += 1
    return image_data


channels = []

with  open('Feed_Definitions.txt') as fp:
    for key,group in it.groupby(fp,lambda line: line.startswith('~-~-~-~-')):
        if not key:
            group = list(group)
            #print(group)
            channels.append(RSSChannel(group))

for channel in channels:
    print(channel)

'''
url = "https://gelbooru.com/index.php?page=post&s=list&tags=fire_emblem%3a_three_houses"
response = requests.get(url)
text = response.text
#print(text)
data = get_image_data(text, '<div class="thumbnail-preview">', 'class="preview "/></a></span>', "</ins></div>")

n = 0

for l in data:
    print(str(n) + ": " + l + "\n\n")
    n += 1
'''
