#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TensorFlow 测试代码
"""

import tensorflow as tf


def show_hello():
    '''
    TensorFlow的Hello World.
    '''
    session = tf.Session()
    tensor_first = tf.constant(1.0)
    tensor_second = tf.constant(2.0)

    print('tensor graph         :', tensor_first.graph)  # 获取当前tensor的计算图
    print('current default graph:', tf.get_default_graph())  # 获取当前默认的计算图

    result = session.run(tensor_first + tensor_second)

    print("tensorflow run result:", result)

    session.close()


def create_new_graph():
    '''
    生成新的计算图
    '''
    g1 = tf.Graph()
    with g1.as_default():
        # v = tf.get_variable("v", initializer=tf.zeros_initializer(shape=[1]))
        # error: 参数错误 
        v = tf.get_variable("v", initializer=tf.zeros(shape=[1]))
    
    g2 = tf.Graph()
    with g2.as_default():
        # v = tf.get_variable("v", initializer=tf.ones_initializer(shape=[1])) 
        # error: 参数错误 
        # v = tf.get_variable("v", initializer=tf.ones_initializer(shape=[1])) 
        v = tf.get_variable("v", initializer=tf.ones(shape=[1]))        

    print("g1 :", g1)
    print("g2 :", g2)
    with tf.Session(graph=g1) as sess:
        # tf.initialize_all_variables().run() 老版本的初始化
        tf.global_variables_initializer().run()
        with tf.variable_scope("", reuse=True):
            print("g1 :", sess.run(tf.get_variable("v")))

    with tf.Session(graph=g2) as sess:
        # tf.initialize_all_variables().run() 老版本的初始化
        tf.global_variables_initializer().run()
        with tf.variable_scope("", reuse=True):
            print("g2 :", sess.run(tf.get_variable("v")))

def show_tensor():
    '''
    数据模型
    '''
    a = tf.constant([1.0,2.0],name ='a');
    b = tf.constant([2.0,3.0],name = 'b');

    result = tf.add(a,b,name ='add');

    print(a)
    print(b)
    print(result)

def show_run_model():
    '''
    运行模型
    '''
    a = tf.constant([1,2],name ='a')
    b = tf.constant([1,2],name ='b')
    r = tf.add(a,b)
    sess1 = tf.Session();
    rr = sess1.run(r);
    sess1.close();

    print(rr)

    with tf.Session() as sess:
        rrr = sess.run(tf.add(a,b));
        print(rrr)

def show_tensor_arg():
    '''
    神经网络参数与tensor变量
    '''
    w1 = tf.Variable(tf.random_normal([2,3],stddev=1,seed=1))
    w2 = tf.Variable(tf.random_normal([3,1],stddev=1,seed=1))

    x = tf.constant([[0.7,0.9]])

    a= tf.matmul(x,w1)
    y = tf.matmul(a,w2)

    with tf.Session() as sess:
        #初始化所有变量
        tf.global_variables_initializer().run()
        print("TENSOR ARGS: ",sess.run(y))

def main():
    """
    """
    # hello world
    show_hello()
    # create graph
    create_new_graph()
    # show tensor
    show_tensor()
    # show run model
    show_run_model()
    # 神经网络参数与tensor变量
    show_tensor_arg()


if __name__ == '__main__':
    main()
