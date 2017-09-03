from __future__ import print_function
from natd_parse import get_seq, input_len, output_len
from random import randint
import numpy as np
import tensorflow as tf
import os.path

# Use batch size 1 first
# Then group sequences of same length and batch them separately

# input_dim = (batch_size,seq_len,25)
# output_dim = (batch_size,1,5)

# Load instancies from text
filename = 'inst_10E5.txt'
model_name = 'lstm_64'
lstm_size = 64
batch_size = 16
seq_len = 60
learning_rate = 0.001
seq_lengths = None
  
def load_model(sess):
    if os.path.isfile(model_name+'.meta'):
        saver = tf.train.import_meta_graph(model_name+'.meta')
        saver.restore(sess,tf.train.latest_checkpoint('./'))
        return saver
    else:
        return None

def RNN(x, weights, biases):
    x = tf.reshape(x,[batch_size,seq_len,input_len])
    x = tf.unstack(x,seq_len,1)
    # x = tf.split(x,seq_len,2)   # split along seq_len dimension
    # 1-layer LSTM with lstm_size units
    rnn_cell = tf.contrib.rnn.BasicLSTMCell(lstm_size)
    #rnn_cell = tf.contrib.rnn.MultiRNNCell([tf.contrib.rnn.BasicLSTMCell(lstm_size),tf.contrib.rnn.BasicLSTMCell(lstm_size)])
    # output and state
    outputs, states = tf.contrib.rnn.static_rnn(rnn_cell,x,dtype=tf.float32) # [seq_len]*batch_size sequence_length=seq_lengths
    # use only the last output
    #outputs = tf.stack(outputs)
    #outputs = tf.transpose(outputs, [1,0,2])
    #index = tf.range(0,batch_size)*seq_len+seq_len-1
    #outputs = tf.gather(tf.reshape(outputs, [-1, lstm_size]), index)
    out_ = tf.matmul(outputs[-1],weights)+biases
    #return tf.nn.softmax(out_)
    return out_

W = tf.Variable(tf.random_normal([lstm_size,output_len],stddev=0.01))
b = tf.Variable(np.zeros([output_len],dtype='float32'))
X = tf.placeholder(tf.float32,[batch_size,None,input_len]) # input_len*seq_len
Y = tf.placeholder(tf.float32,[batch_size,output_len])

model = RNN(X,W,b)
#cost = tf.reduce_mean(tf.losses.softmax_cross_entropy(onehot_labels=Y,logits=model))
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model,labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
#optimizer = tf.train.RMSPropOptimizer(learning_rate=learning_rate).minimize(cost)

sess = tf.Session()
with open(filename) as f:
    sess.run(tf.global_variables_initializer())
    #
    saver = load_model(sess)
    if saver == None:
        saver = tf.train.Saver()
    #
    lines = f.readlines()
    mean_loss = 0
    data_len = len(lines)
    for k in range(data_len-batch_size):
        x,y = get_seq(lines,seq_len,randint(0,data_len-batch_size),batch_size)
        if x != None and y != None:
            _, loss, onehot_pred = sess.run([optimizer,cost,model], feed_dict={X: x, Y: y})
            if k%100 == 99:
                print(mean_loss/100)  # ,onehot_pred,y
                print(onehot_pred[0])
                print(y[0])
                mean_loss = 0
            else:
                mean_loss += loss
            if k%2000 == 0:
                saver.save(sess,model_name)

