#! /usr/bin/python
# -*- coding: utf-8 -*-

#from bitarray import bitarray

import gmpy2
from bit4rep import representation, rev_representation
from Sequence import Sequence


def to_int(sequence):
    out_num = gmpy2.mpz(0)
    for lerret in sequence:
        out_num |= (representation[lerret])
        out_num <<= 4
    out_num >>=4
    return out_num


def to_string(mpz_object):
    out_list = []
    while mpz_object:
        out_list.append(rev_representation[mpz_object%16])
        mpz_object >>=4
    return ''.join(reversed(out_list))


class SequenceShort(Sequence):

    def __init__(self, seq=''):
        super().__init__()
        self.length = len(seq)
        self.load_string(seq)

    def __str__(self):
        return to_string(self.seq)

    def load_string(self, string):
        self.seq = to_int(string)


if __name__ == '__main__':
    import timeit
    seq = 'AGATA'
    print(SequenceShort(seq))
    seq *= 10000
    assert str(SequenceShort(seq)) == seq
    for mnoznik in (625, 1250, 2500, 5000, 10000, 20000, 40000):
        print(mnoznik*5, timeit.timeit('str(SequenceShort(seq))',
                            setup="from __main__ import SequenceShort; seq = 'AGATA'*%d"%mnoznik, number=10))

