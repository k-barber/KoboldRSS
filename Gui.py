import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import queue
import webbrowser

running = True


class ThreadSafeConsole(Text):
    def __init__(self, master, **options):
        Text.__init__(self, master, **options)
        self.tag_config("green", foreground="green")
        self.tag_config("red", foreground="red")
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
                    line_actual = str(line)
                    if "\x1b[32m" in line_actual:
                        start_index = (
                            self.index("end-1l linestart")
                            + "+"
                            + str(line_actual.index("\x1b[32m") + 1)
                            + "c"
                        )
                        line_actual = line_actual.replace("\x1b[32m", "")
                        end_index = (
                            self.index("end-1l linestart")
                            + "+"
                            + str(line_actual.index("\x1b[0m") + 1)
                            + "c"
                        )
                        line_actual = line_actual.replace("\x1b[0m", "")
                        self.insert(END, str(line_actual))
                        self.tag_add("green", start_index, end_index)
                    elif "\x1b[31m" in line_actual:
                        start_index = (
                            self.index("end-1l linestart")
                            + "+"
                            + str(line_actual.index("\x1b[31m") + 1)
                            + "c"
                        )
                        line_actual = line_actual.replace("\x1b[31m", "")
                        end_index = (
                            self.index("end-1l linestart")
                            + "+"
                            + str(line_actual.index("\x1b[0m") + 1)
                            + "c"
                        )
                        line_actual = line_actual.replace("\x1b[0m", "")
                        self.insert(END, str(line_actual))
                        self.tag_add("red", start_index, end_index)
                    else:
                        self.insert(END, str(line_actual))
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
    generator_output = None

    def is_running(self):
        global running
        return running

    def trigger_shutdown(self):
        self.shell.shutdown()

    def close_window(self):
        self.generator_output.shutdown()
        self.server_output.shutdown()
        global running
        running = False
        self.generator_output.insert(END, "Shutting Down")
        self.generator_output.see(END)
        self.generator_output.update_idletasks()
        self.server_output.insert(END, "Shutting Down")
        self.server_output.see(END)
        self.server_output.update_idletasks()
        self.root.config(cursor="wait")
        self.root.update_idletasks()
        self.root.update()
        self.root.destroy()

    def update(self):
        self.root.update_idletasks()
        self.root.update()

    def print_to_server_output(self, string):
        self.server_output.write(str(string) + "\n\r")

    def print_to_generator_output(self, string):
        self.generator_output.write(str(string) + "\n\r")

    def __init__(self, ShellInstance):
        try:
            self.shell = ShellInstance
            self.root = Tk(screenName="KoboldRSS")
            self.root.iconbitmap("Public/img/favicon.ico")
            self.root.title("KoboldRSS")
            self.root.protocol("WM_DELETE_WINDOW", self.trigger_shutdown)
            self.root.tk_setPalette(
                background="aliceblue", activeBackground="aliceblue"
            )
            self.root.minsize(1000, 475)
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)

            def on_enter(e):
                e.widget["background"] = "whitesmoke"

            def on_leave(e):
                e.widget["background"] = "white"

            self.mainframe = tk.Frame(self.root, padx=5, pady=5, height=400, width=800)
            self.mainframe.grid(row=0, column=0, sticky="news")
            self.mainframe.columnconfigure(0, weight=0)
            self.mainframe.columnconfigure(1, weight=1)
            self.mainframe.columnconfigure(2, weight=1)
            self.mainframe.rowconfigure(0, weight=0)
            self.mainframe.rowconfigure(1, weight=1)

            options_box = tk.Frame(self.mainframe)
            options_box.grid(row=1, column=0, sticky="news", pady=5, padx=5)

            Logo = ImageTk.PhotoImage(
                Image.open("Public/img/Logo_Large_shadow.png").resize((175, 50))
            )
            label = Label(self.mainframe, image=Logo)
            label.image = Logo
            label.grid(row=0, column=0, sticky="news", padx=5, pady=5)

            self.settings = {
                "debug_mode": BooleanVar(),
                "show_hidden": BooleanVar(),
                "block_requests": BooleanVar(),
                "backup_definitions": BooleanVar(value=True),
                "backup_length": IntVar(value=7),
                "port_number": IntVar(value=8000),
            }

            """""" """""" """""" """""" """""" """""" """""" """""" """
            
            Generator OUTPUT

            """ """""" """""" """""" """""" """""" """""" """""" """"""

            generator_output_box = tk.Frame(
                self.mainframe,
                borderwidth=2,
                relief="sunken",
            )
            Label(
                self.mainframe,
                text="Generator Output: ",
                font=("Bahnschrift SemiBold", 15),
            ).grid(row=0, column=1, sticky="news", pady=5, padx=5)
            generator_output_box.grid(row=1, column=1, sticky="news", pady=5, padx=5)

            generator_output_box.columnconfigure(0, weight=1)
            generator_output_box.rowconfigure(0, weight=1)

            generator_output_y_scrollbar = Scrollbar(generator_output_box)
            generator_output_x_scrollbar = Scrollbar(
                generator_output_box, orient=HORIZONTAL
            )

            self.generator_output = ThreadSafeConsole(
                generator_output_box,
                width=60,
                wrap="word",
                xscrollcommand=generator_output_x_scrollbar.set,
                yscrollcommand=generator_output_y_scrollbar.set,
                state="disabled",
                borderwidth=0,
                highlightthickness=0,
                bg="#FFFFFF",
                fg="#000000",
                insertbackground="#FFFFFF",
            )

            generator_output_y_scrollbar.config(command=self.generator_output.yview)
            generator_output_y_scrollbar.grid(row=0, column=1, sticky=N + S + E + W)
            generator_output_x_scrollbar.grid(row=1, column=0, sticky=N + S + E + W)

            generator_output_x_scrollbar.config(command=self.generator_output.xview)

            self.generator_output.grid(row=0, column=0, sticky="news")

            """""" """""" """""" """""" """""" """""" """""" """""" """
            
            Server OUTPUT

            """ """""" """""" """""" """""" """""" """""" """""" """"""

            server_output_box = tk.Frame(
                self.mainframe,
                borderwidth=2,
                relief="sunken",
            )

            Label(
                self.mainframe,
                text="Server Output: ",
                font=("Bahnschrift SemiBold", 15),
            ).grid(row=0, column=2, sticky="news", pady=5, padx=5)
            server_output_box.grid(row=1, column=2, sticky="news", pady=5, padx=5)

            server_output_box.columnconfigure(0, weight=1)
            server_output_box.rowconfigure(0, weight=1)

            server_output_y_scrollbar = Scrollbar(server_output_box)
            server_output_x_scrollbar = Scrollbar(server_output_box, orient=HORIZONTAL)

            self.server_output = ThreadSafeConsole(
                server_output_box,
                width=60,
                wrap="word",
                xscrollcommand=server_output_x_scrollbar.set,
                yscrollcommand=server_output_y_scrollbar.set,
                state="disabled",
                borderwidth=0,
                highlightthickness=0,
                bg="#FFFFFF",
                fg="#000000",
                insertbackground="#FFFFFF",
            )

            server_output_y_scrollbar.config(command=self.server_output.yview)
            server_output_y_scrollbar.grid(row=0, column=1, sticky=N + S + E + W)
            server_output_x_scrollbar.grid(row=1, column=0, sticky=N + S + E + W)

            server_output_x_scrollbar.config(command=self.server_output.xview)

            self.server_output.grid(row=0, column=0, sticky="news")

            """""" """""" """""" """""" """""" """""" """""" """""" """
            
            Generator OPTIONS

            """ """""" """""" """""" """""" """""" """""" """""" """"""

            def start_generator():
                self.shell.start_generator()

            def stop_generator():
                self.shell.stop_generator_async()

            generator_options = tk.Frame(options_box)
            generator_options.grid(row=0, column=0, columnspan=2)

            generator_options.columnconfigure(0, weight=1)
            generator_options.columnconfigure(1, weight=1)

            tk.Checkbutton(
                generator_options,
                text="Debug Mode",
                variable=self.settings["debug_mode"],
                command=self.shell.toggle_debug,
                onvalue=True,
            ).grid(row=0, column=0, sticky="news", pady=5, padx=5, columnspan=2)

            Label(
                generator_options,
                text="Generator Options:",
                font=("Bahnschrift SemiBold", 15),
            ).grid(row=1, column=0, sticky="news", pady=5, padx=5, columnspan=2)

            temp = tk.Button(
                generator_options,
                text="Start",
                command=start_generator,
                background="white",
            )
            temp.grid(row=2, column=0, sticky="news", pady=5, padx=5)
            temp.bind("<Enter>", on_enter)
            temp.bind("<Leave>", on_leave)

            temp = tk.Button(
                generator_options,
                text="Stop",
                command=stop_generator,
                background="white",
            )
            temp.grid(row=2, column=1, sticky="news", pady=5, padx=5)
            temp.bind("<Enter>", on_enter)
            temp.bind("<Leave>", on_leave)

            tk.Checkbutton(
                generator_options,
                text="Backup Feed_Definitions.txt for",
                variable=self.settings["backup_definitions"],
                command=self.shell.toggle_backup,
                onvalue=True,
            ).grid(row=3, column=0, sticky="news", pady=5, padx=5, columnspan=2)

            Label(generator_options, text="days").grid(
                row=4, column=1, sticky="news", pady=5, padx=5
            )

            # days_frame = tk.Frame(generator_options, background="red").grid(
            #    row=4, column=1, sticky="news"
            # )
            Entry(
                generator_options,
                textvariable=self.settings["backup_length"],
                background="white",
                width=5,
            ).grid(row=4, column=0, sticky="news", pady=5, padx=5)
            # Label(days_frame, text=" days").grid(row=0, column=1, sticky="w")

            """""" """""" """""" """""" """""" """""" """""" """""" """

            SERVER OPTIONS

            """ """""" """""" """""" """""" """""" """""" """""" """"""

            def start_server():
                try:
                    port_num = int(self.settings["port_number"].get())
                    if 1 <= port_num <= 65535:
                        self.shell.start_server(port_num)
                    else:
                        messagebox.showerror(
                            "Invalid Port Number",
                            "Port numbers must be between 1 and 65535",
                        )
                except ValueError:
                    messagebox.showerror(
                        "Invalid Port Number", "Port numbers must be whole numbers"
                    )

            def open_browser_gui():
                if self.shell.server is not None:
                    print(self.shell.current_port)
                    webbrowser.open("http://localhost:" + str(self.shell.current_port))
                else:
                    messagebox.showerror(
                        "Server Not Running",
                        "You can't open the web interface because the server isn't running!",
                    )

            def stop_server():
                self.shell.stop_server()

            server_options = tk.Frame(options_box)
            server_options.grid(row=1, column=0, columnspan=2)

            Label(
                server_options,
                text="Server Options:",
                font=("Bahnschrift SemiBold", 15),
            ).grid(row=0, column=0, sticky="news", pady=5, padx=5, columnspan=2)

            temp = tk.Button(
                server_options, text="Start", command=start_server, background="white"
            )
            temp.grid(row=1, column=0, sticky="news", pady=5, padx=5)
            temp.bind("<Enter>", on_enter)
            temp.bind("<Leave>", on_leave)

            temp = tk.Button(
                server_options, text="Stop", command=stop_server, background="white"
            )
            temp.grid(row=1, column=1, sticky="news", pady=5, padx=5)
            temp.bind("<Enter>", on_enter)
            temp.bind("<Leave>", on_leave)

            temp = tk.Button(
                server_options,
                text="Open Web Interface",
                command=open_browser_gui,
                background="white",
            )
            temp.grid(row=2, column=0, sticky="news", pady=5, padx=5, columnspan=2)
            temp.bind("<Enter>", on_enter)
            temp.bind("<Leave>", on_leave)

            Label(server_options, text="Port:").grid(
                row=3, column=0, sticky="news", pady=5, padx=5
            )
            port_number = Entry(
                server_options,
                width=5,
                textvariable=self.settings["port_number"],
                background="white",
            )
            port_number.grid(row=3, column=1, sticky="news", pady=5, padx=5)

            tk.Checkbutton(
                server_options,
                text="Show hidden folders on web interface",
                variable=self.settings["show_hidden"],
                command=self.shell.toggle_hidden,
                onvalue=True,
            ).grid(row=4, column=0, sticky="news", pady=5, padx=5, columnspan=2)

            tk.Checkbutton(
                server_options,
                text="Block requests from local machines",
                variable=self.settings["block_requests"],
                command=self.shell.toggle_blocking,
                onvalue=True,
            ).grid(row=5, column=0, sticky="news", pady=5, padx=5, columnspan=2)

        except Exception as err:
            print(err)
