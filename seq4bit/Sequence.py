#! /usr/bin/python
# -*- coding: utf-8 -*-

import abc

class Sequence(abc.ABC):

    def __init__(self):
        super().__init__()

    def __len__(self):
        return self.length

    @abc.abstractmethod
    def load_string(self, string):pass

    @abc.abstractmethod
    def __str__(self):pass


if __name__ == '__main__':
    # should raise an exception
    s = Sequence()

