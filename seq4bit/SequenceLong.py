#! /usr/bin/python
# -*- coding: utf-8 -*-

import psutil
import sharedmem
import sys
import math
from bit4rep import representation, rev_representation
from Sequence import Sequence

# assert environment is 64bit environment
assert sys.maxsize == 2**63 - 1


def to_sharedmem(sequence, length, odd=False, processes=psutil.cpu_count(logical=False)):
    arr = sharedmem.empty(math.ceil(len(sequence)/2), dtype='u1')
    with sharedmem.MapReduce(np=processes) as pool:
        chunksize = int(length/processes//2*2) or 1

        def work(i):
            if (i + chunksize) < length:
                end = i + chunksize
            else:
                end = length
            for x in range(i, end//2*2, 2):
                arr[x/2] = (representation[sequence[x]]<<4) + representation[sequence[x+1]]

        r = pool.map(work, range(0, length, chunksize))
    if odd:
        arr[length//2] = representation[sequence[length-1]]<<4
    return arr


def to_string(array, odd=False, processes=sharedmem.cpu_count()):
    arr_size = array.shape[0]
    out_arr = sharedmem.empty([arr_size*2], dtype='|S1')
    with sharedmem.MapReduce(np=processes) as pool:
        chunksize = int(arr_size / processes) or 1

        def work(i):
            if (i + chunksize) < arr_size:
                end = i + chunksize
            else:
                end = arr_size
            for x in range(i, end):
                out_arr[x*2] = rev_representation[array[x] >> 4]
                out_arr[x*2+1] = rev_representation[array[x] & 0x0F]

        r = pool.map(work, range(0, arr_size, chunksize))
    if odd:
        return str(out_arr[:-1].tostring().decode())
    return str(out_arr.tostring().decode())


class SequenceLong(Sequence):

    def __init__(self, seq='', cpus=sharedmem.cpu_count()):
        super().__init__()
        self.cpus = cpus
        self.load_string(seq)

    def __len__(self):
        return self.length

    def __str__(self):
        return to_string(self.seq, self.odd, self.cpus)

    def load_string(self, string):
        self.length = len(string)
        self.odd = self.length % 2
        self.seq = to_sharedmem(string, self.length, self.odd, self.cpus)


if __name__ == '__main__':
    import timeit
    seq = 'AGATANNNA'
    print(str(SequenceLong(seq)))
    for mnoznik in (625, 1250, 2500, 5000, 10000, 20000, 40000):
        print(mnoznik*5, timeit.timeit('str(SequenceLong(seq, 1))',
                            setup="from __main__ import SequenceLong; seq = 'AGATA'*%d" % mnoznik,
                            number=10), 1)
    for mnoznik in (625, 1250, 2500, 5000, 10000, 20000, 40000):
        print(mnoznik*5, timeit.timeit('str(SequenceLong(seq, 2))',
                            setup="from __main__ import SequenceLong; seq = 'AGATA'*%d" % mnoznik,
                            number=10), 2)