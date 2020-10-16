from login_utils import ChromeWindow
from Generator import GeneratorInstance
from Server import ServerInstance
from Gui import RSSWindow
import threading
from datetime import datetime 
import Utils

class ShellInstance:
    
    gui = None
    server = None
    server_interrupt = None
    generator_interrupt = None
    debug_mode = False
    chrome_instance = None
    generator = None

    stop_signal = None
    generator_stopped_signal = None
    chrome_stopped_signal = None
    shutdown_thread = None
    
    #utils = login_utils.Login_Utils(debug_mode.get())

    def print_server_output(self, value):
        self.gui.print_to_server_output(Utils.log(value))

    def print_generator_output(self, value):
        self.gui.print_to_generator_output(Utils.log(value))

    def start_generator(self):
        if self.generator is None:
            self.generator = GeneratorInstance(self, self.debug_mode, self.chrome_instance)
            generator_thread = threading.Thread(target=self.run_generator)
            generator_thread.start()
        else:
            self.print_generator_output("Generator is already running")

    def run_generator(self):
        while not self.stop_signal.is_set():
            self.generator.check_for_updates()
            self.generator.index_channels()
            self.generator.update_channels(self.stop_signal, self.generator_stopped_signal)
            self.stop_signal.wait(300)

    def stop_generator(self):
        print(self.generator)
        if (self.generator is not None and self.shutdown_thread is None):
            self.generator_interrupt = True
            self.stop_signal.set()
            self.print_generator_output("Stopping Generator")
            self.print_generator_output("Closing Chrome")
            self.shutdown_thread = threading.Thread(target=self.async_generator_shutdown)
            self.shutdown_thread.start()
        elif self.generator is None:
            self.print_generator_output("No Generator Running")
        elif self.shutdown_thread is not None:
            self.print_generator_output("Generator is already stopping")
        else:
            self.print_generator_output("Can't stop generator, don't know why")

    def async_generator_shutdown(self):
        while (not self.generator_stopped_signal.isSet()):
            pass
        self.print_generator_output("Generator Stops")
        self.chrome_instance.close(self.chrome_stopped_signal)
        while (not self.chrome_stopped_signal.isSet()):
            pass
        self.print_generator_output("Chrome Stops")
        self.generator = None
        self.stop_signal.clear()
        self.generator_stopped_signal.clear()
        self.chrome_stopped_signal.clear()
        self.shutdown_thread = None
        self.print_generator_output("Generator shutdown complete.")

    def stop_server(self):
        if self.server is not None:
            self.server_interrupt = True
            self.server.httpd.server_close()
            self.server = None
        else:
            self.print_server_output("No server running")

    def toggle_debug(self):
        self.debug_mode = self.gui.debug_mode.get()
        if self.server is not None:
            self.server.debug_mode = self.debug_mode
        if self.generator is not None:
            self.generator.debug_mode = self.debug_mode
        if self.chrome_instance is not None:
            self.chrome_instance.debug_mode = self.debug_mode
        
    def run_server(self):
        while True:
            self.server.httpd.handle_request()
            if self.server_interrupt:
                self.print_server_output("Server Stops")
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
        self.stop_signal = threading.Event()
        self.generator_stopped_signal = threading.Event()
        self.chrome_stopped_signal = threading.Event()
        self.chrome_instance = ChromeWindow(self.debug_mode, self)
        try:
            self.gui = RSSWindow(self)
            while True:
                self.gui.update()
        except Exception as err:
            exit()
