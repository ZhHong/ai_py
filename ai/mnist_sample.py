from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

mnist = input_data.read_data_sets("MNIST_data/",one_hot=True)

x = tf.placeholder(tf.float32,shape =(None,784),name ='input-x')
y_ = tf.placeholder(tf.float32,shape=(None,10),name ='input-y')

W = tf.Variable(tf.zeros(shape =(784,10)))
b = tf.Variable(tf.zeros(shape =(10)))
y = tf.nn.softmax(tf.matmul(x,W)+b)

cross_entropy = -tf.reduce_sum(y_*tf.log(y))
# cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y),reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(learning_rate = 0.01).minimize(cross_entropy)

loop_times = 10000

with tf.Session() as sess:
    tf.global_variables_initializer().run()

    for i in range(loop_times):
        batch_xs,batch_ys = mnist.train.next_batch(50)
        sess.run(train_step,feed_dict={x:batch_xs,y_:batch_ys})
        
        if i %1000 ==0:
            # total_cross = sess.run(cross_entropy,feed_dict={x:x,y_:y})
            print("after %d steps train,total cross is %g"%(i,0))
    correct_prediction = tf.equal(tf.argmax(y,1),tf.arg_max(y_,1)) 
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
    print(sess.run(accuracy,feed_dict={x:mnist.test.images,y_:mnist.test.labels}))