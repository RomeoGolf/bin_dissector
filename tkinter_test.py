
import tkinter as tk
from tkinter import Tk, ttk, tix, Frame, Label, filedialog
import configparser

ini_file = 'setting.ini'
config = configparser.ConfigParser()
config.read(ini_file)

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.centerWindow()

    def centerWindow(self):
        w = 390
        h = 250
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def createWidgets(self):
        if config.has_option('FILES', 'config'):
            self.config_file = config.get('FILES', 'config')
        else:
            self.config_file = ''
        if config.has_option('FILES', 'data'):
            self.data_file = config.get('FILES', 'data')
        else:
            self.data_file = ''

        self.is_show_graph = tk.IntVar()
        if config.has_option('OPTIONS', 'graph'):
            self.is_show_graph.set(config.getint('OPTIONS', 'graph'))

        g_files = ttk.LabelFrame(self, text = "Files", padding = 5)
        g_files.pack(fill = 'x', expand = 1)
        Label(g_files, text = 'config: ').grid(row = 0)
        Label(g_files, text = 'data: ').grid(row = 1)
        self.l_config = Label(g_files, text = self.config_file)
        self.l_data = Label(g_files, text = self.data_file)
        self.l_config.grid(row = 0, column = 1)
        self.l_data.grid(row = 1, column = 1)

        self.bt_config = tk.Button(g_files, text = 'select...')
        self.bt_data = tk.Button(g_files, text = 'select...')
        self.bt_config.grid(row = 0, column = 2)
        self.bt_data.grid(row = 1, column = 2)
        self.bt_config['command'] = lambda : self.get_fname('config')
        self.bt_data['command'] = lambda : self.get_fname('data')

        g_options = ttk.LabelFrame(self, text = "Options", padding = 5)
        g_options.pack(fill = 'x', expand = 1)

        tk.Checkbutton(g_options, text = 'Show graph', variable = self.is_show_graph).pack()

        self.bt_open = tk.Button(self)
        self.bt_open["text"] = "Open"
        #self.bt_open["command"] =
        self.bt_open.pack(pady=5)

        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                                            command=root.destroy)
        self.QUIT.pack(side="bottom")

        self.pb = tk.ttk.Progressbar(self, maximum = 10)
        self.pb.pack()
        #self.pb["maximum"] = 5
        self.pb.config(maximum=5)

    def get_fname(self, what_file):
        if what_file == 'config':
            ftypes = [('config files', '*.txt'), ('All files', '*')]
        else:
            ftypes = [('data files', '*.bin'), ('All files', '*')]
        dlg = tk.filedialog.Open(self, filetypes = ftypes)
        fname = dlg.show()
        if fname != '':
            if what_file == 'config':
                self.config_file = fname
                self.l_config['text'] = self.config_file
            else:
                self.data_file = fname
                self.l_data['text'] = self.data_file


root = tk.Tk()
app = Application(master=root)
app.mainloop()

if not config.has_section('FILES'):
    config.add_section('FILES')
config.set('FILES', 'config', app.config_file)
config.set('FILES', 'data', app.data_file)
if not config.has_section('OPTIONS'):
    config.add_section('OPTIONS')
config.set('OPTIONS', 'graph', str(app.is_show_graph.get()))
with open(ini_file, 'w') as configfile:
    config.write(configfile)
