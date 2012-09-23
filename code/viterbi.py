#!/usr/bin/env python
#encoding=utf8

import numpy as np

def ViterbiDecode(hidden_transfer, hidden_visible_transfer, init_pro, hidden_candidate_words, visible_words, top_k, top_couplet_k=1):
    '''
    Function: Use Viterbi algorithm to find most probable hidden word sequence
    Input: Five input variables corresponding to five tuple of HMM model. Var: top_couplet_k --> Specify the top k most likely generated second line of couplet
    Output: Return the most probable hidden word sequence
    '''
    state_num = len(visible_words)
    state_pro_matrix = np.random.rand(top_k, state_num)
    state_optimal_route = np.array([0 for i in range(state_num*top_k)], dtype="i").reshape(top_k, state_num)
    optimal_path = np.array([0 for i in range(state_num*top_couplet_k)], dtype="i").reshape(top_couplet_k, state_num)
    '''print np.array([0 for i in range(state_num*top_couplet_k)], dtype="i").reshape(1,3)
    print len(optimal_path[0,:])
    print state_num'''
    max_prob = np.array([0 for i in range(top_couplet_k)], dtype="i")

    ## 1.Initialization
    state_pro_matrix[:, 0] = init_pro[:] * hidden_visible_transfer[:,0]

    ## 2.Recursion
    for i in range(0, state_num-1):
        state_pro_matrix[:, i+1] = np.max(state_pro_matrix[:,i].reshape(-1,1) * hidden_transfer[i,:,:] * hidden_visible_transfer[:,i+1], 0)
        '''print "state_pro_matrix"
        print state_pro_matrix[:, i].reshape(-1,1)
        a = state_pro_matrix[:,i].reshape(-1,1) * hidden_transfer[i,:,:] * hidden_visible_transfer[:,i+1]
        print "hidden_transfer"
        print hidden_transfer[i,:,:]
        print "hidden_visible"
        print hidden_visible_transfer[:,i+1]
        print "State_pro_matrix"
        print a
        print "State_pro_matrix_choose"
        print state_pro_matrix[:,i+1]'''
        state_optimal_route[:, i+1] = np.argmax(state_pro_matrix[:,i].reshape(-1,1) * hidden_transfer[i,:,:] * hidden_visible_transfer[:,i], 0)
        '''print "optimal route"
        print state_optimal_route[:,i+1]
        raw_input()'''

    ## 3.Find word having max probability
    max_last_word_index = np.argmax(state_pro_matrix[:,state_num-1])
    max_prob = state_pro_matrix[max_last_word_index, state_num-1]


    ## 4.Path backtracking
    word_index = max_last_word_index
    '''print state_optimal_route
    print len(optimal_path)'''
    optimal_path[top_couplet_k-1, state_num-1] = max_last_word_index
    for i in range(state_num-1, 0, -1):
        optimal_path[top_couplet_k-1, i-1] = state_optimal_route[word_index, i]
        word_index = optimal_path[top_couplet_k-1, i-1]

    #print optimal_path, max_prob
    return optimal_path, max_prob

#----For test----
if __name__ == "__main__":
    hidden_transfer = np.array([[[0.5, 0.3, 0.2], [0.1, 0.8, 0.1], [0.7, 0.1, 0.2]],\
        [[0.4, 0.3, 0.3], [0.7, 0.1, 0.2], [0.1, 0.4, 0.5]]])
    hidden_visible_transfer = np.array([[0.2, 0.3, 0.6], [0.6, 0.8, 0.3], [0.3, 0.4, 0.2]])
    init_pro = np.array([0.2, 0.5, 0.3])
    top_k = 3
    visible_words = ["中", "国", "龙"]

    ViterbiDecode(hidden_transfer, hidden_visible_transfer, init_pro, [], visible_words, top_k)
