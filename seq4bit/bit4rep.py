#! /usr/bin/python
# -*- coding: utf-8 -*-

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