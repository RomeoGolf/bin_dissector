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
        for i in range(block_num):
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
            
