import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket


HOST_NAME = '0.0.0.0' # Change this to your IP Address if you are hosting from a different computer on the network
PORT_NUMBER = 8000

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

def validate_input(num):
    try:
        port = int(num)
        if 1 <= port <= 65535:
            return True
        else:
            return False
    except ValueError:
        return False

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

urls ={
    "/":["Pages/Main.html", "text/html"],
    "/Bocchi.png":["Img/Bocchi.png", "image/png"],
    "/res/preview.xsl":["Pages/preview.xsl", "text/html"],
    "/RSS.png":["Img/RSS.png", "image/png"],
    "/Feeds/" :["Pages/Feeds.html", "text/html"],
    "/favicon.ico": ["Img/favicon.ico", "image/x-icon"],
    "/Pages/styles.css": ["Pages/styles.css", "text/css"]
}

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.protocol_version = "HTTP/1.1"
        path = self.path
        if (path in urls.keys()):
            self.send_response(200)
            self.send_header("Content-type", urls[path][1])
            self.end_headers()
            if (urls[path][1].startswith("text")):
                ind = open(urls[path][0], "r", encoding="utf-8")
                st = ind.read()
                self.send_header("Content-Length", len(st))
                self.wfile.write(bytes(st, "utf-8"))
            elif(urls[path][1].startswith("image")):
                f = open(urls[self.path][0], "rb")
                st = f.read()
                self.send_header("Content-Length", len(st))
                self.wfile.write(bytes(st))
        elif(path.startswith("/Feeds/")):
            self.send_response(200)
            self.send_header("Content-type", "application/xml")
            self.end_headers()
            path = path[1:]
            ind = open(path, "r", encoding="utf-8")
            st = ind.read()
            self.send_header("Content-Length", len(st))
            self.wfile.write(bytes(st, "utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            ind = open("Pages/404.html", "r", encoding="utf-8")
            st = ind.read()
            self.send_header("Content-Length", len(st))
            self.wfile.write(bytes(st, "utf-8"))
        return

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))