import login_utils
from Gui import RSSWindow

class ShellInstance:

    value = "twenty"
    gui = None
    #utils = login_utils.Login_Utils(debug_mode.get())

    def get_value(self):
        return self.value

    def print_port(self, value):
        self.gui.print_to_server_output(value)

    def __init__(self):
        self.gui = RSSWindow(self)
        while True:
            self.gui.update()
