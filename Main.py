import requests
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

def


url = "https://gelbooru.com/index.php?page=post&s=list&tags=fire_emblem%3a_three_houses"
response = requests.get(url)
text = response.text
#print(text)
data = get_image_data(text, '<div class="thumbnail-preview">', 'class="preview "/></a></span>')
