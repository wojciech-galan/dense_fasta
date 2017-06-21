#! /usr/bin/python
# -*- coding: utf-8 -*-

import psutil
from Sequence import Sequence
from bit4rep import representation, rev_representation
from SequenceShort import to_int, to_string


def to_list(string, length, chunksize):
    #print(length, chunksize, [to_int(string[x:x+chunksize]) for x in range(0, length, chunksize)])
    return [to_int(string[x:x+chunksize]) for x in range(0, length, chunksize)]


def to_string_(a_list):
    return ''.join([to_string(element) for element in a_list])


class SequenceFast(Sequence):

    def __init__(self, seq='', cpus=psutil.cpu_count(logical=False), chunksize=32):
        super().__init__()
        self.length = len(seq)
        self.chunksize = chunksize
        self.load_string(seq)

    def __str__(self):
        return to_string_(self.seq)

    def load_string(self, string):
        self.seq = to_list(string, self.length, self.chunksize)


if __name__ == '__main__':
    import timeit
    seq = 'AGATANNA'
    print(SequenceFast(seq, 2))
    seq *= 10000
    assert str(SequenceFast(seq)) == seq
    for x in [32, 64, 128, 256]:
        for mnoznik in (625, 1250, 2500, 5000, 10000, 20000, 40000, 80000, 200000):
            print(x, mnoznik*5, timeit.timeit('str(SequenceFast(seq, chunksize=%d))'%x,
                                setup="from __main__ import SequenceFast; seq = 'AGATA'*%d"%mnoznik, number=100))