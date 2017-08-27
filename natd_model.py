from __future__ import print_function
from natd_parse import get_seq, input_len, output_len
import numpy as np
import tensorflow as tf

# Use batch size 1 first
# Then group sequences of same length and batch them separately

# input_dim = (batch_size,seq_len,25)
# output_dim = (batch_size,1,5)

# Load instancies from text
filename = 'inst_10E5.txt'
lstm_size = 256
batch_size = 1
seq_len = 80
learning_rate = 0.001

def RNN(x, weights, biases):
    #x = tf.reshape(x,[batch_size,input_len,seq_len])
    x = tf.split(x,seq_len,1)
    # 1-layer LSTM with lstm_size units
    rnn_cell = tf.contrib.rnn.BasicLSTMCell(lstm_size)
    #rnn_cell = tf.contrib.rnn.MultiRNNCell([tf.contrib.rnn.BasicLSTMCell(lstm_size),tf.contrib.rnn.BasicLSTMCell(lstm_size)])
    # output and state
    outputs, states = tf.contrib.rnn.static_rnn(rnn_cell,x,dtype=tf.float32)
    # use only the last output
    out1 = tf.matmul(outputs[-1],weights)+biases
    return tf.nn.softmax(out1)

W = tf.Variable(tf.random_normal([lstm_size,output_len],stddev=0.01))
b = tf.Variable(np.zeros((output_len),dtype='float32'))
#b = tf.Variable(tf.random_normal([output_len],stddev=0.01))
X = tf.placeholder(tf.float32,[batch_size,input_len*seq_len])
Y = tf.placeholder(tf.float32,[batch_size,output_len])

model = RNN(X,W,b)
#cost = tf.reduce_mean(tf.losses.softmax_cross_entropy(onehot_labels=Y,logits=model))
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model,labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
#optimizer = tf.train.RMSPropOptimizer(learning_rate=learning_rate).minimize(cost)

sess = tf.Session()
with open(filename) as f:
    sess.run(tf.global_variables_initializer())
    k = 1
    mean_loss = 0.0
    for line in f:
        x,y = get_seq(line,seq_len)
        if x != None and y != None:
            _, loss, onehot_pred = sess.run([optimizer,cost,model], feed_dict={X: x, Y: y})
            mean_loss += loss
            if k%100 == 0:
                print(mean_loss/k,onehot_pred,y)
            k = k+1

