#!/usr/bin/env python
#encoding=utf8

from __future__ import division
import numpy as np

def AdditiveSmooth(two_gram, one_gram):
    '''
    Function: use additive smoothing, that's so simple. But I feel other smoothing technique should smooth whole campus
    var: two_gram --> word count of wi to all candidate wj in the next position, one_gram --> wi
    '''
    length = len(two_gram)
    transfer_vector = (two_gram+1) / (one_gram+length)

    return transfer_vector


if __name__ == "__main__":
    a = np.random.rand(10)
    b = np.random.rand(1)
    c = AdditiveSmooth(a, b)
    print c
