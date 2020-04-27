import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import requests
from RSSChannel import RSSChannel
import json
import gc
from io import BytesIO
import login_utils
import os
from os import path as file_path, listdir
from os.path import isfile, join
from datetime import datetime, timedelta

new_channel = RSSChannel()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def clear_cache():
    now = datetime.now()
    onlyfiles = [join("Img/Cache/", f) for f in listdir("Img/Cache/") if isfile(join("Img/Cache/", f))]
    for file_name in onlyfiles:
        modified = datetime.fromtimestamp(file_path.getmtime(file_name))

        if (now >= modified + timedelta(days=7)):
            os.remove(file_name)

def validate_input(num):
    try:
        port = int(num)
        if 1 <= port <= 65535:
            return True
        else:
            return False
    except ValueError:
        return False

def channel_from_data(data):
    global new_channel
    if(data['category'] != ""):
        cats = data['category'].strip().split(",")
        cats = [cat.strip() for cat in cats]
        new_channel.category = cats
    if(data['copyright'] != ""):
        new_channel.copyright = data['copyright']
    if(data['description'] != ""):
        new_channel.description = data['description']
    if(data['use_media'] == "True"):
        if(data['enclosure_length'] != ""):
            new_channel.enclosure_length = data['enclosure_length']
        if(data['enclosure_type'] != ""):
            new_channel.enclosure_type = data['enclosure_type']
        if(data['enclosure_url'] != ""):
            new_channel.enclosure_url = data['enclosure_url']
    if(data['use_image'] == "True"):
        if(data['image_link'] != ""):
            new_channel.image_link = data['image_link']
        if(data['image_title'] != ""):
            new_channel.image_title = data['image_title']
        if(data['image_url'] != ""):
            new_channel.image_url = data['image_url']
    if(data['item_author'] != ""):
        new_channel.item_author = data['item_author']
    if(data['item_category'] != ""):
        new_channel.item_category = data['item_category']
    if(data['item_comments'] != ""):
        new_channel.item_comments = data['item_comments']
    if(data['item_description'] != ""):
        new_channel.item_description = data['item_description']
    if(data['item_guid'] != ""):
        new_channel.item_guid = data['item_guid']
    if(data['item_link'] != ""):
        new_channel.item_link = data['item_link']
    if(data['item_pattern'] != ""):
        new_channel.item_pattern = data['item_pattern']
    if(data['item_pubDate'] != ""):
        new_channel.item_pubDate = data['item_pubDate']
    if(data['item_source'] != ""):
        new_channel.item_source = data['item_source']
    if(data['item_title'] != ""):
        new_channel.item_title = data['item_title']
    if(data['language'] != ""):
        new_channel.language = data['language']
    if(data['link'] != ""):
        new_channel.link = data['link']
    if(data['managingEditor'] != ""):
        new_channel.managingEditor = data['managingEditor']
    if(data['title'] != ""):
        new_channel.title = data['title']
    if(data['ttl'] != ""):
        new_channel.ttl = data['ttl']
    if(data['webMaster'] != ""):
        new_channel.webMaster = data['webMaster']
    if(data['login_required'] == True):
        if(data['website'] != ""):
            new_channel.website = data['website']
        if(data['username'] != ""):
            new_channel.username = data['username']
        if(data['password'] != ""):
            new_channel.password = data['password']
    if(data['delay'] != 0):
        new_channel.delay = data['delay']

def update_defs():
    output = new_channel.print_definition()
    f = open("Feed_Definitions.txt", "a+")
    f.write("~-~-~-~-\n"+output)
    f.close()

def return_source():
    print("Test")
    '''
    response = requests.get(url)
    text = response.text
    return text
    '''

urls ={
    "/":["Pages/Main.html", "text/html"],
    "/res/preview.xsl":["Pages/preview.xsl", "text/html"],
    "/Feeds/" :["Pages/Feeds.html", "text/html"],
    "/Public/" :["Pages/Public.html", "text/html"],
    "/favicon.ico": ["Img/favicon.ico", "image/x-icon"],
    "/Pages/styles.css": ["Pages/styles.css", "text/css"],
    "/New-Feed": ["Pages/New-Feed.html", "text/html"],
    "/Success": ["Pages/Success.html", "text/html"],
    "/Help": ["Pages/Help.html", "text/html"],
}

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.protocol_version = "HTTP/1.1"
            path = self.path
            if (path in urls.keys()):
                if (urls[path][1].startswith("text")):
                    ind = open(urls[path][0], "r", encoding="utf-8")
                    st = ind.read()
                    self.send_response(200)
                    self.send_header("Content-type", urls[path][1])
                    self.end_headers()
                    self.wfile.write(bytes(st, "utf-8"))
                elif(urls[path][1].startswith("image")):
                    f = open(urls[self.path][0], "rb")
                    st = f.read()
                    self.send_response(200)
                    self.send_header("Content-type", urls[path][1])
                    self.end_headers()
                    self.wfile.write(bytes(st))
            elif(path.startswith("/Proxy/")):
                url = path[7:]
                try:
                    filename = url[url.find("/")+1:].replace("/","-")
                    if file_path.exists("Img/Cache/" + filename):
                        cached = open("Img/Cache/" + filename, "rb").read()
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(bytes(cached))
                    else:
                        domain = url[:url.find("/")]
                        if (domain.count(".") > 1):
                            domain = domain[domain.rfind(".", 0, domain.rfind("."))+1:]
                        referer = "https://" + domain
                        url = "https://" + url
                        response = requests.get(url, headers = {'User-agent': 'RSS Generator Bot', 'referer': referer})
                        cached = open("Img/Cache/" + filename, "wb")
                        cached.write(response.content)
                        cached.close()
                        self.send_response(response.status_code)
                        self.end_headers()
                        self.wfile.write(bytes(response.content))
                except Exception as err:
                    print(str(err))
            elif(path.startswith("/Feeds/")):
                path = path[1:]
                ind = open(path, "r", encoding="utf-8")
                st = ind.read()
                self.send_response(200)
                self.send_header("Content-type", "application/xml")
                self.end_headers()
                self.wfile.write(bytes(st, "utf-8"))
            elif(path.startswith("/Img/")):
                filetype = path.split(".")[1]
                path = path[1:]
                f = open(path, "rb")
                st = f.read()
                self.send_response(200)
                self.send_header("Content-type", "image/" + filetype)
                self.end_headers()
                self.wfile.write(bytes(st))
            else:
                ind = open("Pages/404.html", "r", encoding="utf-8")
                st = ind.read()
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(st, "utf-8"))
            return
        except Exception as err:
            print(str(err))
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            ind = open("Pages/500.html", "r", encoding="utf-8")
            st = ind.read()
            self.wfile.write(bytes(st, "utf-8"))
            return

    def do_POST(self):
        global new_channel
        try:
            self.protocol_version = "HTTP/1.1"
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            if(self.path == "/Get_Source"):
                params = json.loads(str(post_data, encoding="utf-8"))
                url = params["url"]
                login_required = params["login_required"]
                delay = int(params["delay"])
                if (login_required == True):
                    text = login_utils.multi_scrape(
                        params["username"],
                        params["password"],
                        params["website"],
                        url,
                        delay=delay)
                elif (delay > 0):
                    text = login_utils.generic_scrape(url, delay)
                else:
                    response = requests.get(url, headers = {'User-agent': 'RSS Generator Bot'})
                    text = response.text
                new_channel.link = url
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(text, "utf-8"))
            if(self.path == "/Test_Pattern"):
                params = json.loads(str(post_data, encoding="utf-8"))
                pattern = params["pattern"]
                text = params["body"]
                data = new_channel.test_pattern(pattern, text)
                response = json.dumps(data)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(response, "utf-8"))
            if(self.path == "/Feed_Data"):
                data = json.loads(str(post_data, encoding="utf-8"))
                channel_from_data(data)
                update_defs()
                new_channel.clear()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("Received", "utf-8"))
            if(self.path == "/Test_Description"):
                data = json.loads(str(post_data, encoding="utf-8"))
                response = new_channel.test_definition(
                    data["pattern"],
                    data["body"],
                    data["title"],
                    data["link"],
                    data["description"])
                response = json.dumps(response)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(response, "utf-8"))
            return
        except Exception as err:
            print(str(err))
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            ind = open("Pages/500.html", "r", encoding="utf-8")
            st = ind.read()
            self.wfile.write(bytes(st, "utf-8"))
            return

def main():
    clear_cache()
    HOST_NAME = '0.0.0.0' # Change this to your IP Address if you are hosting from a different computer on the network
    PORT_NUMBER = 8000
    IP = get_ip()
    if (IP is not None):
        print("Detected IP address as: " + IP + "\n")
        #HOST_NAME = IP
    ans = ""
    while ((ans != "y") and (ans != "n")):
        ans = input("Default port number is 8000. Use 8000? (y/n)")
    if (ans == "n"):
        port = 0
        while (not validate_input(port)):
            print("Ports can be between 1 and 65535 inclusive.")
            port = input("Enter a new port number:")
        PORT_NUMBER = int(port)
    print("Server will accessible as localhost:" + str(PORT_NUMBER) + " on this machine or " + IP + ":" + str(PORT_NUMBER) + " for machines on this network")
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

if __name__ == '__main__':
    main()    