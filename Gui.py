from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tkst

class RSSWindow:

    shell = None
    def __init__(self, ShellInstance):
        self.shell = ShellInstance
        print(self.shell.get_value())
        root = Tk(screenName="RSS Generator")
        root.title("RSS Generator")

        mainframe = ttk.Frame(root, width=300, height=300, padding="5 5 5 5")
        mainframe.grid(row=0, column=0, sticky="news")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)
        mainframe.rowconfigure(1, weight=1)

        generator_output_box = ttk.Frame(mainframe, borderwidth=2, relief="sunken", width=200, height=400)
        server_output_box = ttk.Frame(mainframe, borderwidth=2, relief="sunken", width=200, height=400)
        options_box = ttk.Frame(mainframe, width=200, height=400)

        Label(mainframe, text="Options: ").grid(row=0, column=0, sticky="news", pady=5, padx=5)
        Label(mainframe, text="Generator Output: ").grid(row=0, column=1, sticky="news", pady=5, padx=5)
        Label(mainframe, text="Server Output: ").grid(row=0, column=2, sticky="news", pady=5, padx=5)

        options_box.grid(row=1, column=0, sticky="news", pady=5, padx=5)
        generator_output_box.grid(row=1, column=1, sticky="news", pady=5, padx=5)
        server_output_box.grid(row=1, column=2, sticky="news", pady=5, padx=5)


        # Set up generator output
        generator_output_y_scrollbar = Scrollbar(generator_output_box)
        generator_output_x_scrollbar = Scrollbar(generator_output_box, orient=HORIZONTAL)

        generator_output = Text(generator_output_box, width=30, wrap="none",
                        xscrollcommand=generator_output_x_scrollbar.set,
                        yscrollcommand=generator_output_y_scrollbar.set,
                        borderwidth=0, highlightthickness=0, bg="#000000", fg="#FFFFFF", insertbackground="#FFFFFF")

        generator_output_y_scrollbar.config(command=generator_output.yview)
        generator_output_y_scrollbar.grid(row=0, column=1, sticky=N+S+E+W)
        generator_output_x_scrollbar.grid(row=1, column=0, sticky=N+S+E+W)

        generator_output_x_scrollbar.config(command=generator_output.xview)

        generator_output.grid(row=0, column=0)

        debug_mode = BooleanVar()

        # Set up server output
        server_output_y_scrollbar = Scrollbar(server_output_box)
        server_output_x_scrollbar = Scrollbar(server_output_box, orient=HORIZONTAL)

        server_output = Text(server_output_box, width=30, wrap="none",
                        xscrollcommand=server_output_x_scrollbar.set,
                        yscrollcommand=server_output_y_scrollbar.set,
                        borderwidth=0, highlightthickness=0, bg="#000000", fg="#FFFFFF", insertbackground="#FFFFFF")

        server_output_y_scrollbar.config(command=server_output.yview)
        server_output_y_scrollbar.grid(row=0, column=1, sticky=N+S+E+W)
        server_output_x_scrollbar.grid(row=1, column=0, sticky=N+S+E+W)

        server_output_x_scrollbar.config(command=server_output.xview)

        server_output.grid(row=0, column=0)

        debug_mode = BooleanVar()

        ttk.Checkbutton(options_box, text="Debug Mode", variable=debug_mode, onvalue=True).grid(row=0, column=0, sticky="news", pady=5, padx=5)

        generator_output.insert(END, str(debug_mode.get()))

        root.mainloop()
