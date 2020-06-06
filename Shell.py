import login_utils
from Gui import RSSWindow

class ShellInstance:

    value = "twenty"

    #utils = login_utils.Login_Utils(debug_mode.get())

    def get_value(self):
        return self.value

    def __init__(self):
        gui = RSSWindow(self)
    