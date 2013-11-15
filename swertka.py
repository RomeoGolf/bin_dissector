#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      GordonRV
#
# Created:     15.11.2013
# Copyright:   (c) GordonRV 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#def main():
#    pass

#if __name__ == '__main__':
#    main()

import numpy as np

def get_swertka(CodNonius, Num_Swr, Num_Div, Diapazon, Srez):
    _noise = 8
    _gr_non = 2 ** (5 - CodNonius)
    _bad = 0
    maxx = Num_Swr * Num_Div * 2
    if maxx > len(Srez):
        sk = np.ones(Num_Swr, dtype=np.int) # tuple([1 for i in range(Num_Swr)])
        s1 = np.ones(Num_Swr, dtype=np.int) # tuple([1 for i in range(Num_Swr)])
        c1 = np.ones(Num_Swr, dtype=np.int) # tuple([1 for i in range(Num_Swr)])
        zz = np.ones(Num_Swr, dtype=np.int) # tuple([1 for i in range(Num_Swr)])
        Signal = 1
        bad = 1
        # Exception? Returned value?
        return False

    _srez = np.array(Srez[0:maxx])
    _srez = _srez.reshape(maxx//4, 4)
    _srez = np.fliplr(_srez)
    _srez = _srez.reshape(1, maxx)

    Sz = _srez.reshape(Num_Swr//(_gr_non // 2), _gr_non)
    Szs = np.zeros(Num_Swr * Num_Div)
    Szc = np.zeros(Num_Swr * Num_Div)








#test_srez = [i for i in range(128)]
#res =  get_swertka(1, 16, 4, 1, test_srez)
#print(res)

