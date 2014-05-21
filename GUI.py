
from data_read import *

import tkinter as tk
from tkinter import Tk, ttk, tix, Frame, Label, filedialog
import configparser

class Application(tk.Frame):
    def __init__(self, master=None):
        self.ini_file = 'setting.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.ini_file)
        self.stop = False

        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.setWindowPosition()
        self.master.bind("<Configure>", self.save_geometry)

    def setWindowPosition(self):
        if self.config.has_option('POS', 'geom'):
            g = self.config.get('POS', 'geom').split('+')
            self.master.geometry('+%s+%s' % (g[1], g[2]))

    def createWidgets(self):
        if self.config.has_option('FILES', 'config'):
            self.config_file_name = self.config.get('FILES', 'config')
        else:
            self.config_file_name = ''
        if self.config.has_option('FILES', 'data'):
            self.data_file_name = self.config.get('FILES', 'data')
        else:
            self.data_file_name = ''
        if self.config.has_option('FILES', 'result'):
            self.result_file_name = self.config.get('FILES', 'result')
        else:
            self.result_file_name = ''

        # binded variables preparing
        self.is_show_graph = tk.IntVar()
        self.is_use_skip = tk.IntVar()
        self.str_skip_b = tk.StringVar()
        self.str_skip_e = tk.StringVar()
        self.str_skip_b.set("0")
        self.str_skip_e.set("0")
        if self.config.has_option('OPTIONS', 'graph'):
            self.is_show_graph.set(self.config.getint('OPTIONS', 'graph'))
        if self.config.has_option('OPTIONS', 'use_skip'):
            self.is_use_skip.set(self.config.getint('OPTIONS', 'use_skip'))
        if self.config.has_option('OPTIONS', 'skip_begin'):
            self.str_skip_b.set(self.config.getint('OPTIONS', 'skip_begin'))
        if self.config.has_option('OPTIONS', 'skip_end'):
            self.str_skip_e.set(self.config.getint('OPTIONS', 'skip_end'))

        # Files group
        g_files = ttk.LabelFrame(self, text = "Files", padding = 5)
        g_files.pack(fill = 'x', expand = 1)
        Label(g_files, text = 'config: ').grid(row = 0)
        Label(g_files, text = 'data: ').grid(row = 1)
        self.l_config = Label(g_files, text = self.config_file_name)
        self.l_data = Label(g_files, text = self.data_file_name)
        self.l_config.grid(row = 0, column = 1)
        self.l_data.grid(row = 1, column = 1)

        self.bt_config = tk.Button(g_files, text = 'select...')
        self.bt_data = tk.Button(g_files, text = 'select...')
        self.bt_config.grid(row = 0, column = 2)
        self.bt_data.grid(row = 1, column = 2)
        self.bt_config['command'] = lambda : self.get_fname('config')
        self.bt_data['command'] = lambda : self.get_fname('data')

        Label(g_files, text = 'result: ').grid(row = 2)
        self.l_result = Label(g_files, text = self.result_file_name)
        self.l_result.grid(row = 2, column = 1)
        self.bt_result = tk.Button(g_files, text = 'select...')
        self.bt_result.grid(row = 2, column = 2)
        self.bt_result['command'] = self.get_result_fname

        # Options group
        g_options = ttk.LabelFrame(self, text = "Options", padding = 5)
        g_options.pack(fill = 'x', expand = 1)
        tk.Checkbutton(g_options, text = 'Show graph',
                                    variable = self.is_show_graph).pack()
        g_skip = ttk.Frame(g_options)
        g_skip.pack(fill = 'x', expand = 1, ipadx = 5)
        tk.Checkbutton(g_skip, text = 'Use skip',
                            variable = self.is_use_skip).pack(side = 'left')
        Label(g_skip, text = "from begin=").pack(side = 'left')
        e_skip_b = ttk.Entry(g_skip, textvariable = self.str_skip_b)
        e_skip_b.pack(side = 'left')
        Label(g_skip, text = ", to end=").pack(side = 'left')
        e_skip_e = ttk.Entry(g_skip, textvariable = self.str_skip_e)
        e_skip_e.pack(side = 'left')

        # Info group
        g_info = ttk.LabelFrame(self, text = "Info", padding = 5)
        g_info.pack(fill = 'x', expand = 1)

        Label(g_info, text = 'packets: ').grid(row = 0)
        self.l_packets = Label(g_info, text = '-')
        self.l_packets.grid(row = 0, column = 1)

        Label(g_info, text = 'packet #: ').grid(row = 1)
        self.l_packet = Label(g_info, text = '0')
        self.l_packet.grid(row = 1, column = 1)

        Label(g_info, text = 'Elapsed time: ').grid(row = 2)
        self.l_time = Label(g_info, text = '-')
        self.l_time.grid(row = 2, column = 1)

        Label(g_info, text = 'Remained time: ').grid(row = 3)
        self.l_rem_time = Label(g_info, text = '-')
        self.l_rem_time.grid(row = 3, column = 1)

        Label(g_info, text = 'Expected time: ').grid(row = 4)
        self.l_exp_time = Label(g_info, text = '-')
        self.l_exp_time.grid(row = 4, column = 1)

        # Buttons
        self.bt_open = tk.Button(self)
        self.bt_open["text"] = "Open"
        self.bt_open["command"] = self.open_data
        self.bt_open.pack(pady=5)

        self.bt_process = tk.Button(self)
        self.bt_process["text"] = "Process"
        self.bt_process["command"] = self.process_data
        self.bt_process.pack(pady = 5)

        self.bt_stop = tk.Button(self)
        self.bt_stop["text"] = "Stop"
        self.bt_stop["command"] = self.set_stop
        self.bt_stop.pack(pady = 5)

        self.QUIT = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.QUIT.pack(side="bottom", pady = 5)

        self.pb = tk.ttk.Progressbar(self, maximum = 10, )
        self.pb.pack(fill = 'x', expand = 1, pady = 5)
        self.pb["maximum"] = 5      #self.pb.config(maximum=5)

    def get_fname(self, what_file):
        if what_file == 'config':
            ftypes = [('config files', '*.txt'), ('All files', '*')]
        else:
            ftypes = [('data files', '*.bin'), ('All files', '*')]
        dlg = tk.filedialog.Open(self, filetypes = ftypes)
        fname = dlg.show()
        if fname != '':
            if what_file == 'config':
                self.config_file_name = fname
                self.l_config['text'] = self.config_file_name
            else:
                self.data_file_name = fname
                self.l_data['text'] = self.data_file_name

    def get_result_fname(self):
        ftypes = [('text files', '*.txt'), ('All files', '*')]
        dlg = tk.filedialog.SaveAs(self, filetypes = ftypes)
        fname = dlg.show()
        self.result_file_name = fname
        self.l_result['text'] = self.result_file_name

    def open_data(self):
        self.dr = DataRead(self.data_file_name, self.config_file_name)
        self.l_packets["text"] = '%d' % self.dr.block_num

    def set_stop(self):
        self.stop = True

    def process_data(self):
        self.bt_process["state"] = 'disabled'

        # get skip values
        if self.is_use_skip.get() == 1:
            skip_b = int(self.str_skip_b.get())
            skip_e = int(self.str_skip_e.get())

        t1 = time.perf_counter()    # for timer
        data_file = open(self.data_file_name, "rb")
        if self.is_use_skip.get() == 1:
            data_file.seek(self.dr.dconf.packet_length * skip_b)

        # Chart preparing
        fig = plt.figure()
        plt.ion()
        x = range(60)
        y = [1 for i in x]
        y[0] = 20000
        line1, = plb.plot(x, y)
        line2, = plb.plot(x, y)

        # skip count
        skip = 0
        if self.is_use_skip.get() == 1:
            skip = skip_b + skip_e
        self.pb["maximum"] = self.dr.block_num - skip
        self.pb["value"] = 0

        # data processing loop
        for i in self.dr.get_vars(data_file, self.dr.block_num - skip):
            if self.stop:
                self.stop = False
                break
            # ============== Data processing and indication here ===============
            res = swertka.get_swertka(i['CodNonius'], i['Num_Swr'],
                                      i['Num_Div'], i['Diapazon'], i['Srez'])
            if self.is_show_graph.get() == 1:
                if len(line1.get_xdata()) != i['Num_Swr']:
                    line1.set_xdata(range(i['Num_Swr']))
                    line2.set_xdata(range(i['Num_Swr']))
                    line1.get_axes().axis([0,  i['Num_Swr'], 0, 25000])

                line1.set_ydata(res)
                line2.set_ydata(i['Swertka'][0:i['Num_Swr']])
                plt.draw()
                fig.canvas.flush_events()
            self.l_packet["text"] = str(i["Npack_"])
            # ==================================================================
            # progress bar and timer
            self.pb.step()
            if self.pb["value"] > 0:
                t2 = time.perf_counter() - t1
                self.l_time["text"] = self.time_to_text(t2)
                t_expected = (t2 / self.pb["value"]) * self.pb["maximum"]
                self.l_exp_time["text"] = self.time_to_text(t_expected)
                t_remained = t_expected - t2
                self.l_rem_time["text"] = self.time_to_text(t_remained)
            self.update()

        plt.close()
        data_file.close()
        self.bt_process["state"] = 'normal'

    def time_to_text(self, t):
        Secs = t % 60
        Mins = (t/60) % 60
        Hrs = (t/3600) % 60
        return '%.2d:%.2d:%.2d' % (Hrs, Mins, Secs)

    def save_app_config(self):
        if not self.config.has_section('FILES'):
            self.config.add_section('FILES')
        self.config.set('FILES', 'config', self.config_file_name)
        self.config.set('FILES', 'data', self.data_file_name)
        self.config.set('FILES', 'result', self.result_file_name)
        if not self.config.has_section('OPTIONS'):
            self.config.add_section('OPTIONS')
        self.config.set('OPTIONS', 'graph', str(self.is_show_graph.get()))
        self.config.set('OPTIONS', 'use_skip', str(self.is_use_skip.get()))
        self.config.set('OPTIONS', 'skip_begin', self.str_skip_b.get())
        self.config.set('OPTIONS', 'skip_end', self.str_skip_e.get())

        with open(self.ini_file, 'w') as configfile:
            self.config.write(configfile)

    def save_geometry(self, event):
        if not self.config.has_section('POS'):
            self.config.add_section('POS')
        self.config.set('POS', 'geom', self.master.geometry(None))

root = tk.Tk()
app = Application(master=root)
app.mainloop()
app.save_app_config()
