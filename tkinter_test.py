
from data_read import *

import tkinter as tk
from tkinter import Tk, ttk, tix, Frame, Label, filedialog
import configparser


skip = 7000
endskip = 5000

class Application(tk.Frame):

    def __init__(self, master=None):
        self.ini_file = 'setting.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.ini_file)
        self.stop = False

        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        #self.centerWindow()

    def centerWindow(self):
        w = 390
        h = 250
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def createWidgets(self):
        if self.config.has_option('FILES', 'config'):
            self.config_file = self.config.get('FILES', 'config')
        else:
            self.config_file = ''
        if self.config.has_option('FILES', 'data'):
            self.data_file = self.config.get('FILES', 'data')
        else:
            self.data_file = ''

        self.is_show_graph = tk.IntVar()
        if self.config.has_option('OPTIONS', 'graph'):
            self.is_show_graph.set(self.config.getint('OPTIONS', 'graph'))

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

        g_info = ttk.LabelFrame(self, text = "Info", padding = 5)
        g_info.pack(fill = 'x', expand = 1)

        Label(g_info, text = 'packets: ').grid(row = 0)
        self.l_packets = Label(g_info, text = '-')
        self.l_packets.grid(row = 0, column = 1)

        Label(g_info, text = 'packet: ').grid(row = 1)
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

        tk.Checkbutton(g_options, text = 'Show graph', variable = self.is_show_graph).pack()

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

        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                                            command=root.destroy)
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
                self.config_file = fname
                self.l_config['text'] = self.config_file
            else:
                self.data_file = fname
                self.l_data['text'] = self.data_file

    def open_data(self):
        self.dr = DataRead()
        #print('Block quantity = %d' % self.dr.block_num)
        self.l_packets["text"] = '%d' % self.dr.block_num

    def set_stop(self):
        self.stop = True

    def process_data(self):
        self.bt_process["state"] = 'disabled'
        print('Start...')
        t1 = time.perf_counter()
        data_file = open(data_fname, "rb")
        data_file.seek(self.dr.dconf.packet_length * skip)
        lHi = []
        fig = plt.figure()
        plt.ion()
        x = range(60)
        y = [1 for i in x]
        y[0] = 20000
        line1, = plb.plot(x, y)
        line2, = plb.plot(x, y)
        self.pb["maximum"] = self.dr.block_num - skip - endskip
        self.pb["value"] = 0
        for i in self.dr.get_vars(data_file, self.dr.block_num - skip - endskip):
            if self.stop:
                self.stop = False
                break
            res = swertka.get_swertka(i['CodNonius'], i['Num_Swr'], i['Num_Div'],
                                      i['Diapazon'], i['Srez'])
            #lHi.append(i['Hi'] / 8)
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
            #if (i['Npack_'] % 100) == 0:
            #    print(i["Npack_"])

            self.pb.step()
            if self.pb["value"] > 0:
                t2 = time.perf_counter() - t1
                Secs = t2 % 60
                Mins = (t2/60) % 60
                Hrs = (t2/3600) % 60
                self.l_time["text"] = '%.2d:%.2d:%.2d' % (Hrs, Mins, Secs)

                t_expected = (t2 / self.pb["value"]) * self.pb["maximum"]
                Secs = t_expected % 60
                Mins = (t_expected/60) % 60
                Hrs = (t_expected/3600) % 60
                self.l_exp_time["text"] = '%.2d:%.2d:%.2d' % (Hrs, Mins, Secs)

                t_remained = t_expected - t2
                Secs = t_remained % 60
                Mins = (t_remained/60) % 60
                Hrs = (t_remained/3600) % 60
                self.l_rem_time["text"] = '%.2d:%.2d:%.2d' % (Hrs, Mins, Secs)
            self.update()

        plt.close()
        data_file.close()
        self.bt_process["state"] = 'normal'

    def save_app_config(self):
        if not self.config.has_section('FILES'):
            self.config.add_section('FILES')
        self.config.set('FILES', 'config', self.config_file)
        self.config.set('FILES', 'data', self.data_file)
        if not self.config.has_section('OPTIONS'):
            self.config.add_section('OPTIONS')
        self.config.set('OPTIONS', 'graph', str(self.is_show_graph.get()))
        with open(self.ini_file, 'w') as configfile:
            self.config.write(configfile)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
app.save_app_config()


