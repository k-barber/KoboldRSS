import time
from http.server import BaseHTTPRequestHandler, HTTPServer


HOST_NAME = '0.0.0.0' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000

urls ={
    "/":["Pages/Main.html", "text/html"],
    "/RSS.png":["RSS.png", "image/png"],
    "/Feeds/" :["Pages/Feeds.html", "text/html"],
    "/favicon.ico": ["favicon.ico", "image/x-icon"],
    "/Pages/styles.css": ["Pages/styles.css", "text/css"]
}

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("You accessed path: %s" % self.path)
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
            print("404")
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