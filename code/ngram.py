#!/usr/bin/env python
#encoding=utf-8

import sys, codecs, os

def StaGram(doc_list, output_file, len_gram):
    '''
    Given a document list, output statistic number of n gram
    '''
    # length of gram
    n_gram = len_gram

    # dictionary for recording data
    gram_dic = {}

    # format of doc in "doc_list" should be the same, that is one sentence one line...
    # odd line is the first line of a couplet on a scroll, even line is the second line of a couplet on a scroll
    for doc in doc_list:
        rfd = codecs.open(doc, "r", encoding="utf8")
        list_lines = rfd.readlines()

        # Total number of sentences should be even
        length = len(list_lines)
        if length % 2 != 0:
            print length
            print 'Match error in couplets'
            sys.exit()

        for i in range(length):
            sentence = list_lines[i]
            word_num = len(sentence) - 2    # Erase some illegal character in the end of the sentence
            # for ngram
            for j in range(word_num-n_gram+1):
                key = " ".join(sentence[j:j+n_gram])
                if gram_dic.has_key(key):
                    gram_dic[key] += 1
                else:
                    gram_dic[key] = 1
        rfd.close()

    wfd = codecs.open(output_file, "w", encoding="utf8")
    for key in gram_dic.keys():
        #try:
            wfd.write(key + " " + str(gram_dic[key]) + "\n")
        #except:
        #    print key
        #    print gram_dic[key]
    wfd.close()

    return gram_dic


def StaMatchWord(doc_list, output_file):
    '''
    Statistic the match information of the first and the second line of a couplet
    '''
    # dictionary for recording data
    match_word_dic = {}

    # format of doc in "doc_list" should be the same, that is one sentence one line...
    # odd line is the first line of a couplet on a scroll, even line is the second line of a couplet on a scroll
    for doc in doc_list:
        rfd = codecs.open(doc, "r", encoding="utf8")
        list_lines = rfd.readlines()

        # Total number of sentences should be even
        length = len(list_lines)
        if length % 2 != 0:
            print 'Match error in couplets'
            sys.exit()

        for i in range(0, length, 2):
            first_sentence = list_lines[i]
            second_sentence = list_lines[i+1]
            word_num = len(first_sentence) - 2
            com_num = len(second_sentence) - 2
            if word_num != com_num:
                print first_sentence
                print second_sentence
                raw_input()
            # for ngram
            for j in range(word_num):
                try:
                    f_tag = False
                    s_tag = False
                    key_f = " ".join((first_sentence[j], second_sentence[j]))
                    key_s = " ".join((second_sentence[j], first_sentence[j]))
                    '''if first_sentence[j] == u"菊" and second_sentence[j] == u"棠":
                        print key
                        print len(key)
                        raw_input()'''

                    if match_word_dic.has_key(key_f):
                        f_tag = True
                    elif match_word_dic.has_key(key_s):
                        s_tag = True
                    '''if match_word_dic.has_key(key):
                        match_word_dic[key] += 1'''
                    if f_tag:
                        match_word_dic[key_f] += 1
                    elif s_tag:
                        match_word_dic[key_s] += 1
                    else:
                        match_word_dic[key_f] = 1
                except:
                    print first_sentence
                    print second_sentence
                    raw_input()

        rfd.close()

    wfd = codecs.open(output_file, "w", encoding="utf8")
    for key in match_word_dic.keys():
        wfd.write(key + " " + str(match_word_dic[key]) + "\n")
    wfd.close()

    return match_word_dic


def HashTreeGram(two_gram_lines, one_gram_lines, intra_transfer_lines):
    '''
    Function: Make use of relation between co-occurence words to generate a hash tree, conveniently for scan
    Note: inner sentence's words use probability, intra sentence's words use count(should be smoothed)
    Return: inner_transfer_hash, intra_transfer_hash
    '''
    ##--> Process inner sentence words
    inner_transfer_hash_tree = {}
    #rfd = codecs.open(inner_transfer_doc, "r", encoding="utf8")
    #list_lines = rfd.readlines()
    #length = len(list_lines)
    length = len(two_gram_lines)
    for i in range(length):
        [first_word, second_word, count] = two_gram_lines[i].split(" ")
        count = int(count)
        #print two_gram_lines[i]
        #raw_input()
        MakeUpTree(inner_transfer_hash_tree, first_word, second_word, count)

    #rfd.close()

    ##--> Process intra sentence words
    intra_transfer_hash_tree = {}

    length = len(intra_transfer_lines)
    for i in range(length):
        [first_word, second_word, pro] = intra_transfer_lines[i].split(" ")
        pro = float(pro)
        MakeUpTree(intra_transfer_hash_tree, first_word, second_word, pro)
    ##--> Process single word
    one_gram_dic = {}

    length = len(one_gram_lines)
    for i in range(length):
        [word, count] = one_gram_lines[i].split(" ")
        count = int(count)
        MakeUpDic(one_gram_dic, word, count)

    return inner_transfer_hash_tree, intra_transfer_hash_tree, one_gram_dic


def MakeUpDic(hash_dic, word, value):
    '''
    Function: make up hash dic
    '''
    if hash_dic.has_key(word):
        print "Wrong key in dic"
        sys.exit()
    else:
        hash_dic[word] = value

def MakeUpTree(hash_tree, first_word, second_word, value):
    '''
    Function: make up hash tree
    '''
    if hash_tree.has_key(first_word):
        hash_leaf = hash_tree[first_word]
        if hash_leaf.has_key(second_word):
            print "Wrong key in tree"
            print first_word
            print second_word
            print hash_leaf[second_word]
            print value
            if first_word != second_word:
                #pass
                raw_input()
                #sys.exit()
        hash_leaf[second_word] = value

    else:
        hash_leaf = {}
        hash_leaf[second_word] = value
        hash_tree[first_word] = hash_leaf


# For test
if __name__ == "__main__":
    #--> Test "StaGram" function
    source_text_doc = "../corpus/couplet_utf8.txt"
    '''target_text_doc = "../stainfo/two_gram.txt"
    StaGram([source_text_doc], target_text_doc, 2)
    target_text_doc = "../stainfo/one_gram.txt"
    StaGram([source_text_doc], target_text_doc, 1)'''
    target_text_doc = "../stainfo/match_word.txt"
    StaMatchWord([source_text_doc], target_text_doc)

    '''#--> Test "HashTreeGram" function
    a = ["中 央 40", "华 人 100", "华 族 1000"]
    b = ["信 10", "心 100"]
    c = ["中 国 0.488", "中 间 0.222", "发 达 0.189"]
    print HashTreeGram(a, b, c)'''
