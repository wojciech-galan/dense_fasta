#! /usr/bin/python
# -*- coding: utf-8 -*-

#from bitarray import bitarray

import gmpy2

representation = {
    'A':1,
    'C':2,
    'G':4,
    'T':8,
    'R':5,
    'Y':10,
    'S':6,
    'W':9,
    'K':12,
    'M':3,
    'B':14,
    'D':13,
    'H':11,
    'V':7,
    'N':15,
    '-':0,
    '.':0
}

rev_representation = {v:k for k, v in representation.items()}


def to_int_int(sequence):
    out_num = 0
    for lerret in sequence:
        out_num |= (representation[lerret])
        out_num <<= 4
    out_num >>=4
    return out_num


def to_string_int(integer):
    out_list = []
    while integer:
        out_list.append(rev_representation[integer%16])
        integer >>=4
    return ''.join(reversed(out_list))


def to_int_gmpy2(sequence):
    out_num = gmpy2.mpz(0)
    for lerret in sequence:
        out_num |= (representation[lerret])
        out_num <<= 4
    out_num >>=4
    return out_num

def to_string_gmpy2(mpz_object):
    out_list = []
    while mpz_object:
        out_list.append(rev_representation[mpz_object%16])
        mpz_object >>=4
    return ''.join(reversed(out_list))

def to_string_gmpy2_(mpz_object):
    out_list = []
    while mpz_object:
        mpz_object, reminder = gmpy2.f_divmod(mpz_object, 16)
        out_list.append(rev_representation[reminder])
    return ''.join(reversed(out_list))



class Sequence(object):

    def __init__(self, seq='', to_int=to_int_gmpy2, to_string=to_string_gmpy2):
        super().__init__()
        self.length = len(seq)
        self.seq = to_int(seq)
        self.to_string = to_string

    @classmethod
    def fromstring(cls, string):
        return cls(string)

    def __len__(self):
        return self.length

    def __str__(self):
        return self.to_string(self.seq)

    def load_string(self, string):
        self.length = len(string)
        self.seq = to_int(string)


if __name__ == '__main__':
    import timeit
    for mnoznik in (5000, 10000, 20000, 40000):
        print(mnoznik)
        print(timeit.timeit('str(Sequence(seq, to_int_int, to_string_int))',
                            setup="from __main__ import Sequence, to_int_int, to_string_int; seq = 'AGATA'*%d"%mnoznik, number=1))
        print(timeit.timeit('str(Sequence(seq, to_int_gmpy2, to_string_gmpy2))',
                            setup="from __main__ import Sequence, to_int_gmpy2, to_string_gmpy2; seq = 'AGATA'*%d"%mnoznik, number=1))
        print(timeit.timeit('str(Sequence(seq, to_int_gmpy2, to_string_gmpy2_))',
                            setup="from __main__ import Sequence, to_int_gmpy2, to_string_gmpy2_; seq = 'AGATA'*%d" % mnoznik,
                            number=1))
    seq = 'AGATA'
    print(Sequence(seq, to_int_int, to_string_int))
    print(Sequence(seq, to_int_gmpy2, to_string_gmpy2))

