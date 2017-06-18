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


def main():
    """
    """
    # hello world
    show_hello()
    # create graph
    create_new_graph()


if __name__ == '__main__':
    main()
