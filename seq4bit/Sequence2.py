#! /usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import sharedmem
import sys
import math
from Sequence import Sequence, representation, rev_representation

# assert it works in 64bit environment
assert sys.maxsize == 2**63 - 1

def to_sharedmem(sequence, odd=False):
    arr = sharedmem.empty(math.ceil(len(sequence)/2), dtype='u1')
    for x in range(0, len(sequence)//2*2, 2):# lerret in sequence:
        # print(x, representation[sequence[x]], representation[sequence[x+1]])
        # print(representation[sequence[x]]<<4, representation[sequence[x+1]], representation[sequence[x]]<<4 + representation[sequence[x+1]])
        arr[x/2] = (representation[sequence[x]]<<4) + representation[sequence[x+1]]
    if len(sequence)%2:
        arr[x/2+1] = representation[sequence[x+2]]<<4
    #print(arr)
    return arr

def to_string(array, odd=False):
    out_list = []
    for x in range(array.shape[0]):
        #print(array[x], array[x] >> 4, array[x] & 0x0F)
        out_list.append(rev_representation[array[x] >> 4])
        out_list.append(rev_representation[array[x] & 0x0F])
    if odd:
        out_list.pop()
    return ''.join(out_list)


if __name__ == '__main__':
    import timeit
    seq = 'AGATA'
    print(str(Sequence(seq, to_sharedmem, to_string)))
    for mnoznik in (5000, 10000, 20000, 40000):
        print(mnoznik)
        print(timeit.timeit('str(Sequence(seq, to_int_int, to_string_int))',
                            setup="from Sequence import Sequence, to_int_int, to_string_int; seq = 'AGATA'*%d"%mnoznik, number=1))
        print(timeit.timeit('str(Sequence(seq, to_int_gmpy2, to_string_gmpy2))',
                            setup="from Sequence import Sequence, to_int_gmpy2, to_string_gmpy2; seq = 'AGATA'*%d"%mnoznik, number=1))
        print(timeit.timeit('str(Sequence(seq, to_sharedmem, to_string))',
                            setup="from Sequence import Sequence; from __main__ import to_sharedmem, to_string; seq = 'AGATA'*%d" % mnoznik,
                            number=1))