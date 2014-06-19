
from data_read import *

import tkinter as tk
from tkinter import Tk, ttk, tix, Frame, Label, filedialog
import configparser
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.pylab as plb

import time

import multiprocessing as mp

import scipy
from scipy import ndimage
import swertka

class Graphica():
    def __init__(self, is_array, is_var):
        # Chart preparing
        plt.ion()
        x = range(5)
        y = range(5)
        # chart lines for arrays and variables
        self.line_a = []
        self.line_v = []

        # max & min for axes
        self.a_minx = 0
        self.a_miny = 0
        self.a_maxx = 1
        self.a_maxy = 1
        self.v_minx = 0
        self.v_miny = 0
        self.v_maxx = 1
        self.v_maxy = 1

    def Draw(self):
        data = q.get()
        arr_data = data[2]
        arr_var = data[3]
        x = range(2)
        y = range(2)

        # need show arrays
        if data[0] == 1:
            # create figure if need
            if plt.get_fignums().count(1) == 0:
                self.fig = plt.figure(num = 1)
                self.line_a.clear()
                
            # create lines if need
            if len(self.line_a) < len(arr_data):
                for i in range(len(arr_data) - len(self.line_a)):
                    line, = plt.plot(x, y, figure = plt.figure(num = 1))
                    self.line_a.append(line)

            # overgrow protection
            if self.a_maxx > 1000000:
                self.a_maxx = 1;
            if self.a_maxy > 1000000:
                self.a_maxy = 1;
            if self.a_miny < -1000000:
                self.a_miny = 0;

            # match line length and draw lines
            for line in self.line_a:
                if len(line.get_xdata()) != len(arr_data[self.line_a.index(line)]):
                    line.set_xdata(range(len(arr_data[self.line_a.index(line)])))
                line.set_ydata(arr_data[self.line_a.index(line)])

                if self.a_minx > min(line.get_xdata()):
                    self.a_minx = min(line.get_xdata())
                if self.a_maxx < max(line.get_xdata()):
                    self.a_maxx = max(line.get_xdata())

                if self.a_miny > min(line.get_ydata()):
                    self.a_miny = min(line.get_ydata())
                if self.a_maxy < max(line.get_ydata()):
                    self.a_maxy = max(line.get_ydata())
            # set axes
            self.line_a[0].get_axes().axis([self.a_minx, self.a_maxx,
                                                self.a_miny, self.a_maxy])
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

        # need show variables
        if data[1] == 1:
            if plt.get_fignums().count(2) == 0:
                self.fig_var = plt.figure(num = 2)
                self.line_v.clear()

            if len(self.line_v) < len(arr_var):
                for i in range(len(arr_var) - len(self.line_v)):
                    line, = plt.plot(x, y, figure = plt.figure(num = 2))
                    self.line_v.append(line)

            for line in self.line_v:
                if len(line.get_xdata()) != len(arr_var[self.line_v.index(line)]):
                    line.set_xdata(range(len(arr_var[self.line_v.index(line)])))
                line.set_ydata(arr_var[self.line_v.index(line)])

                if self.v_minx > min(line.get_xdata()):
                    self.v_minx = min(line.get_xdata())
                if self.v_maxx < max(line.get_xdata()):
                    self.v_maxx = max(line.get_xdata())

                if self.v_miny > min(line.get_ydata()):
                    self.v_miny = min(line.get_ydata())
                if self.v_maxy < max(line.get_ydata()):
                    self.v_maxy = max(line.get_ydata())

            self.line_v[0].get_axes().axis([self.v_minx, self.v_maxx,
                                                self.v_miny, self.v_maxy])

            self.fig_var.canvas.draw()
            self.fig_var.canvas.flush_events()

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
        self.master.bind("<Destroy>", self.onDestroy)

        self.gr = Graphica(self.is_show_graph.get(), self.is_show_var_graph.get())

        self.time_queue = deque([])
        self.time_queue_max = 100

    def onDestroy(self, event):
        self.save_geometry()
        plt.close('all')

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

        self.ini_var = []
        if self.config.has_section('SELVAR'):
            ini_var_opt = self.config.options('SELVAR')
            self.ini_var = [self.config.get('SELVAR', opt) for opt in self.config.options('SELVAR')]

        # binded variables preparing
        self.is_show_graph = tk.IntVar()
        self.is_show_var_graph = tk.IntVar()
        self.is_not_thinned = tk.IntVar()
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
        if self.config.has_option('OPTIONS', 'var_graph'):
            self.is_show_var_graph.set(self.config.getint('OPTIONS', 'var_graph'))
        if self.config.has_option('OPTIONS', 'not_thinned'):
            self.is_not_thinned.set(self.config.getint('OPTIONS', 'not_thinned'))

        # for variable selecting
        self.varSelVar = tk.StringVar(self)
        self.varSelVar.set("---")

        self.sel_var_list = {}
        self.sel_varframe_list = {}

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

        g_graph_opt = ttk.Frame(g_options)
        g_graph_opt.pack(fill = 'x', expand = 1, ipadx = 5)

        tk.Checkbutton(g_graph_opt, text = 'Show array graph',
                                    variable = self.is_show_graph).pack(side = 'left')
        tk.Checkbutton(g_graph_opt, text = 'Show variable graph',
                                    variable = self.is_show_var_graph).pack(side = 'left')
        tk.Checkbutton(g_graph_opt, text = 'Not thinning data (slowly)',
                                    variable = self.is_not_thinned).pack(side = 'left')

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
        g_info = ttk.LabelFrame(self, text = "Info")
        g_info.pack(fill = 'x', expand = 1)

        g_time_info = ttk.Frame(g_info)
        g_time_info.pack(anchor = 'ne', fill = 'x', side = 'left', padx = 10)

        g_sel_var = ttk.Frame(g_info)
        g_sel_var.pack(anchor = 'ne', fill = 'x', side = 'left', padx = 10)

        self.g_vars = ttk.Frame(g_info)
        self.g_vars.pack(anchor = 'ne', fill = 'x', side = 'left', padx = 10)

        Label(g_time_info, text = 'packets: ').grid(row = 0)
        self.l_packets = Label(g_time_info, text = '-')
        self.l_packets.grid(row = 0, column = 1)

        Label(g_time_info, text = 'packet #: ').grid(row = 1)
        self.l_packet = Label(g_time_info, text = '0')
        self.l_packet.grid(row = 1, column = 1)

        Label(g_time_info, text = 'Elapsed time: ').grid(row = 2)
        self.l_time = Label(g_time_info, text = '-')
        self.l_time.grid(row = 2, column = 1)

        Label(g_time_info, text = 'Remained time: ').grid(row = 3)
        self.l_rem_time = Label(g_time_info, text = '-')
        self.l_rem_time.grid(row = 3, column = 1)

        Label(g_time_info, text = 'Expected time: ').grid(row = 4)
        self.l_exp_time = Label(g_time_info, text = '-')
        self.l_exp_time.grid(row = 4, column = 1)

        self.cbSelVar = tk.ttk.Combobox(g_sel_var, textvariable = self.varSelVar)
        self.cbSelVar.grid(row = 0, column = 3)
        self.btAddVarInfo = tk.Button(g_sel_var, text = '+', command = self.add_var_info)
        self.btAddVarInfo.grid(row = 0, column = 4)
        for var_name in self.ini_var:
            self.create_var_info_frame(var_name)

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

        options = tuple([opt[0] for opt in self.dr.dconf.config if opt[2] == 1])
        self.varSelVar.set(options[0])
        self.cbSelVar['values'] = options

    def set_stop(self):
        self.stop = True

    def add_var_info(self):
        var_name = self.varSelVar.get()
        if list(self.sel_var_list.keys()).count(var_name) == 0:
            self.create_var_info_frame(var_name)

    def create_var_info_frame(self, name):
         _g_ = ttk.Frame(self.g_vars)
         _g_.pack(anchor = 'ne')
         _l_ = tk.Label(_g_, text = '{} = '.format(name))
         _l_.grid(row = 0, column = 0)
         _l_data = tk.Label(_g_, text = '-')
         _l_data.grid(row = 0, column = 1)
         _b_ = tk.Button(_g_, text = 'x')
         _b_.grid(row = 0, column = 2)
         _b_['command'] = lambda : self.del_sel_var(name)
         self.sel_var_list.update({name:_l_data})
         self.sel_varframe_list.update({name:_g_})

    def del_sel_var(self, name):
        _g_ = self.sel_varframe_list[name]
        _g_.destroy()
        del self.sel_var_list[name]
        del self.sel_varframe_list[name]

    def process_data(self):
        self.bt_process["state"] = 'disabled'

        # get skip values
        if self.is_use_skip.get() == 1:
            skip_b = int(self.str_skip_b.get())
            skip_e = int(self.str_skip_e.get())
        # for timer
        t1 = time.perf_counter()
        # skip count
        skip = 0
        if self.is_use_skip.get() == 1:
            skip = skip_b + skip_e
        pack_cnt = skip
        self.pb["maximum"] = self.dr.block_num - skip
        self.pb["value"] = 0

        # open data file
        data_file = open(self.data_file_name, "rb")

        start_h = 11
        start_m = 27
        start_s = 22
        start_t = start_h * 60 * 60 + start_m * 60 + start_s
        # get time of first block
        i = self.dr.get_vars(data_file, 1).__next__()
        self.start_time = i['Sys_t_']
        data_file.seek(0)
        if self.is_use_skip.get() == 1:
            data_file.seek(self.dr.dconf.packet_length * skip_b)
        # open result file
        result_file = open(self.result_file_name, "w", 1)

        # assembling data names to out
        out_vars = ("Time", "Hi", "Sys_t")
        # write the header to the result file
        res_header = '\t'.join(out_vars)
        result_file.writelines('{}{}'.format(res_header, '\n'))

        # data preparing for var chart
        hi_ = []
        sys_dt_ = []
        old_sys_t = 0

        # subprocess initialization
        q.put([0, 0,  0, 0])
        pp = mp.Process(target = self.gr.Draw())

        now_t = time.perf_counter()
        # data processing loop
        for i in self.dr.get_vars(data_file, self.dr.block_num - skip):
            if self.stop:
                self.stop = False
                break
            # ============== Data processing and indication here ===============
            result = swertka.get_swertka(i['CodNonius'], i['Num_Swr'],
                                 i['Num_Div'], i['Diapazon'], i['Srez'])

            # prepare data for file
            curr_t = (i['Sys_t_'] - self.start_time) * 244.15e-6  + start_t
            out_data = {}
            out_data.update({"Time": '%f' % curr_t})
            out_data.update({"Hi": '%f' % (i['Hi'] / 8 - 32)})
            out_data.update({"Sys_t": '%d' % i['Sys_t_']})

            # write data to file
            out_data_str = [out_data[ind] for ind in out_vars]
            result_file.writelines('{}{}'.format('\t'.join(out_data_str), '\n'))

            # data for charts
            hi_.append(i['Hi'] / 8 - 32)

            if (self.is_show_graph.get() == 1) or (self.is_show_var_graph.get() == 1):
                arr_data = []
                arr_data.append(result)
                arr_data.append(i['Swertka'][0:i['Num_Swr']])
                arr_var = [hi_]

                if self.is_not_thinned.get():
                    q.put([self.is_show_graph.get(),
                                self.is_show_var_graph.get(), arr_data, arr_var])
                    self.gr.Draw()
                else:
                    if not pp.is_alive():
                        q.put([self.is_show_graph.get(),
                                self.is_show_var_graph.get(), arr_data, arr_var])
                        pp = mp.Process(target = self.gr.Draw())
                        pp.start()

            # show variables on GUI
            for var in self.sel_var_list.keys():
                if list(i.keys()).count(var) > 0:
                    self.sel_var_list[var]["text"] = str(i[var])
                if list(out_data.keys()).count(var) > 0:
                    self.sel_var_list[var]["text"] = str(out_data[var])
            # ==================================================================
            self.l_packet["text"] = str(pack_cnt)
            pack_cnt = pack_cnt + 1

            # progress bar and timer
            self.pb.step()
            if self.pb["value"] > 0:
                old_t = now_t
                now_t = time.perf_counter()
                now_dt = now_t - old_t
                self.time_queue.append(now_dt)

                if len(self.time_queue) > self.time_queue_max:
                    self.time_queue.popleft()

                #t_aver = (now_t - self.time_queue[0]) / len(self.time_queue)
                if len(self.time_queue) > 0:
                    t_aver = sum(self.time_queue) / len(self.time_queue)
                else:
                    t_aver = 0

                t2 = now_t - t1
                self.l_time["text"] = self.time_to_text(t2)
                #t_expected = (t2 / self.pb["value"]) * self.pb["maximum"]
                t_expected = (t_aver) * self.pb["maximum"]
                self.l_exp_time["text"] = self.time_to_text(t_expected)
                #t_remained = t_expected - t2
                #self.l_rem_time["text"] = self.time_to_text(t_remained)
                t_remained = t_aver * (self.pb["maximum"] - self.pb["value"])
                self.l_rem_time["text"] = self.time_to_text(t_remained)

            self.update()

        data_file.close()
        result_file.close()
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
        self.config.set('OPTIONS', 'var_graph', str(self.is_show_var_graph.get()))
        self.config.set('OPTIONS', 'not_thinned', str(self.is_not_thinned.get()))

        if self.config.has_section('SELVAR'):
            if len(self.config.options('SELVAR')) > 0:
                self.config.remove_section('SELVAR')
        if not self.config.has_section('SELVAR'):
            self.config.add_section('SELVAR')
        for var in self.sel_var_list.keys():
            self.config.set('SELVAR', var, var)

        with open(self.ini_file, 'w') as configfile:
            self.config.write(configfile)

    def save_geometry(self):
        if not self.config.has_section('POS'):
            self.config.add_section('POS')
        self.config.set('POS', 'geom', self.master.geometry(None))

if __name__ == '__main__':
    root = tk.Tk()
    q = mp.Queue()
    app = Application(master=root)
    app.mainloop()
    app.save_app_config()
