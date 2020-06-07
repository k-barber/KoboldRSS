from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tkst
import queue

class ThreadSafeConsole(Text):
    def __init__(self, master, **options):
        Text.__init__(self, master, **options)
        self.queue = queue.Queue()
        self.update_me()
    def write(self, line):
        self.queue.put(line)
    def clear(self):
        self.queue.put(None)
    def update_me(self):
        try:
            while 1:
                line = self.queue.get_nowait()
                if line is None:
                    self.delete(1.0, END)
                else:
                    self.insert(END, str(line))
                self.see(END)
                self.update_idletasks()
        except queue.Empty:
            pass
        self.after(100, self.update_me)

class RSSWindow:

    shell = None
    server_output = None
    root = None

    def update(self):
        self.root.update_idletasks()
        self.root.update()

    def print_to_server_output(self, string):
        self.server_output.write(str(string) + "\n\r")
    
    def __init__(self, ShellInstance):
        self.shell = ShellInstance
        print(self.shell.get_value())
        self.root = Tk(screenName="RSS Generator")
        self.root.title("RSS Generator")

        mainframe = ttk.Frame(self.root, width=300, height=300, padding="5 5 5 5")
        mainframe.grid(row=0, column=0, sticky="news")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)
        mainframe.columnconfigure(2, weight=1)
        mainframe.rowconfigure(1, weight=1)

        generator_output_box = ttk.Frame(mainframe, borderwidth=2, relief="sunken", width=400, height=400)
        server_output_box = ttk.Frame(mainframe, borderwidth=2, relief="sunken", width=400, height=400)
        options_box = ttk.Frame(mainframe, width=200, height=400)

        Label(mainframe, text="Options: ").grid(row=0, column=0, sticky="news", pady=5, padx=5)
        Label(mainframe, text="Generator Output: ").grid(row=0, column=1, sticky="news", pady=5, padx=5)
        Label(mainframe, text="Server Output: ").grid(row=0, column=2, sticky="news", pady=5, padx=5)

        options_box.grid(row=1, column=0, sticky="news", pady=5, padx=5)
        generator_output_box.grid(row=1, column=1, sticky="news", pady=5, padx=5)
        generator_output_box.columnconfigure(0, weight=1)
        generator_output_box.rowconfigure(0, weight=1)

        server_output_box.grid(row=1, column=2, sticky="news", pady=5, padx=5)
        server_output_box.columnconfigure(0, weight=1)
        server_output_box.rowconfigure(0, weight=1)

        # Set up generator output
        generator_output_y_scrollbar = Scrollbar(generator_output_box)
        generator_output_x_scrollbar = Scrollbar(generator_output_box, orient=HORIZONTAL)

        generator_output = ThreadSafeConsole(generator_output_box, width=60, wrap="none",
                        xscrollcommand=generator_output_x_scrollbar.set,
                        yscrollcommand=generator_output_y_scrollbar.set,
                        borderwidth=0, highlightthickness=0, bg="#000000", fg="#FFFFFF", insertbackground="#FFFFFF")

        generator_output_y_scrollbar.config(command=generator_output.yview)
        generator_output_y_scrollbar.grid(row=0, column=1, sticky=N+S+E+W)
        generator_output_x_scrollbar.grid(row=1, column=0, sticky=N+S+E+W)

        generator_output_x_scrollbar.config(command=generator_output.xview)

        generator_output.grid(row=0, column=0, sticky="news")

        # Set up server output
        server_output_y_scrollbar = Scrollbar(server_output_box)
        server_output_x_scrollbar = Scrollbar(server_output_box, orient=HORIZONTAL)

        self.server_output = ThreadSafeConsole(server_output_box, width=60, wrap="none",
                        xscrollcommand=server_output_x_scrollbar.set,
                        yscrollcommand=server_output_y_scrollbar.set,
                        borderwidth=0, highlightthickness=0, bg="#000000", fg="#FFFFFF", insertbackground="#FFFFFF")

        server_output_y_scrollbar.config(command=self.server_output.yview)
        server_output_y_scrollbar.grid(row=0, column=1, sticky=N+S+E+W)
        server_output_x_scrollbar.grid(row=1, column=0, sticky=N+S+E+W)

        server_output_x_scrollbar.config(command=self.server_output.xview)

        self.server_output.grid(row=0, column=0, sticky="news")

        debug_mode = BooleanVar()

        ttk.Checkbutton(options_box, text="Debug Mode", variable=debug_mode, onvalue=True).grid(row=0, column=0, sticky="news", pady=5, padx=5, columnspan=2)
        port = StringVar()
        Label(options_box, text="Server Options:").grid(row=1, column=0, sticky="news", pady=5, padx=5, columnspan=2)
        Label(options_box, text="Port:").grid(row=2, column=0, sticky="news")
        port_number = Entry(options_box, width=5, textvariable=port)
        port_number.insert(index=0, string="8000")
        port_number.grid(row=2, column=1, sticky="news", pady=5, padx=5)

        def print_port():
            self.shell.print_server_output(port.get())

        def start_server():
            self.shell.start_server(port.get(), debug_mode.get())

        def stop_server():
            self.shell.stop_server()

        ttk.Button(options_box, text="Start", command=start_server).grid(row=3, column=0, sticky="news", pady=5, padx=5)
        ttk.Button(options_box, text="Stop", command=stop_server).grid(row=3, column=1, sticky="news", pady=5, padx=5)
        
        port.set("8000")
        generator_output.insert(END, str(debug_mode.get()))
