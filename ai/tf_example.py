
import tensorflow as tf
import numpy as np

def example():
    '''
    '''
    # 定义训练数据 batch大小
    batch_size = 8

    # 定义神经网络参数
    w1 = tf.Variable(tf.random_normal([2,3],stddev=1,seed=1))
    w2 = tf.Variable(tf.random_normal([3,1],stddev=1,seed=1))

    # w1 = tf.Variable(tf.random_normal([2,3],stddev=1))
    # w2 = tf.Variable(tf.random_normal([3,1],stddev=1))
    #定义输入数据
    x = tf.placeholder(tf.float32,shape=(None,2),name ='x-input')
    y_= tf.placeholder(tf.float32,shape=(None,1),name ='y-input')

    # 定义传播过程
    a =tf.matmul(x,w1)
    y = tf.matmul(a,w2)

    # 定义损失函数 和反向传播算法
    cross_entropy = -tf.reduce_mean(
        y_*tf.log(tf.clip_by_value(y,1e-10,1.0))
    )

    train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)

    # 随机生成模拟数据集
    rdm = np.random.RandomState(1)
    dataset_size =128
    X = rdm.rand(dataset_size,2)

    #定义规则 给出样本标签
    Y = [[int(x1+x2)<1] for (x1,x2) in X]
    # print("Y===>",Y)
    # 创建会话
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        print("Before Tain :",sess.run(w1))
        print("Before Tain :",sess.run(w2))

        # 设定训练轮数

        loop_times = 5000

        for i in range(loop_times):
            #每次选取batch_size的样本进行训练
            start = (i * batch_size) %dataset_size
            end = min(start + batch_size,dataset_size)
            # 通过选取样本训练神经网络 并更新参数
            sess.run(train_step,feed_dict={x:X[start:end],y_:Y[start:end]})
            
            if i %1000 ==0:
                #每隔一段时间计算所有数据的交叉熵
                total_cross_entropy = sess.run(cross_entropy,feed_dict={x:X,y_:Y})
                print("After %d trainning steps, cross entropy on all data is %g"%(i,total_cross_entropy))
        
        print("After Tain :",sess.run(w1))
        print("After Tain :",sess.run(w2))

def my_sample():
    '''
    '''
    #定义batch size
    batch_size = 8
    #定义神经网络参数
    w1 = tf.Variable(tf.random_normal([2,3],stddev=1,seed =1))
    w2 = tf.Variable(tf.random_normal([3,1],stddev=1,seed =1))
    #定义输入数据
    x = tf.placeholder(tf.float32,shape=(None,2),name ='input-x')
    y_ = tf.placeholder(tf.float32,shape=(None,1),name ='input-y')
    #定义传递方向
    a = tf.matmul(x,w1)
    y = tf.matmul(a,w2)

    #定义损失函数和反向传递算法
    cross_entropy = -tf.reduce_mean(y_*tf.log(tf.clip_by_value(y,1e-10,1.0)))
    train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)
    #随机生成数据集
    rdm = np.random.RandomState(1)
    dataset_size = 128
    X = rdm.rand(dataset_size,2)
    #定义规则给出样本标签
    Y = [[int(x1+x2)<1] for (x1,x2) in X]
    # print("X:",X)
    # print("Y:",Y)
    #创建会话
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        print("Befor Train:",sess.run(w1))
        print("Befor Train:",sess.run(w2))

        loop_times = 5000

        for i in range(loop_times):
            start = (i * batch_size) %dataset_size
            end = min(start + batch_size,dataset_size)
            # print("start -->",start)
            # print("end----->",end)
            sess.run(train_step,feed_dict={x:X[start:end],y_:Y[start:end]})

            if i%1000 ==0:
                total_cross_entropy = sess.run(cross_entropy,feed_dict={x:X,y_:Y})
                print("After %d steps trainning,cross entropy on all data is %g"%(i,total_cross_entropy))
        
        print("After Train:",sess.run(w1))
        print("After Train:",sess.run(w2))

def my_sample1():
    #定义batch size
    batch_size = 8
    #定义参数
    w1 = tf.Variable(tf.random_normal([2,3],stddev =1,seed =1))
    w2 = tf.Variable(tf.random_normal([3,1],stddev =1,seed =1))

    #定义输入数据
    x = tf.placeholder(tf.float32,shape =(None,2),name ='input-a')
    y_ = tf.placeholder(tf.float32,shape =(None,1),name ='input-y')
    #定义传输算法
    a = tf.matmul(x,w1)
    y = tf.matmul(a,w2)

    #定义损失函数
    cross_entropy = -tf.reduce_mean(y_*tf.log(tf.clip_by_value(y,1e-10,1)))
    #定义反向传输
    train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)

    #随机输入数据
    rdm = np.random.RandomState(seed=1)
    dataset_size =128;
    X = rdm.rand(dataset_size,2)

    Y = [[int(x1+x2)<1] for (x1,x2) in X]

    #定义训练次数
    loop_times =5000

    #训练
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        print("Before train:",sess.run(w1))
        print("Before train:",sess.run(w2))

        for i in range(loop_times):
            begin = (i * batch_size) %dataset_size
            end = min(begin+batch_size,dataset_size)

            sess.run(train_step,feed_dict={x:X[begin:end],y_:Y[begin:end]})

            if i%1000 ==0:
                total_cross_entropy = sess.run(cross_entropy,feed_dict ={x:X,y_:Y})
                print("After %d steps, total_cross_entropy %g"%(i,total_cross_entropy))
        print("After train:",sess.run(w1))
        print("After train:",sess.run(w2))

def main():

    example()

    my_sample()

    my_sample1();

if __name__ == '__main__':
    main()