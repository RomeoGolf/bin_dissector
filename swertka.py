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

import matplotlib.pyplot as plt
import numpy as np
import math

def get_swertka(CodNonius, Num_Swr, Num_Div, Diapazon, Srez):
    _noise = 8
    _gr_non = 2 ** (5 - CodNonius)
    _bad = 0
    maxx = Num_Swr * Num_Div * 2
#    if maxx > len(Srez):
    if maxx > Srez.size:
        sk = np.ones(Num_Swr, dtype=np.int)
        s1 = np.ones(Num_Swr, dtype=np.int)
        c1 = np.ones(Num_Swr, dtype=np.int)
        zz = np.ones(Num_Swr, dtype=np.int)
        Signal = 1
        bad = 1
        # Exception? Returned value?
        return False

#    _srez = Srez[0:maxx]
#    _srez = _srez.reshape(4, maxx//4, order='F')
#    _srez = np.flipud(_srez)
#    _srez = _srez.reshape(1, maxx, order='F')

    _srez = Srez[0:maxx]
    _srez = np.flipud(_srez.reshape(4, maxx//4, order='F'))
    _srez = _srez.reshape(1, maxx, order='F')

    Sz = _srez.reshape(Num_Swr//(_gr_non // 2), _gr_non, maxx // (Num_Swr * 2), order='F')

    Szs = np.zeros(Num_Swr * Num_Div)
    Szc = np.zeros(Num_Swr * Num_Div)

    for k in range(Num_Div):
        Sz1 = Sz[:,:,k]
        Sz_buf = np.zeros(Num_Swr)
        i = 0
        j = 0
        while i < Num_Swr:
            for n in range(_gr_non//2):
                Sz_buf[i+n] = Sz1[j, (_gr_non-2*n)-1]
            i = i + _gr_non//2
            j = j + 1;
        Szc[k * Num_Swr : k*Num_Swr + Num_Swr] = Sz_buf

    for k in range(Num_Div):
        Sz1 = Sz[:,:,k]
        Sz_buf = np.zeros(Num_Swr)
        i = 0
        j = 0
        while i < Num_Swr:
            for n in range(_gr_non//2):
                Sz_buf[i+n] = Sz1[j, (_gr_non-2*n)-2]
            i = i + _gr_non//2
            j = j + 1;
        Szs[k * Num_Swr : k*Num_Swr + Num_Swr] = Sz_buf

    #Signal = [math.sqrt( (c - np.mean(Szc))**2 +
    #            (s - np.mean(Szs))**2) for c, s in zip(Szc, Szs)]
    Signal = np.sqrt((np.square(Szc - np.mean(Szc))) + (np.square(Szs - np.mean(Szs))))

    s1 = Szs.reshape(Num_Swr, Num_Div, order='F')
    c1 = Szc.reshape(Num_Swr, Num_Div, order='F')

    #msk = [n / Num_Div for n in [sum(item) for item in s1]]
    #msk = np.asarray([n / Num_Div for n in np.sum(s1, axis=1)])
    msk =  np.floor(np.sum(s1, axis=1) / Num_Div)
    s2 = s1[0:_noise,:]
    #ms0 = np.mean([np.mean(item) for item in s2])
    ms0 = np.floor(np.mean(s2))

    #mck = [n / Num_Div for n in [sum(item) for item in c1]]
    #mck = np.asarray([n / Num_Div for n in np.sum(c1, axis=1)])
    mck = np.floor(np.sum(c1, axis=1) / Num_Div)
    c2 = c1[0:_noise,:]
    #mc0 = np.mean([np.mean(item) for item in c2])
    mc0 = np.floor(np.mean(c2))
    n20 = (np.square(ms0) + np.square(mc0))

    #s2 = [n**2 for n in s2]
    #c2 = [n**2 for n in c2]
    s2 = np.square(s2)
    c2 = np.square(c2)
    #sc2 = [m + n for m, n in zip(s2, c2)]
    sc2 = s2 + c2

    #m20 = [np.mean(n) for n in [np.mean(m) for m in sc2]]
    #m20 = [np.mean(n) for n in np.mean(sc2, axis=1)]
    #m20 = np.mean(np.mean(sc2, axis=1), axis=0)
    m20 = np.floor(np.mean(sc2))

    #s2 = [n**2 for n in s1]
    #c2 = [n**2 for n in c1]
    s2 = np.square(s1)
    c2 = np.square(c1)
    #sc2 = [m + n for m, n in zip(s2, c2)]
    sc2 = s2 + c2

    #m2k = [np.mean(m) for m in sc2]
    m2k = np.floor(np.mean(sc2, axis=1))

    #sk =[m2_ - 2*(s*ms0 + c*mc0) + n20 for s, c, m2_ in zip(msk, mck, m2k)]
    sk =  (m2k - 2*(msk*ms0 + mck*mc0)) + n20

    return sk



