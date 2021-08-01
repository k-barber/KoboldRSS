from login_utils import BrowserWindow
from Generator import GeneratorInstance
from RSSChannel import RSSChannel
from Server import ServerInstance
from Gui import RSSWindow
import threading
from datetime import datetime, timedelta
from shutil import copyfile
import itertools as it
from Utils import *
import os


class ShellInstance:

    debug_mode = False
    running = True
    channels = []
    show_hidden = False

    gui = None

    server = None
    server_interrupt = None
    current_port = None

    generator = None
    browser_instance = None
    generator_stop_signal = None
    generator_stopped_signal = None
    browser_stopped_signal = None

    """
    PRINTING FUNCTIONS
    """

    def print_server_output(self, value):
        if self.gui.is_running():
            self.gui.print_to_server_output(log(value))
            print("Server Output: " + log(value))

    def print_generator_output(self, value):
        if self.gui.is_running():
            self.gui.print_to_generator_output(log(value))
            print("Generator Output: " + log(value))

    """
    GENERATOR FUNCTIONS
    """

    def start_generator(self):
        if self.running:
            if self.generator is None:
                self.generator = GeneratorInstance(
                    self, self.debug_mode, self.browser_instance
                )
                generator_thread = threading.Thread(target=self.generator.run)
                generator_thread.start()
            else:
                self.print_generator_output("Generator is already running")

    def stop_generator(self):
        if self.generator is not None:
            self.print_generator_output("Stopping Generator")
            self.generator_stop_signal.set()
            while not self.generator_stopped_signal.isSet():
                pass
            self.print_generator_output("Generator Stopped")
            self.print_generator_output("Stopping browser")
            self.browser_instance.close()
            while not self.browser_stopped_signal.isSet():
                pass
            self.print_generator_output("browser Stopped")
            self.generator = None
            self.generator_stop_signal.clear()
            self.generator_stopped_signal.clear()
            self.browser_stopped_signal.clear()
            self.print_generator_output("Generator shutdown complete.")
        elif self.generator is None:
            self.print_generator_output("No Generator Running")

    def stop_generator_async(self):
        shutdown_thread = threading.Thread(target=self.stop_generator)
        shutdown_thread.start()

    """
    SERVER FUNCTIONS
    """

    def stop_server(self):
        if self.server is not None:
            self.server_interrupt = True
            self.server.httpd.server_close()
            self.server = None
        else:
            self.print_server_output("No server running")

    def run_server(self):
        if self.running:
            while True:
                self.server.httpd.handle_request()
                if self.server_interrupt:
                    self.print_server_output("Server Stops")
                    self.server_interrupt = False
                    break

    def start_server(self, port_number):
        if self.running:
            if self.server is None:

                def create_server_instance(self, port_number):
                    self.server = ServerInstance(
                        self, port_number, self.debug_mode, self.browser_instance
                    )
                    server_thread = threading.Thread(target=self.run_server)
                    server_thread.start()
                    self.current_port = port_number

                creation_thread = threading.Thread(
                    target=create_server_instance, args=[self, port_number]
                )
                creation_thread.start()
            else:
                self.print_server_output("Server is already running")

    """
    OTHER FUNCTIONS
    """

    def shutdown(self):
        # Shuts down the generator, server, and gui
        self.running = False
        print("Shutting Down")

        def shutboth():
            self.stop_generator()
            self.stop_server()
            self.recompile_definitions()

        shutdown_thread = threading.Thread(target=shutboth)
        shutdown_thread.start()

        shutdown_thread.join()

        shutdown_thread = None

        self.gui.close_window()

        print("Shutdown complete")
        # exit()

    def toggle_debug(self):
        if self.running:
            self.debug_mode = self.gui.debug_mode.get()
            if self.server is not None:
                self.server.debug_mode = self.debug_mode
            if self.generator is not None:
                self.generator.debug_mode = self.debug_mode
            if self.browser_instance is not None:
                self.browser_instance.debug_mode = self.debug_mode

    def toggle_hidden(self):
        if self.running:
            self.show_hidden = self.gui.show_hidden.get()

    def back_up_definitions(self):
        now = datetime.now()
        now = now.replace(microsecond=0)
        date = now.isoformat("_")
        date = date.replace(":", "_")
        file_name = "FD_Backup_" + date + ".txt"
        file_name = os.path.join("FD_Backup", file_name)
        create_folders_to_file(file_name)
        copyfile("Feed_Definitions.txt", file_name)
        self.clear_backups()

    def clear_backups(self):
        now = datetime.now()
        onlyfiles = [
            os.path.join("FD_Backup/", f)
            for f in os.listdir("FD_Backup/")
            if os.path.isfile(os.path.join("FD_Backup/", f))
        ]
        for file_name in onlyfiles:
            modified = datetime.fromtimestamp(os.path.getmtime(file_name))

            if now >= modified + timedelta(days=7):
                os.remove(file_name)

    def recompile_definitions(self):
        self.back_up_definitions()
        if len(self.channels) > 0:
            self.channels.sort(key=lambda a: os.path.join(a.path, a.title))
            f = open("Feed_Definitions.txt", "w")
            for channel in self.channels:
                output = channel.print_definition()
                f.write(output + "~-~-~-~-\n")
            f.close()

    def create_channels(self):
        self.channels = []
        if self.debug_mode:
            self.print_generator_output("Feed_Definitions.txt defines the following:")
        if not os.path.isfile("Feed_Definitions.txt"):
            self.print_generator_output("Feed_Definitions.txt missing, creating it now")
            f = open("Feed_Definitions.txt", "x")
        with open("Feed_Definitions.txt") as fp:
            for key, group in it.groupby(fp, lambda line: line.startswith("~-~-~-~-")):
                if not key:
                    group = list(group)
                    channel = RSSChannel(group)
                    if self.debug_mode:
                        self.print_generator_output(channel.title)
                    self.channels.append(channel)

    def __init__(self):
        self.create_channels()
        self.generator_stop_signal = threading.Event()
        self.generator_stopped_signal = threading.Event()
        self.browser_stopped_signal = threading.Event()
        self.browser_instance = BrowserWindow(self.debug_mode, self)
        self.back_up_definitions()
        try:
            self.gui = RSSWindow(self)
            while True:  # self.running:
                self.gui.update()
        except Exception as err:
            exit()
