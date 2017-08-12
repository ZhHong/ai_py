import tensorflow as tf
import numpy as np

def sample():
    batch_size = 8

    w1 = tf.Variable(tf.random_normal([2,3],stddev =1,seed =1))
    w2 = tf.Variable(tf.random_normal([3,1],stddev =1,seed =1))

    x = tf.placeholder(tf.float32,shape =(None,2),name='input-x')
    y_ = tf.placeholder(tf.float32,shape =(None,1),name ='input-y')

    a = tf.matmul(x,w1)
    y = tf.matmul(a,w2)

    rdm = np.random.RandomState(seed =1)
    dataset_size = 128
    X = rdm.rand(dataset_size,2)
    Y = [[int(x1+x2)<1] for (x1,x2) in X]

    cross_entropy = -tf.reduce_mean(y_*tf.log(tf.clip_by_value(y,1e-10,1)))
    train_step = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cross_entropy)
    loop_times = 5000

    with tf.Session() as sess:
        tf.global_variables_initializer().run();
        print("Before train W1:",sess.run(w1))
        print("Before train w2:",sess.run(w2))

        for i in range(loop_times):
            begin = (i*batch_size) % dataset_size
            end = min(begin+batch_size,dataset_size)

            sess.run(train_step,feed_dict={x:X[begin:end],y_:Y[begin:end]})

            if i%1000 ==0:
                total_cross_entropy = sess.run(cross_entropy,feed_dict={x:X,y_:Y})
                print("After %d steps train,total cross entropy %g"%(i,total_cross_entropy))
        print("After train w1:",sess.run(w1))
        print("After train w2:",sess.run(w2))

def main():
    sample()

if __name__ == '__main__':
    main()