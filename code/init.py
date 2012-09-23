#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import numpy as np
from ngram import HashTreeGram

def LoadInfo(intra_transfer_doc, one_gram_doc, two_gram_doc):
    '''
    Function: load word count and transfer probability between words from disk to main memory
    Input: intra_transfer_doc --> transfer probability in the corresponding position of word in couplet
            ong_gram_doc --> single word count in sentence;  two_gram_doc --> 2-gram words sequence in one sentence
    Output: gram of hash tree
    '''
    rfd = codecs.open(intra_transfer_doc, "r", encoding="utf8")
    intra_transfer_lines = rfd.readlines()
    rfd.close()

    rfd = codecs.open(one_gram_doc, "r", encoding="utf8")
    one_gram_lines = rfd.readlines()
    rfd.close()

    rfd = codecs.open(two_gram_doc, "r", encoding="utf8")
    two_gram_lines = rfd.readlines()
    rfd.close()

    return HashTreeGram(two_gram_lines, one_gram_lines, intra_transfer_lines)
