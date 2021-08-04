from http.server import BaseHTTPRequestHandler, HTTPServer
import email.parser
import socket
import requests
from RSSChannel import RSSChannel
from Utils import clean_input, folder_is_hidden
from socketserver import ThreadingMixIn
import json
import os
import magic
import mimetypes

mime = magic.Magic(mime=True)
from datetime import datetime, timedelta
from urllib import parse

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
        self.httpd = ThreadedHTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
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
        os.path.join("Public/img/Cache/", f)
        for f in os.listdir("Public/img/Cache/")
        if os.path.isfile(os.path.join("Public/img/Cache/", f))
    ]
    for file_name in onlyfiles:
        modified = datetime.fromtimestamp(os.path.getmtime(file_name))

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
    shell.channels.append(new_channel)
    shell.recompile_definitions()
    new_channel = RSSChannel()


urls = {
    "/": "pages/Main.html",
    "/res/preview.xsl": "pages/preview.xsl",
    "/favicon.ico": "Img/favicon.ico",
    "/New-Feed": "pages/New-Feed.html",
    "/Success": "pages/Success.html",
    "/Help": "pages/Help.html",
}


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread"""


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
                path = urls[path]
            path = path.strip("/")
            full_path = os.path.join("Public/", path)
            if os.path.exists(full_path):
                guessed = mimetypes.guess_type(full_path)
                file_type = guessed[0]
                if guessed[0] == None:
                    file_type = mime.from_file(full_path)
                if file_type.startswith("text"):
                    file = open(full_path, "r", encoding="utf-8")
                    response = file.read()
                    if file_type == "text/html":
                        template = open(
                            "Public/pages/template.html", "r", encoding="utf-8"
                        )
                        template = template.read()
                        response = template.replace(
                            '<div id="container"></div>', response
                        )
                    self.send_response(200)
                    self.send_header("Content-type", file_type)
                    self.end_headers()
                    self.wfile.write(bytes(response, "utf-8"))
                else:
                    file = open(full_path, "rb")
                    response = file.read()
                    self.send_response(200)
                    self.send_header("Content-type", file_type)
                    self.end_headers()
                    self.wfile.write(bytes(response))
            elif path.startswith("Proxy/"):
                url = path[6:]
                try:
                    file_name = os.path.basename(url)
                    full_file = os.path.join("Public/img/Cache/", file_name)
                    if os.path.exists(full_file):
                        cached = open(full_file, "rb").read()
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
                        cached = open(full_file, "wb")
                        cached.write(response.content)
                        cached.close()
                        self.send_response(response.status_code)
                        self.end_headers()
                        self.wfile.write(bytes(response.content))
                except Exception as err:
                    shell.print_server_output(str(err))
            elif path.startswith("Feeds"):
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
                    f = open("Public/pages/Feeds.html", "r", encoding="utf-8")
                    insert = f.read()
                    insert = insert.replace(
                        "var items = [];", "var items = " + json.dumps(items) + ";"
                    )
                    template = open("Public/pages/template.html", "r", encoding="utf-8")
                    template = template.read()
                    response = template.replace('<div id="container"></div>', insert)
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes(response, "utf-8"))
            else:
                ind = open("Public/pages/404.html", "r", encoding="utf-8")
                st = ind.read()
                template = open("Public/pages/template.html", "r", encoding="utf-8")
                template = template.read()
                response = template.replace('<div id="container"></div>', st)
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(response, "utf-8"))
            return
        except Exception as err:
            print(err)
            shell.print_server_output(str(err))
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            ind = open("Public/pages/500.html", "r", encoding="utf-8")
            st = ind.read()
            template = open("Public/pages/template.html", "r", encoding="utf-8")
            template = template.read()
            response = template.replace('<div id="container"></div>', st)
            self.wfile.write(bytes(response, "utf-8"))
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
                if len(data) == 2 and data[0] == "ERROR":
                    self.send_response(401)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    if data[1] == "INVALID":
                        self.wfile.write(bytes("Invalid RegEx provided.", "utf-8"))
                    elif data[1] == "TIMEOUT":
                        self.wfile.write(bytes("RegEx evaluation timed out.", "utf-8"))
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
                out_file = os.path.join("Public/img/Uploads", filename)
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
                directory = data["directory"]
                directory = directory[1:]
                file_name = data["file_name"]
                destination = os.path.normpath(
                    os.path.join(directory, data["destination"])
                )
                new_file = os.path.normpath(os.path.join(destination, file_name))
                full_file = os.path.normpath(os.path.join(directory, file_name))
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
            ind = open("Public/pages/500.html", "r", encoding="utf-8")
            st = ind.read()
            self.wfile.write(bytes(st, "utf-8"))
            return
