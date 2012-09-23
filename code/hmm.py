#!/usr/bin/evn python
#encoding=utf8

from __future__ import division
import sys
import numpy as np
from smooth import AdditiveSmooth

def ModelInit(inner_transfer_tree, one_gram_dic, hidden_candidate_words, top_k_word):
    '''
    Function: for hmm model, there are five key element. Here focus on hidden to hidden transfer probability and the initial state(word) probability
    Output: hidden_transfer --> hidden state to hidden state transfer probability; init_pro --> initial state probability
    '''
    # Get state initial probability
    init_pro = CalInitialPro(one_gram_dic, hidden_candidate_words[:,0])

    # Make up hidden to hidden to hidden transfer probability
    hidden_transfer = GenHiddenHiddenArr(inner_transfer_tree, one_gram_dic, hidden_candidate_words, top_k_word)

    return hidden_transfer, init_pro


def CalInitialPro(one_gram_dic, initial_words):
    '''
    Function: Calculate the initial probability of each state(word)
    '''
    word_num = len(initial_words)
    init_pro = np.random.rand(word_num)
    total_count = 0

    for i in range(word_num):
        total_count += one_gram_dic[initial_words[i]]

    for i in range(word_num):
        init_pro[i] = one_gram_dic[initial_words[i]] / total_count

    return init_pro


def GenHiddenHiddenArr(inner_transfer_tree, one_gram_dic, hidden_candidate_words, top_k_word):
    '''
    Function: Generate hidden word to hidden word transfer probability matrix
    '''
    # Whole number of states in the hmm process
    state_num = hidden_candidate_words.shape[1]

    # Hidden state to hidden state transfer array
    hidden_transfer = np.random.rand(state_num-1, top_k_word, top_k_word)

    for i in range(state_num-1):
        for j in range(top_k_word):
            start_word = hidden_candidate_words[j,i]
            #print start_word
            #print j, i
            end_words = hidden_candidate_words[:,i+1]
            one_gram = one_gram_dic[start_word]
            try:
                hash_leaf = inner_transfer_tree[start_word]
            except:
                print 'key not exist in inner transfer tree'
                sys.exit()

            two_gram = np.array([0 for m in range(top_k_word)])
            #print hash_leaf
            for k in range(len(end_words)):
                try:
                    two_gram[k] = hash_leaf[end_words[k]]
                except:
                    #print start_word, end_words[k]
                    two_gram[k] = 0
                    #raw_input()
            #print hidden_transfer[1, 1, :]
            #print AdditiveSmooth(two_gram, one_gram)
            hidden_transfer[i,j,:] = AdditiveSmooth(two_gram, one_gram)

    return hidden_transfer
