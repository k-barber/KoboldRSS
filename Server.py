from http.server import BaseHTTPRequestHandler, HTTPServer
import email.parser
import socket
import requests
from RSSChannel import RSSChannel
from Utils import clean_input, folder_is_hidden
import json
from io import BytesIO
import os
from os import path as file_path, listdir
from os.path import isfile, join
from datetime import datetime, timedelta
from urllib import parse
import re

shell = None
browser = None


class ServerInstance:

    debug_mode = None
    running = None
    httpd = None

    def __init__(self, shell_param, port_number, debug, browser_instance):
        self.debug_mode = debug
        global shell, browser
        shell = shell_param
        browser = browser_instance
        clear_cache()
        # Change this to your IP Address if you are hosting from a different computer on the network
        HOST_NAME = "0.0.0.0"
        IP = get_ip()
        if IP is not None:
            shell.print_server_output("Detected IP address as: " + IP)
            # HOST_NAME = IP
        PORT_NUMBER = int(port_number)
        shell.print_server_output(
            "Server will accessible as localhost:"
            + str(PORT_NUMBER)
            + " on this machine or "
            + IP
            + ":"
            + str(PORT_NUMBER)
            + " for machines on this network"
        )
        self.httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
        shell.print_server_output(IP + ":" + str(PORT_NUMBER) + " Server Start")


new_channel = RSSChannel()


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


def clear_cache():
    now = datetime.now()
    onlyfiles = [
        join("Img/Cache/", f)
        for f in listdir("Img/Cache/")
        if isfile(join("Img/Cache/", f))
    ]
    for file_name in onlyfiles:
        modified = datetime.fromtimestamp(file_path.getmtime(file_name))

        if now >= modified + timedelta(days=7):
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
    print(data)
    if data["category"] != "":
        cats = data["category"].strip().split(",")
        cats = [cat.strip() for cat in cats]
        new_channel.category = cats
    if data["copyright"] != "":
        new_channel.copyright = data["copyright"]
    if data["description"] != "":
        new_channel.description = data["description"]
    if data["use_media"] == True:
        if data["enclosure_length"] != "":
            new_channel.enclosure_length = data["enclosure_length"]
        if data["enclosure_type"] != "":
            new_channel.enclosure_type = data["enclosure_type"]
        if data["enclosure_url"] != "":
            new_channel.enclosure_url = data["enclosure_url"]
    if data["use_image"] == True:
        if data["image_link"] != "":
            new_channel.image_link = data["image_link"]
        if data["image_title"] != "":
            new_channel.image_title = data["image_title"]
        if data["image_url"] != "":
            new_channel.image_url = data["image_url"]
    if data["item_author"] != "":
        new_channel.item_author = data["item_author"]
    if data["item_category"] != "":
        new_channel.item_category = data["item_category"]
    if data["item_comments"] != "":
        new_channel.item_comments = data["item_comments"]
    if data["item_description"] != "":
        new_channel.item_description = data["item_description"]
    if data["item_guid"] != "":
        new_channel.item_guid = data["item_guid"]
    if data["item_link"] != "":
        new_channel.item_link = data["item_link"]
    if data["item_pattern"] != "":
        new_channel.item_pattern = data["item_pattern"]
    if data["item_pubDate"] != "":
        new_channel.item_pubDate = data["item_pubDate"]
    if data["item_source"] != "":
        new_channel.item_source = data["item_source"]
    if data["item_title"] != "":
        new_channel.item_title = data["item_title"]
    if data["language"] != "":
        new_channel.language = data["language"]
    if data["link"] != "":
        new_channel.link = data["link"]
    if data["managingEditor"] != "":
        new_channel.managingEditor = data["managingEditor"]
    if data["title"] != "":
        new_channel.title = data["title"]
    if data["ttl"] != "":
        new_channel.ttl = data["ttl"]
    if data["webMaster"] != "":
        new_channel.webMaster = data["webMaster"]
    if data["login_required"] == True:
        if data["logged_title"] != "":
            new_channel.logged_title = data["logged_title"]
        if data["logged_URL"] != "":
            new_channel.logged_URL = data["logged_URL"]
    if data["delay"] != 0:
        new_channel.delay = data["delay"]
    if data["path"] != "":
        new_channel.path = data["path"]


def update_defs():
    """
    Write a new channel to the 'Feed_Definitions.txt' file
    """
    global new_channel, shell
    output = new_channel.print_definition()
    f = open("Feed_Definitions.txt", "a+")
    f.write(output + "~-~-~-~-\n")
    f.close()
    shell.channels.append(new_channel)
    new_channel = RSSChannel()


urls = {
    "/": ["Pages/Main.html", "text/html"],
    "/res/preview.xsl": ["Pages/preview.xsl", "text/html"],
    "/Public/": ["Pages/Public.html", "text/html"],
    "/favicon.ico": ["Img/favicon.ico", "image/x-icon"],
    "/Pages/styles.css": ["Pages/styles.css", "text/css"],
    "/Pages/dayjs.min.js": ["Pages/dayjs.min.js", "text/javascript"],
    "/Pages/css/all.css": ["Pages/css/all.css", "text/css"],
    "/New-Feed": ["Pages/New-Feed.html", "text/html"],
    "/Success": ["Pages/Success.html", "text/html"],
    "/Help": ["Pages/Help.html", "text/html"],
}


class MyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        global shell
        output = self.client_address[0] + " " + args[0] + " - " + args[1]
        shell.print_server_output(output)

    def log_error(self, format, *args):
        global shell
        output = self.client_address[0] + " " + args[0] + " - " + args[1]
        shell.print_server_output(output)

    def do_GET(self):
        global shell
        try:
            self.protocol_version = "HTTP/1.1"
            path = parse.unquote(self.path)
            if path in urls.keys():
                if urls[path][1].startswith("text"):
                    ind = open(urls[path][0], "r", encoding="utf-8")
                    st = ind.read()
                    self.send_response(200)
                    self.send_header("Content-type", urls[path][1])
                    self.end_headers()
                    self.wfile.write(bytes(st, "utf-8"))
                elif urls[path][1].startswith("image"):
                    f = open(urls[self.path][0], "rb")
                    st = f.read()
                    self.send_response(200)
                    self.send_header("Content-type", urls[path][1])
                    self.end_headers()
                    self.wfile.write(bytes(st))
            elif path.startswith("/Pages/"):
                path = path[1:]
                if path.endswith(".css"):
                    file_type = "text/css"
                elif path.endswith(".ttf"):
                    file_type = "font/ttf"
                elif path.endswith("eot"):
                    file_type = "application/vnd.ms-fontobject"
                elif path.endswith("svg"):
                    file_type = "image/svg+xml"
                elif path.endswith("woff"):
                    file_type = "font/woff"
                elif path.endswith("woff2"):
                    file_type = "font/woff2"
                elif path.endswith(".js"):
                    file_type = "text/javascript"
                ind = open(path, "rb")
                st = ind.read()
                self.send_response(200)
                self.send_header("Content-type", file_type)
                self.end_headers()
                self.wfile.write(bytes(st))
            elif path.startswith("/Proxy/"):
                url = path[7:]
                try:
                    filename = url[url.find("/") + 1 :].replace("/", "-")
                    if file_path.exists("Img/Cache/" + filename):
                        cached = open("Img/Cache/" + filename, "rb").read()
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(bytes(cached))
                    else:
                        domain = url[: url.find("/")]
                        if domain.count(".") > 1:
                            domain = domain[
                                domain.rfind(".", 0, domain.rfind(".")) + 1 :
                            ]
                        referer = "https://" + domain
                        url = "https://" + url
                        response = requests.get(
                            url,
                            headers={
                                "User-agent": "RSS Generator Bot",
                                "referer": referer,
                            },
                        )
                        cached = open("Img/Cache/" + filename, "wb")
                        cached.write(response.content)
                        cached.close()
                        self.send_response(response.status_code)
                        self.end_headers()
                        self.wfile.write(bytes(response.content))
                except Exception as err:
                    shell.print_server_output(str(err))
            elif path.startswith("/Feeds"):
                path = path[1:]
                if path.endswith(".xml"):
                    ind = open(path, "r", encoding="utf-8")
                    st = ind.read()
                    self.send_response(200)
                    self.send_header("Content-type", "application/xml")
                    self.end_headers()
                    self.wfile.write(bytes(st, "utf-8"))
                else:
                    files = os.listdir(path)
                    items = []
                    for file_item in files:
                        full_file = os.path.join(path, file_item)
                        stats = os.stat(full_file)
                        is_dir = os.path.isdir(full_file)
                        if not shell.show_hidden and folder_is_hidden(full_file):
                            continue
                        if is_dir == True or full_file.endswith(".xml"):
                            size = stats.st_size
                            modified = stats.st_mtime
                            items.append(
                                {
                                    "name": file_item,
                                    "size": size,
                                    "modified": modified,
                                    "is_dir": is_dir,
                                }
                            )
                    f = open("Pages/Feeds.html", "r", encoding="utf-8")
                    st = f.read()
                    st = st.replace(
                        "var items = [];", "var items = " + json.dumps(items) + ";"
                    )
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes(st, "utf-8"))
            elif path.startswith("/Img/"):
                filetype = path.split(".")[1]
                path = path[1:]
                f = open(path, "rb")
                st = f.read()
                if filetype == "svg":
                    filetype = "svg+xml"
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
            print(err)
            shell.print_server_output(str(err))
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            ind = open("Pages/500.html", "r", encoding="utf-8")
            st = ind.read()
            self.wfile.write(bytes(st, "utf-8"))
            return

    def do_POST(self):
        global new_channel, shell, browser
        try:
            self.protocol_version = "HTTP/1.1"
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            if self.path == "/Get_Source":
                params = json.loads(str(post_data, encoding="utf-8"))
                url = params["url"]
                login_required = params["login_required"]
                delay = int(params["delay"])
                if delay > 0 or login_required == True:
                    text = browser.generic_scrape(url, delay)
                else:
                    response = requests.get(
                        url, headers={"User-agent": "RSS Generator Bot"}
                    )
                    text = response.text
                new_channel.link = url
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(text, "utf-8"))
            elif self.path == "/Test_Pattern":
                params = json.loads(str(post_data, encoding="utf-8"))
                text = params["body"]
                new_channel.scrape_start_position = clean_input(
                    params["scrape_stop_position"]
                )
                new_channel.scrape_stop_position = clean_input(
                    params["scrape_start_position"]
                )
                new_channel.item_pattern = params["pattern"]
                data = new_channel.generate_items(text, True)
                if data == "ERROR":
                    self.send_response(401)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes("Invalid RegEx provided", "utf-8"))
                    return
                response = json.dumps(data)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(response, "utf-8"))
            elif self.path == "/Image_Upload":
                msg = email.parser.BytesParser().parsebytes(post_data)
                str_payload = str(msg.get_payload())
                content_type_start = str_payload.index("Content-Type: ") + 14
                content_type_stop = str_payload.index("\r\n", content_type_start)
                content_type = str_payload[content_type_start:content_type_stop]
                if (
                    content_type != "image/png"
                    and content_type != "image/jpeg"
                    and content_type != "image/gif"
                ):
                    self.send_response(401)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(
                        bytes(
                            "Wrong file type. Only PNG, JPG, and GIF accepted.", "utf-8"
                        )
                    )
                    return
                filename = self.headers["FEED_IMAGE_FILENAME"]
                print(filename)
                out_file = os.path.join("Img/Uploads", filename)
                output = open(out_file, "wb")
                output.write(
                    post_data[content_type_stop + 4 : str_payload.index("\r\n--------")]
                )
                output.close()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("Received", "utf-8"))
            elif self.path == "/Feed_Data":
                data = json.loads(str(post_data, encoding="utf-8"))
                channel_from_data(data)
                update_defs()
                new_channel.clear()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("Received", "utf-8"))
            elif self.path == "/Test_Description":
                data = json.loads(str(post_data, encoding="utf-8"))
                response = new_channel.test_definition(
                    data["pattern"],
                    data["body"],
                    data["title"],
                    data["link"],
                    data["description"],
                )
                response = json.dumps(response)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(response, "utf-8"))
            elif self.path == "/refresh_path":
                data = json.loads(str(post_data, encoding="utf-8"))
                directory = data["path"]
                directory = directory[1:]
                files = os.listdir(directory)
                items = []
                for file_item in files:
                    full_file = os.path.join(directory, file_item)
                    stats = os.stat(full_file)
                    is_dir = os.path.isdir(full_file)
                    if not shell.show_hidden and folder_is_hidden(full_file):
                        continue
                    if is_dir == True or full_file.endswith(".xml"):
                        size = stats.st_size
                        modified = stats.st_mtime
                        items.append(
                            {
                                "name": file_item,
                                "size": size,
                                "modified": modified,
                                "is_dir": is_dir,
                            }
                        )
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(json.dumps(items), "utf-8"))
            elif self.path == "/move_channel":
                data = json.loads(str(post_data, encoding="utf-8"))
                print(data)
                directory = data["directory"]
                directory = directory[1:]
                file_name = data["file_name"]
                destination = os.path.normpath(
                    os.path.join(directory, data["destination"])
                )
                new_file = os.path.normpath(os.path.join(destination, file_name))
                full_file = os.path.normpath(os.path.join(directory, file_name))
                print(destination)
                print(full_file)
                print(new_file)
                os.replace(full_file, new_file)
                for channel in shell.channels:
                    if (
                        os.path.normpath(channel.path) == os.path.normpath(directory)
                        and (channel.title.replace(":", "~").replace(" ", "_") + ".xml")
                        == file_name
                    ):
                        channel.path = destination
                        break
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(bytes("OK", "utf-8"))
            return
        except Exception as err:
            shell.print_server_output(str(err))
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            ind = open("Pages/500.html", "r", encoding="utf-8")
            st = ind.read()
            self.wfile.write(bytes(st, "utf-8"))
            return
