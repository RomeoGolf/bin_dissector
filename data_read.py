#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      GordonRV
#
# Created:     14.11.2013
# Copyright:   (c) GordonRV 2013
#-------------------------------------------------------------------------------

#def main():
#    pass
#
#if __name__ == '__main__':
#    main()


#import data_config
from data_config import *

import struct
import os
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import time
import swertka
import numpy as np

data_fname = "data/02.bin"
# (66, 83, 73, 64, 100, 50, 49, 48)
config_fname = "data/config_2.txt"

class DataRead:
    def __init__(self):
        self.dconf = DataConfig(config_fname)
        # quantity of blocks
        self.block_num = os.path.getsize(data_fname) // self.dconf.packet_length
        
    def get_vars(self, df, block_num):
        _data_type = {1:'B', 2:'H', 4:'I'}
        for i in range(self.block_num):
            packet = df.read(self.dconf.packet_length)
            variables = {};
            index = 0
            for item in self.dconf.config:
                s = str(item[0])
                if item[2] == 1:    #single variable
                    v = int.from_bytes(packet[index:(index+item[1])], 'little')
                    variables.update({s: v})
                else:               # array
                    s1 = "<%d%s" % (item[2], _data_type[item[1]])
                    p = packet[index:(index+item[1]*item[2])]
                    v = np.asarray(struct.unpack(s1, p))
                    variables.update({s: v})
                index = index + item[1] * item[2]
            yield variables
            
dr = DataRead()

print('Block quantity = %d' % dr.block_num)
print('Start...')
t1 = time.perf_counter()

data_file = open(data_fname, "rb")
#data_file.seek(dconf.packet_length * 500)
lHi = []

fig = plt.figure()
plt.ion()
x = range(60)
y = [1 for i in x]
y[0] = 20000
line1, = plb.plot(x, y)
line2, = plb.plot(x, y)

#for i in get_vars(data_file, 100):
for i in dr.get_vars(data_file, dr.block_num):
    #print(i['Swertka'])
    res = swertka.get_swertka(i['CodNonius'], i['Num_Swr'], i['Num_Div'],
            i['Diapazon'], i['Srez'])

    lHi.append(i['Hi'] / 8)
    if len(line1.get_xdata()) != i['Num_Swr']:
        line1.set_xdata(range(i['Num_Swr']))
        line2.set_xdata(range(i['Num_Swr']))
        line1.get_axes().axis([0,  i['Num_Swr'], 0, 25000])

    line1.set_ydata(res)
    line2.set_ydata(i['Swertka'][0:i['Num_Swr']])
    plt.draw()
    #plt.pause(0.0001)
    fig.canvas.flush_events()

#    print(i["Hi"])
    #if (i['Npack_'] % 1000) == 0:
    if (i['Npack_'] % 100) == 0:
        print(i["Npack_"])

plt.close()

#plt.plot(res)
#plt.plot(i['Swertka'][0:i['Num_Swr']])
#plt.show()


data_file.close()

t2 = time.perf_counter() - t1
Secs = t2 % 60
Mins = (t2/60) % 60
Hrs = (t2/3600) % 60
print('Stop! Elapsed time is %d h %d min %f s' % (Hrs, Mins, Secs))
##print('Stop! Elapsed time is %f s' % (t2))

#plt.plot(lHi)
#plt.show()





