#! /usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import sharedmem
import sys
import math
from Sequence import representation, rev_representation

# assert it works in 64bit environment
assert sys.maxsize == 2**63 - 1

def to_sharedmem(sequence, odd=False):
    arr = sharedmem.empty(math.ceil(len(sequence)/2), dtype='u1')
    for x in range(0, len(sequence)//2*2, 2):# lerret in sequence:
        arr[x/2] = (representation[sequence[x]]<<4) + representation[sequence[x+1]]
    if odd:
        arr[x/2+1] = representation[sequence[x+2]]<<4
    return arr

def to_string(array, odd=False):
    out_list = []
    for x in range(array.shape[0]):
        out_list.append(rev_representation[array[x] >> 4])
        out_list.append(rev_representation[array[x] & 0x0F])
    if odd:
        out_list.pop()
    return ''.join(out_list)

class Sequence(object):

    def __init__(self, seq=''):
        super().__init__()
        self.load_string(seq)

    @classmethod
    def fromstring(cls, string):
        return cls(string)

    def __len__(self):
        return self.length

    def __str__(self):
        return to_string(self.seq, self.odd)

    def load_string(self, string):
        self.length = len(string)
        self.odd = self.length % 2
        self.seq = to_sharedmem(string, self.odd)


if __name__ == '__main__':
    import timeit
    #seq = 'AGATA'*20000
    #print(str(Sequence(seq)))
    for mnoznik in (5000, 10000, 20000, 40000, 80000, 200000):
        print(mnoznik)
        # print(timeit.timeit('str(Sequence(seq, to_int_int, to_string_int))',
        #                     setup="from Sequence import Sequence, to_int_int, to_string_int; seq = 'AGATA'*%d"%mnoznik, number=1))
        # print(timeit.timeit('str(Sequence(seq, to_int_gmpy2, to_string_gmpy2))',
        #                     setup="from Sequence import Sequence, to_int_gmpy2, to_string_gmpy2; seq = 'AGATA'*%d"%mnoznik, number=1))
        print(timeit.timeit('str(Sequence(seq))',
                            setup="from __main__ import Sequence; seq = 'AGATA'*%d" % mnoznik,
                            number=1))