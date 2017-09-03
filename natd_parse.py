import numpy as np
from random import randint

input_len = 25  # 20 var, 5 special
output_len = 5  # rule identifier
char_map = {'~':20,'^':21,'F':22,',':23,'>':24}

def char_index(c):
    ordc = ord(c)
    orda = ord('a')
    if ordc >= orda and ordc < orda+20:
        return ordc-orda
    if c in char_map:
        return char_map[c]
    return -1

def one_hot_char(c):
    i = char_index(c)
    vec = np.zeros(input_len)
    if i >= 0:
        vec[i] = 1.0
    return vec

def one_hot_rule(i):
    vec = np.zeros(output_len)
    if i >= 0 and i < output_len:
        vec[i] = 1.0
    return vec

def get_seq(s, seq_len, start, batch_size):    # returns padded sequence
    X = np.zeros((batch_size,seq_len,input_len))
    Y = np.zeros((batch_size,output_len))
    for i in range(start,start+batch_size):
        p = len(s[i])-3
        if p > seq_len or s[i][p] != ':':
            return None,None
        #x = [[0.0]*input_len]*seq_len   # seq_len
        x = np.random.normal(0.0,0.1,(seq_len,input_len))
        b = randint(0,seq_len-p)
        for j in range(p):
            x[j+b][char_index(s[i][j])] = 1.0  # input is squashed
        for j in range(p+b,seq_len):
            x[j] = np.zeros((input_len))
        rule = ord(s[i][p+1])-ord('0')
        y = one_hot_rule(rule)
        #
        X[i-start] = x
        Y[i-start] = y
    return X,Y

