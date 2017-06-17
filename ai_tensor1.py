#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    test tensorflow one day
"""

import tensorflow as tf


def main():
    """
    show hello
    """
    session = tf.Session()
    tensor_first = tf.constant(1.0)
    tensor_second = tf.constant(2.0)

    result = session.run(tensor_first + tensor_second)

    print("tensorflow run result ---->", result)


if __name__ == '__main__':
    main()
