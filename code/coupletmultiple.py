#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---% Computatational Linguistics class project %---#
#     Instructions
#     ------------
# This project's thought is mainly based on HMM model.
# Key words: Posterior probability; Viterbi algorithm; language model

import sys, os
import numpy as np
from init import LoadInfo
from candidate import GetCandidateWord
from hmm import ModelInit
from viterbimultiple import ViterbiDecode
from filtercouplet import RepeatWords

## Set variables
# For data files
one_gram_doc = "../stainfo/one_gram.txt"
two_gram_doc = "../stainfo/two_gram.txt"
intra_transfer_doc = "../stainfo/intra_transfer.txt"
# For top k candidate words
top_k_word = 20
top_k_candidate = 10

## Do some init work, such as loading statistic info from hard disk
print "Loading statistic info from hard disk..."
inner_transfer_tree, intra_transfer_tree, one_gram_dic = LoadInfo(intra_transfer_doc, one_gram_doc, two_gram_doc)
print "Loading finish."

## Loop: user specify the up couplet, machine find the down couplet
run_tag = True

while(run_tag):
    up_couplet = raw_input("Please input the first line of couplet and end the line with Enter button.\n\
If you want to exit the program, just input 'q' and enter.\n")
    up_couplet = up_couplet.decode("utf8")
    if up_couplet == u"q":
        sys.exit()
    couplet_length = len(up_couplet)
    print couplet_length

    # Visible words
    visible_words = np.array([up_couplet[i] for i in range (couplet_length)])

    # Candidate words for each word in first line of couplet
    hidden_candidate_words = np.array([u" " for i in range(top_k_word*couplet_length)]).reshape(top_k_word, couplet_length)

    # Transfer probability from hidden word to visible word
    hidden_visible_transfer = np.random.rand(top_k_word, couplet_length)

    # Look for candidate words accroding to each word in the the frist line of couplet
    for i in range(couplet_length):
        key = up_couplet[i]

        if not intra_transfer_tree.has_key(key):
            print "%s, Can't generate couplet" % key
            sys.exit(0)

        hash_leaf = intra_transfer_tree[key]
        #print GetCandidateWord(top_k_word, hash_leaf, up_couplet)
        #raw_input()
        hidden_candidate_words[:,i], hidden_visible_transfer[:,i] = GetCandidateWord(top_k_word, hash_leaf, up_couplet)

    for i in range(couplet_length):
        candidate = u""
        for j in range(top_k_word):
            candidate += hidden_candidate_words[j,i]
        print candidate
    hidden_transfer, init_pro = ModelInit(inner_transfer_tree, one_gram_dic, hidden_candidate_words, top_k_word)

    # Now, use viterbi algorithm to decode and get most probable path
    optimal_path, prob = ViterbiDecode(hidden_transfer, hidden_visible_transfer, init_pro, [], visible_words, top_k_word, top_k_candidate)

    #print optimal_path
    optimal_path = RepeatWords(up_couplet, optimal_path)
    #print optimal_path
    #raw_input()
    # Output the result
    for i in range(optimal_path.shape[0]):
        result = u""
        for j in range(optimal_path.shape[1]):
            result += hidden_candidate_words[optimal_path[i, j], j]
            #print hidden_candidate_words[i, optimal_path[0,i]]
        print result
    print "Press enter button to start new."

    # clear window
    #print 'Press enter to continue'
    #os.system('clear')
