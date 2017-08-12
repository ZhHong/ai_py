'''
tensorflow 模型
'''
import tensorflow as tf

def tensor_mode():
    '''
    tensorflow 模型
    '''
    w1 = tf.Variable(tf.random_normal([2,3],stddev=1))
    w2 = tf.Variable(tf.random_normal([3,1],stddev=1))

    #定义placeholder作为数据输入的地方
    # x = tf.placeholder(tf.float32,shape=(1,2),name ='input')
    x = tf.placeholder(tf.float32,shape=(3,2),name ='input')
    a = tf.matmul(x,w1)
    y = tf.matmul(a,w2)

    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        # print("Result ===>",sess.run(y,feed_dict={x:[[0.7,0.9]]}))
        print("Result ===>",sess.run(y,feed_dict={x:[[0.7,0.9],[0.1,0.4],[0.5,0.8]]}))

def main():
    tensor_mode()

if __name__ == '__main__':
    main()