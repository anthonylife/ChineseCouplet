#!/usr/bin/env python
#encoding=utf8

from __future__ import division
from ngram import StaGram, StaMatchWord
import sys, codecs

def CalTransferPro(one_gram_dic, two_gram_dic, match_word_dic, inner_transfer_doc, intra_transfer_doc):
    '''
    FUNCTION: calculate the following matrix transfer propability:
        1. word transfer probability inner sentence; 2. word transfer probability intra sentence
        var: one_gram_dic --> single word count;
        var: two_gram_dic --> two consecutive words count;
        var: match_word_dic --> match word intra sentence count
    '''
    # Store transfer probability
    inner_transfer_dic = {}
    intra_transfer_dic = {}

    # Calculate inner transfer probaility
    wfd = codecs.open(inner_transfer_doc, "w", encoding="utf8")
    for key in two_gram_dic.keys():
        [first_word, second_word] = key.split(" ")
        try:
            one_word_count = one_gram_dic[first_word]
            two_word_count = two_gram_dic[key]
        except:
            print first_word
            sys.exit()
        transfer_pro = two_word_count / one_word_count
        wfd.write(key + " " + str(transfer_pro) + "\n")
    wfd.close()

    # Calculate intra probability
    wfd =codecs.open(intra_transfer_doc, "w", encoding="utf8")
    for key in match_word_dic.keys():
        [up_word, down_word] = key.split(" ")
        try:
            up_word_count = one_gram_dic[up_word]
            down_word_count = one_gram_dic[down_word]
            match_word_count = match_word_dic[key]

            # Calculate separately for the first line ans the second line of couplet
            forward_transfer_pro = match_word_count / up_word_count
            forward_match_words = " ".join([up_word, down_word])
            wfd.write(forward_match_words + " " + str(forward_transfer_pro) + "\n")

            if up_word != down_word:
                backward_transfer_pro = match_word_count / down_word_count
                backward_match_words = " ".join([down_word, up_word])
                wfd.write(backward_match_words + " " + str(backward_transfer_pro) + "\n")

        except:
            print key
            print up_word
            print down_word
            raw_input()
            #sys.exit()
    wfd.close()


# Now not for test, but generate train corpus for couplet
if __name__ == "__main__":
    #source_text_doc = "../corpus/couplet_utf8.txt"
    source_text_doc = "../corpus/couplet_train_inner_gram.txt"
    target_text_doc = "../stainfo/two_gram.txt"
    two_gram_dic = StaGram([source_text_doc], target_text_doc, 2)
    target_text_doc = "../stainfo/one_gram.txt"
    one_gram_dic = StaGram([source_text_doc], target_text_doc, 1)

    target_text_doc = "../stainfo/match_word.txt"
    match_word_dic = StaMatchWord([source_text_doc], target_text_doc)

    inner_transfer_doc = "../stainfo/inner_transfer.txt"
    intra_transfer_doc = "../stainfo/intra_transfer.txt"
    CalTransferPro(one_gram_dic, two_gram_dic, match_word_dic, inner_transfer_doc, intra_transfer_doc)

    '''source_text_doc = "../corpus/couplet_train_inner_gram.txt"
    target_text_doc = "../stainfo/two_gram.txt"
    two_gram_dic = StaGram([source_text_doc], target_text_doc, 2)
    target_text_doc = "../stainfo/one_gram.txt"
    one_gram_dic = StaGram([source_text_doc], target_text_doc, 1)'''

