#!/usr/bin/env python
#encoding=utf8

#---% Description: Make up a good corpus is important for a couplet system %---#

import codecs

def ProcessPoetry(input_file, output_gram_file, output_file):
    '''
    Function: this function is special for specific file format of inputfile. Process based on the following characteristics of different poetrys.
            Quatrains: Temporaily can't decide wheter
            Poem:
            Pailv:
            Other:
    '''
    rfd = codecs.open(input_file, "r", encoding="utf8")
    doc_line = rfd.readlines()
    rfd.close()

    # Extrac pair sentence accroding to the specific format of the inputfile
    wfd = codecs.open(output_gram_file, "w", encoding="utf8")
    sep = u"】 "
    line_length = len(doc_line)

    for i in range(line_length):
        #print doc_line[i]
        try:
            temp = doc_line[i].split(sep)
            sentences = temp[1].split(" ")
        except:
            print doc_line[i]
            continue
            raw_input()
        sentence_length = len(sentences)

        if sentence_length % 2 == 0:
            for i in range(0, sentence_length, 2):
                '''if sentences[i] == u"待明公放下":
                    print sentences[i]
                    print sentences[i+1]
                    print len(sentences[i])
                    print len(sentences[i+1])'''
                if len(sentences[i]) == len(sentences[i+1]):
                    if len(sentences[i]) > 2 and len(sentences[i+1])> 2:
                        if sentences[i][len(sentences[i])-1] != u"\n":
                            wfd.write(sentences[i] + '\n')
                        else:
                            wfd.write(sentences[i])
                        if sentences[i+1][len(sentences[i+1])-1] != u"\n":
                            wfd.write(sentences[i+1] + '\n')
                        else:
                            wfd.write(sentences[i+1])
    wfd.close()

    rfd = codecs.open(output_gram_file, "r", encoding="utf8")
    doc_line = rfd.readlines()
    rfd.close()

    wfd = codecs.open(output_file, "a", encoding="utf8")
    line_length = len(doc_line)
    for i in range(0, line_length, 2):
        if len(doc_line[i]) == len(doc_line[i+1]):
            wfd.write(doc_line[i])
            wfd.write(doc_line[i+1])
    wfd.close()


def MineCouplet(input_file, output_file):
    '''

    '''
    pass


# For test
if __name__ == "__main__":
    input_file = "../corpus/Tang_poetry_utf8.txt"
    output_gram_file = "../corpus/Tang_poetry_format_utf8.txt"
    output_file = "../corpus/couplet_train_inner_gram.txt"

    ProcessPoetry(input_file, output_gram_file, output_file)
