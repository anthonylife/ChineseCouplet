#!/usr/bin/env python
#encoding=utf8

import sys
import numpy as np

def GetCandidateWord(top_k, hash_leaf, up_couplet):
    '''
    Function: for each word in the first line of couplet, get top k candidate corresponding word as the component of the second line of couplet
    Note: the words in the second line of couplet can't occur in the first line of couplet
    '''
    # Check the words repeat in the candidate
    cache_remove_item = {}
    for word in up_couplet:
        if hash_leaf.has_key(word):
            cache_remove_item[word] = hash_leaf.pop(word)

    item_list = hash_leaf.items()
    item_list.sort(key=lambda item: item[1], reverse=True)

    # Recovery the candidate dict
    if len(cache_remove_item) > 0:
        hash_leaf.update(cache_remove_item)

    #for item in item_list:
    #    print item[0], item[1]
    try:
        # Size of candidate set is smaller than top_k
        if len(item_list) < top_k:
            length = len(item_list)
            for i in range(length, top_k):
                item_list.append(item_list[length-1])

        candidate_word = np.array([word[0] for word in item_list[:top_k]])
        candidate_pro = np.array([word[1] for word in item_list[:top_k]])
    except:
        print "As corpus limits, You should set top_k to smaller."
        sys.exit(0)
    '''candidate_word = candidate_word_pro[:,0]
    temp_pro = candidate_word_pro[:,1]
    print "temp_pro", temp_pro
    raw_input()
    candidate_pro = np.random.rand(len(temp_pro))
    for i in range(len(candidate_pro)):
        candidate_pro[i] = float(temp_pro[i]
    print candidate_word
    print candidate_pro'''

    return candidate_word, candidate_pro


# For test
if __name__ == "__main__":
    top_k = 5
    hash_leaf = {}
    hash_leaf['a'] = 0.7
    hash_leaf['b'] = 0.2
    hash_leaf['c'] = 0.4
    hash_leaf['d'] = 0.6
    print GetCandidateWord(top_k, hash_leaf, [''])
