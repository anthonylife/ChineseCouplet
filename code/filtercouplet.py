#!/usr/bin/env python
#encoding=utf8

#---% Some linguistic hard rules for modifying the second line of couplet %---#i

import numpy as np

def RepeatWords(up_couplet, down_couplet):
    '''
    Function: accroding to the words repeated format of up couplet, modify the down_couplet
    '''
    length_couplet = down_couplet.shape[1]
    print length_couplet
    repeat_tags = np.array([-1 for i in range(length_couplet)])

    for i in range(1, length_couplet):
        for j in range(0, i):
            if up_couplet[i] == up_couplet[j]:
                repeat_tags[i] = j
                break

    print repeat_tags

    for i in range(len(down_couplet)):
        for j in range(length_couplet):
            if repeat_tags[j] >= 0:
                down_couplet[i][j] = down_couplet[i][repeat_tags[j]]

    return down_couplet

# for test
if __name__ == "__main__":
    a = ["ha", "hb", "ha", "hc"]
    b = np.array([10,2,3,4]).reshape(1,4)
    c = RepeatWords(a, b)
    print c
