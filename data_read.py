#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      GordonRV
#
# Created:     14.11.2013
# Copyright:   (c) GordonRV 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#def main():
#    pass
#
#if __name__ == '__main__':
#    main()


import data_config
import struct
import os
import matplotlib.pyplot as plt
import time

data_fname = "02.bin"
# (66, 83, 73, 64, 100, 50, 49, 48)

block_num = os.path.getsize(data_fname) // data_config.packet_length

def get_vars(df, block_num):
    _data_type = {1:'B', 2:'H', 4:'I'}
    for i in range(block_num):
        packet = df.read(data_config.packet_length)
        variables = {};
        index = 0
        for item in data_config.config:
            s = str(item[0])
            if item[2] == 1:
                v = int.from_bytes(packet[index:(index+item[1])], 'little')
                variables.update({s: v})
            else:
                s1 = "<%d%s" % (item[2], _data_type[item[1]])
                p = packet[index:(index+item[1]*item[2])]
                v = struct.unpack(s1, p)
                variables.update({s: v})

#                if item[1] == 1:
#                    s1 = "<%dB" % (item[2])
#                    p = packet[index:(index+item[1]*item[2])]
#                    v = struct.unpack(s1, p)
#                    variables.update({s: v})
#                elif item[1] == 4:
#                    s1 = "<%di" % (item[2])
#                    p = packet[index:(index+item[1]*item[2])]
#                    v = struct.unpack(s1, p)
#                    variables.update({s: v})
#                else:
#                    raise Exception("Unsupported data type")
#                    v = [];
#                    for i in range(item[2] - 1):
#                        buf = packet[index + i * item[1] : (index + (i + 1) * item[1])]
#                        v.append(int.from_bytes(buf, 'little'))
#                    variables.update({s: v})


            index = index + item[1] * item[2]
        yield variables

print('Start...')
t1 = time.perf_counter()

data_file = open(data_fname, "rb")
#data_file.seek(data_config.packet_length * 500)
lHi = []

#plt.ion()
for i in get_vars(data_file, block_num):
    lHi.append(i['Hi'] / 8)
#    plt.clf()
#    plt.plot(i['Swertka'][0:i['Num_Swr']])
#    plt.draw()
#plt.close()

#    print(i["Hi"])
#    if (i['Npack_'] % 1000) == 0:
#        print(i["Npack_"])
data_file.close()

t2 = time.perf_counter() - t1
print('Stop! Elapsed time is %f s' % t2)

plt.plot(lHi)
plt.show()





