from __future__ import print_function
from natd_parse import get_seq, input_len, output_len
from random import randint
import numpy as np
import tensorflow as tf
import os.path

# input_dim = (batch_size,seq_len,25)
# output_dim = (batch_size,1,5)

filename = 'inst_10E6.txt'
model_name = 'lstm_64'
lstm_size = 64
batch_size = 16
seq_len = 60
learning_rate = 0.001
seq_lengths = None

def RNN(x, weights, biases):
    x = tf.reshape(x,[batch_size,seq_len,input_len])
    x = tf.unstack(x,seq_len,1)
    rnn_cell = tf.contrib.rnn.BasicLSTMCell(lstm_size)
    #rnn_cell = tf.contrib.rnn.MultiRNNCell([tf.contrib.rnn.BasicLSTMCell(lstm_size),tf.contrib.rnn.BasicLSTMCell(lstm_size)])
    outputs, states = tf.contrib.rnn.static_rnn(rnn_cell,x,dtype=tf.float32)
    out_ = tf.matmul(outputs[-1],weights)+biases
    return out_

W = tf.Variable(tf.random_normal([lstm_size,output_len],stddev=0.01))
b = tf.Variable(np.zeros([output_len],dtype='float32'))
X = tf.placeholder(tf.float32,[batch_size,None,input_len])
Y = tf.placeholder(tf.float32,[batch_size,output_len])

model = RNN(X,W,b)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model,labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

with open(filename) as f:
    sv = tf.train.Supervisor(logdir='/checkpoint',save_model_secs=60)
    with sv.managed_session() as sess:
        if not sv.should_stop():
            lines = f.readlines()
            mean_loss = 0
            data_len = len(lines)
            for k in range(data_len-batch_size):
                x,y = get_seq(lines,seq_len,randint(0,data_len-batch_size),batch_size)
                if x != None and y != None:
                    _, loss, onehot_pred = sess.run([optimizer,cost,model], feed_dict={X: x, Y: y})
                    if k%100 == 99:
                        print(mean_loss/100)
                        print(onehot_pred[0])
                        print(y[0])
                        mean_loss = 0
                    else:
                        mean_loss += loss

