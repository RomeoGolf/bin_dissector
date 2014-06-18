
from data_config import *

import struct
import os
import numpy as np

# (66, 83, 73, 64, 100, 50, 49, 48)

class DataRead:
    def __init__(self, data_fname, config_fname):
        self.dconf = DataConfig(config_fname)
        # quantity of blocks
        self.block_num = os.path.getsize(data_fname) // self.dconf.packet_length

    def get_vars(self, df, block_num):
        # var_config = var_name, var_width, var_length, var_type
        for i in range(block_num):
            packet = df.read(self.dconf.packet_length)
            variables = {};
            index = 0
            for item in self.dconf.config:
                s = str(item[0])
                s1 = "<%d%s" % (item[2], item[3])
                p = packet[index:(index+item[1]*item[2])] # get raw array
                if item[2] == 1:    #single variable
                    v = struct.unpack(s1, p)[0]
                else:
                    v = np.asarray(struct.unpack(s1, p)) # convert to numpy arr
                variables.update({s: v})
                index = index + item[1] * item[2]
            yield variables
