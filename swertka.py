
import matplotlib.pyplot as plt
import numpy as np
import math

def get_swertka(CodNonius, Num_Swr, Num_Div, Diapazon, Srez):
    _noise = 8
    _gr_non = 2 ** (5 - CodNonius)
    _bad = 0
    maxx = Num_Swr * Num_Div * 2
    if maxx > Srez.size:
        sk = np.ones(Num_Swr, dtype=np.int)
        s1 = np.ones(Num_Swr, dtype=np.int)
        c1 = np.ones(Num_Swr, dtype=np.int)
        zz = np.ones(Num_Swr, dtype=np.int)
        Signal = 1
        bad = 1
        # Exception? Returned value?
        return False

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

    Signal = np.sqrt((np.square(Szc - np.mean(Szc))) + (np.square(Szs - np.mean(Szs))))

    s1 = Szs.reshape(Num_Swr, Num_Div, order='F')
    c1 = Szc.reshape(Num_Swr, Num_Div, order='F')

    msk =  np.floor(np.sum(s1, axis=1) / Num_Div)
    s2 = s1[0:_noise,:]
    ms0 = np.floor(np.mean(s2))

    mck = np.floor(np.sum(c1, axis=1) / Num_Div)
    c2 = c1[0:_noise,:]
    mc0 = np.floor(np.mean(c2))
    n20 = (np.square(ms0) + np.square(mc0))

    s2 = np.square(s2)
    c2 = np.square(c2)
    sc2 = s2 + c2

    m20 = np.floor(np.mean(sc2))

    s2 = np.square(s1)
    c2 = np.square(c1)
    sc2 = s2 + c2
    m2k = np.floor(np.mean(sc2, axis=1))
    sk =  (m2k - 2*(msk*ms0 + mck*mc0)) + n20

    return sk
