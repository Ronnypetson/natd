import numpy

input_len = 26  # 20 var, 6 special
output_len = 5  # rule identifier
char_map = {'~':20,'^':21,'F':22,',':23,'>':24,':':25}

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
    vec = numpy.zeros(input_len)
    if i >= 0:
        vec[i] = 1.0
    return vec

def one_hot_rule(i):
    vec = numpy.zeros(output_len)
    if i >= 0 and i < output_len:
        vec[i] = 1.0
    return vec

