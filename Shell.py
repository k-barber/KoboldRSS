from login_utils import ChromeWindow
from Generator import GeneratorInstance
from Server import ServerInstance
from Gui import RSSWindow
import threading
from datetime import datetime 

class ShellInstance:
    
    gui = None
    server = None
    server_interrupt = None
    generator_interrupt = None
    debug_mode = False
    chrome_instance = None
    generator = None
    stop_event = None
    
    #utils = login_utils.Login_Utils(debug_mode.get())

    def print_server_output(self, value):
        self.gui.print_to_server_output(value)

    def print_generator_output(self, value):
        self.gui.print_to_generator_output(value)

    def start_generator(self):
        if self.generator is None:
            self.generator = GeneratorInstance(self, self.debug_mode, self.chrome_instance)
            generator_thread = threading.Thread(target=self.run_generator)
            generator_thread.start()
        else:
            self.print_generator_output("Generator is already running")

    def run_generator(self):
        while not self.stop_event.is_set():
            self.generator.update_channels()
            if self.generator_interrupt:
                self.print_generator_output(datetime.now().strftime('[%Y/%m/%d %H:%M:%S] - ') + "Server Stops")
                self.generator_interrupt = False
                break
            self.stop_event.wait(300)

    def stop_generator(self):
        self.generator_interrupt = True
        self.stop_event.set()

    def stop_server(self):
        self.server_interrupt = True
        self.server.httpd.server_close()
        self.server = None

    def toggle_debug(self):
        debug_mode = self.gui.debug_mode.get()
        print(debug_mode)
        if self.server is not None:
            self.server.debug_mode = self.debug_mode
        if self.chrome_instance is not None:
            self.chrome_instance.debug_mode = self.debug_mode
        
    def run_server(self):
        while True:
            self.server.httpd.handle_request()
            if self.server_interrupt:
                self.print_server_output(datetime.now().strftime('[%Y/%m/%d %H:%M:%S] - ') + "Server Stops")
                self.server_interrupt = False
                break
    
    def start_server(self, port_number):
        if self.server is None:
            self.server = ServerInstance(self, port_number, self.debug_mode, self.chrome_instance)
            server_thread = threading.Thread(target=self.run_server)
            server_thread.start()
        else:
            self.print_server_output("Server is already running")

    def __init__(self):
        self.stop_event = threading.Event()
        self.chrome_instance = ChromeWindow(self.debug_mode)
        try:
            self.gui = RSSWindow(self)
            while True:
                self.gui.update()
        except Exception as err:
            self.stop_server()
            self.stop_generator()
            exit()
