from __future__ import print_function
from natd_parse import get_seq
import numpy as np

# Use batch size 1 first
# Then group sequences of same length and batch them separately

# input_dim = (1,seq_len,25)
# output_dim = (1,1,5)

# Load instancies from text
filename = 'inst.txt'
X = []
Y = []
with open(filename) as f:
    for line in f:
        x,y = get_seq(line)
        X.append(x)
        Y.append(y)
print(X.shape)
print(Y.shape)

