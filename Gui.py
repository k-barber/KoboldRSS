from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as tkst
import queue
import time

running = True

class ThreadSafeConsole(Text):
    def __init__(self, master, **options):
        Text.__init__(self, master, **options)
        self.queue = queue.Queue()
        self.after_id = None
        self.update_me()
    def write(self, line):
        self.queue.put(line)
    def clear(self):
        self.queue.put(None)
    def update_me(self):
        global running
        try:
            while running:
                if not running:
                    self.after_cancel(self.after_id)
                    break
                line = self.queue.get_nowait()
                if not running:
                    self.after_cancel(self.after_id)
                    break
                if line is None:
                    self.delete(1.0, END)
                else:
                    self.configure(state="normal")
                    self.insert(END, str(line))
                    self.configure(state="disabled")
                self.see(END)
                self.update_idletasks()
            if not running:
                self.after_cancel(self.after_id)
        except queue.Empty:
            pass
        if running:
            self.after_id = self.after(100, self.update_me)
        else:
            self.after_cancel(self.after_id)
    
    def shutdown(self):
        self.after_cancel(self.after_id)


class RSSWindow:

    shell = None
    server_output = None
    root = None
    debug_mode = None
    generator_output = None

    def is_running(self):
        global running
        return running

    def trigger_shutdown(self):
        global running
        running = False
        self.generator_output.shutdown()
        self.server_output.shutdown()
        self.generator_output.insert(END, "Shutting Down")
        self.generator_output.see(END)
        self.generator_output.update_idletasks()
        self.server_output.insert(END, "Shutting Down")
        self.server_output.see(END)
        self.server_output.update_idletasks()
        self.root.config(cursor="wait")
        self.root.update_idletasks()
        self.root.update()
        self.shell.shutdown()
    
    def close_window(self):
        global running
        running = False
        self.root.destroy()

    def update(self):
        self.root.update_idletasks()
        self.root.update()

    def print_to_server_output(self, string):
        self.server_output.write(str(string) + "\n\r")

    def print_to_generator_output(self, string):
        self.generator_output.write(str(string) + "\n\r")
    
    def __init__(self, ShellInstance):
        self.shell = ShellInstance
        self.root = Tk(screenName="RSS Generator")
        self.root.title("RSS Generator")
        self.root.protocol("WM_DELETE_WINDOW", self.trigger_shutdown)

        self.mainframe = ttk.Frame(self.root, width=300, height=300, padding="5 5 5 5")
        self.mainframe.grid(row=0, column=0, sticky="news")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.columnconfigure(2, weight=1)
        self.mainframe.rowconfigure(1, weight=1)

        generator_output_box = ttk.Frame(self.mainframe, borderwidth=2, relief="sunken", width=400, height=400)
        server_output_box = ttk.Frame(self.mainframe, borderwidth=2, relief="sunken", width=400, height=400)
        options_box = ttk.Frame(self.mainframe, width=200, height=400)

        Label(self.mainframe, text="Options: ").grid(row=0, column=0, sticky="news", pady=5, padx=5)
        Label(self.mainframe, text="Generator Output: ").grid(row=0, column=1, sticky="news", pady=5, padx=5)
        Label(self.mainframe, text="Server Output: ").grid(row=0, column=2, sticky="news", pady=5, padx=5)

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

        self.generator_output = ThreadSafeConsole(generator_output_box, width=60, wrap="none",
                        xscrollcommand=generator_output_x_scrollbar.set,
                        yscrollcommand=generator_output_y_scrollbar.set,
                        state="disabled",
                        borderwidth=0, highlightthickness=0, bg="#000000", fg="#FFFFFF", insertbackground="#FFFFFF")

        generator_output_y_scrollbar.config(command=self.generator_output.yview)
        generator_output_y_scrollbar.grid(row=0, column=1, sticky=N+S+E+W)
        generator_output_x_scrollbar.grid(row=1, column=0, sticky=N+S+E+W)

        generator_output_x_scrollbar.config(command=self.generator_output.xview)

        self.generator_output.grid(row=0, column=0, sticky="news")

        # Set up server output
        server_output_y_scrollbar = Scrollbar(server_output_box)
        server_output_x_scrollbar = Scrollbar(server_output_box, orient=HORIZONTAL)

        self.server_output = ThreadSafeConsole(server_output_box, width=60, wrap="none",
                        xscrollcommand=server_output_x_scrollbar.set,
                        yscrollcommand=server_output_y_scrollbar.set,
                        state="disabled",
                        borderwidth=0, highlightthickness=0, bg="#000000", fg="#FFFFFF", insertbackground="#FFFFFF")

        server_output_y_scrollbar.config(command=self.server_output.yview)
        server_output_y_scrollbar.grid(row=0, column=1, sticky=N+S+E+W)
        server_output_x_scrollbar.grid(row=1, column=0, sticky=N+S+E+W)

        server_output_x_scrollbar.config(command=self.server_output.xview)

        self.server_output.grid(row=0, column=0, sticky="news")

        self.debug_mode = BooleanVar()

        ttk.Checkbutton(options_box, text="Debug Mode", variable=self.debug_mode,
                        command=self.shell.toggle_debug, onvalue=True).grid(row=0, column=0, sticky="news", pady=5, padx=5, columnspan=2)
        port = StringVar()
        Label(options_box, text="Server Options:").grid(row=1, column=0, sticky="news", pady=5, padx=5, columnspan=2)
        Label(options_box, text="Port:").grid(row=2, column=0, sticky="news")
        port_number = Entry(options_box, width=5, textvariable=port)
        port_number.insert(index=0, string="8000")
        port_number.grid(row=2, column=1, sticky="news", pady=5, padx=5)

        def print_port():
            self.shell.print_server_output(port.get())

        port.set("8000")

        def start_server():
            try:
                port_num = int(port.get())
                if 1 <= port_num <= 65535:
                    self.shell.start_server(port_num)
                else:
                    messagebox.showerror("Invalid Port Number", "Port numbers must be between 1 and 65535")
            except ValueError:
                messagebox.showerror("Invalid Port Number", "Port numbers must be whole numbers")

        def stop_server():
            self.shell.stop_server()

        def start_generator():
            self.shell.start_generator()

        def stop_generator():
            self.shell.stop_generator()

        ttk.Button(options_box, text="Start", command=start_server).grid(row=3, column=0, sticky="news", pady=5, padx=5)
        ttk.Button(options_box, text="Stop", command=stop_server).grid(row=3, column=1, sticky="news", pady=5, padx=5)
        
        Label(options_box, text="Generator Options:").grid(row=4, column=0, sticky="news", pady=5, padx=5, columnspan=2)

        ttk.Button(options_box, text="Start", command=start_generator).grid(row=5, column=0, sticky="news", pady=5, padx=5)
        ttk.Button(options_box, text="Stop", command=stop_generator).grid(row=5, column=1, sticky="news", pady=5, padx=5)