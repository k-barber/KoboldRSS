import login_utils
from Server import ServerInstance
from Gui import RSSWindow
import threading
from datetime import datetime 

class ShellInstance:

    value = "twenty"
    gui = None
    server = None
    server_interrupt = None
    #utils = login_utils.Login_Utils(debug_mode.get())

    def get_value(self):
        return self.value

    def print_server_output(self, value):
        self.gui.print_to_server_output(value)

    def stop_server(self):
        self.server_interrupt = True
        self.server.httpd.server_close()
        

    def run_server(self):
        while True:
            self.server.httpd.handle_request()
            if self.server_interrupt:
                self.print_server_output(datetime.now().strftime('[%Y/%m/%d %H:%M:%S] - ') + "Server Stops")
                break

    def start_server(self, port_number, debug):
        if self.server is None:
            self.server = ServerInstance(self, port_number, debug)
            x = threading.Thread(target=self.run_server)
            x.start()
        else:
            self.print_server_output("Server is already running")

    def __init__(self):
        try:
            self.gui = RSSWindow(self)
            while True:
                self.gui.update()
        except Exception as err:
            self.server_interrupt = True
            self.server.httpd.server_close()
            exit()
